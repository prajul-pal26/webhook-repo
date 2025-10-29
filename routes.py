from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
from utils import send_simple_email

def create_routes(app: FastAPI):
    """Create and register all API routes"""
    
    @app.get("/")
    async def root():
        """Root endpoint to check if the server is running"""
        return {"message": "Webhook server is running"}

    @app.post("/webhook")
    async def receive_webhook(request: Request):
        """
        Receive webhook events from action-repo and send email notification
        """
        try:
            # Get request details for debugging
            request_method = request.method
            request_url = str(request.url)
            request_headers = dict(request.headers)
            
            # Try to get the webhook payload
            try:
                payload = await request.json()
                payload_str = json.dumps(payload, indent=2)
                payload_type = "JSON"
            except Exception as json_error:
                # If JSON parsing fails, try to get raw body
                try:
                    body = await request.body()
                    payload_str = body.decode('utf-8') if body else "Empty body"
                    payload = {"raw_body": payload_str}
                    payload_type = "Raw Text"
                except Exception as body_error:
                    payload_str = f"Unable to read body: {str(body_error)}"
                    payload = {"error": payload_str}
                    payload_type = "Error"
            
            # Extract information from payload (handle different structures)
            if isinstance(payload, dict):
                # Try common field names
                event_type = (
                    payload.get("event_type") or
                    payload.get("type") or
                    payload.get("event") or
                    payload.get("action") or
                    "Unknown Event"
                )
                
                event_data = (
                    payload.get("data") or
                    payload.get("payload") or
                    payload.get("body") or
                    payload
                )
                
                timestamp = (
                    payload.get("timestamp") or
                    payload.get("time") or
                    payload.get("created_at") or
                    str(request.headers.get("date", "Unknown Time"))
                )
            else:
                event_type = "Unknown Event"
                event_data = payload
                timestamp = str(request.headers.get("date", "Unknown Time"))
            
            # Create email subject
            email_subject = f"Webhook Notification: {event_type}"
            
            # Format the email body with comprehensive information
            email_body = f"""
            Webhook Event Received
            
            Request Information:
            - Method: {request_method}
            - URL: {request_url}
            - Payload Type: {payload_type}
            - Timestamp: {timestamp}
            
            Request Headers:
            {json.dumps(request_headers, indent=2)}
            
            Event Type: {event_type}
            
            Full Payload:
            {payload_str}
            
            Extracted Event Data:
            {json.dumps(event_data, indent=2) if isinstance(event_data, (dict, list)) else str(event_data)}
            
            ---
            This is an automated notification from the webhook system.
            """
            
            # Send email notification
            email_sent = send_simple_email(email_subject, email_body)
            
            # Prepare response with debugging info
            response_data = {
                "status": "success",
                "message": "Webhook received successfully",
                "email_sent": email_sent,
                "debug_info": {
                    "payload_type": payload_type,
                    "event_type": event_type,
                    "payload_keys": list(payload.keys()) if isinstance(payload, dict) else "Not a dict"
                }
            }
            
            if not email_sent:
                response_data["warning"] = "Webhook processed but email notification failed"
            
            return JSONResponse(
                status_code=200,
                content=response_data
            )
        
        except Exception as e:
            # Log the error and send error notification email
            error_subject = "Webhook Processing Error"
            error_body = f"""
            An error occurred while processing webhook:
            
            Error: {str(e)}
            
            Request details:
            Method: {request.method}
            URL: {request.url}
            Headers: {dict(request.headers)}
            
            Please check the webhook system for issues.
            """
            
            # Try to send error notification
            try:
                send_simple_email(error_subject, error_body)
            except:
                pass  # Don't let email errors break the error response
            
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

