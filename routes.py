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
            # Get the webhook payload
            payload = await request.json()
            
            # Extract relevant information from payload
            event_type = payload.get("event_type", "Unknown Event")
            event_data = payload.get("data", {})
            timestamp = payload.get("timestamp", "Unknown Time")
            
            # Create email subject and body
            email_subject = f"Webhook Notification: {event_type}"
            
            # Format the email body with webhook data
            email_body = f"""
            Webhook Event Received
            
            Event Type: {event_type}
            Timestamp: {timestamp}
            
            Event Data:
            {json.dumps(event_data, indent=2)}
            
            ---
            This is an automated notification from the webhook system.
            """
            
            # Send email notification
            email_sent = send_simple_email(email_subject, email_body)
            
            # Prepare response
            response_data = {
                "status": "success",
                "message": "Webhook received successfully",
                "email_sent": email_sent
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

