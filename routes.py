from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from utils import send_simple_email
from datetime import datetime


def create_routes(app: FastAPI):
    """Create and register all API routes"""
    
    @app.get("/")
    async def root():
        """Root endpoint to check if the server is running"""
        return {"message": "Webhook server is running"}

    @app.post("/webhook")
    async def receive_webhook(request: Request):
        """
        Receive webhook events and send email notification
        """
        try:
            payload = await request.json()
            
            # Extract event information with fallbacks
            event_type = (
                payload.get("event_type") or
                payload.get("type") or
                payload.get("event") or
                payload.get("action") or
                "Unknown Event"
            )
            
            # Extract repository information
            repository_name = "Unknown Repository"
            if "repository" in payload and isinstance(payload["repository"], dict):
                repository_name = payload["repository"].get("name", "Unknown Repository")
            elif "repo" in payload and isinstance(payload["repo"], dict):
                repository_name = payload["repo"].get("name", "Unknown Repository")
            elif "repository_name" in payload:
                repository_name = payload["repository_name"]
            
            # Extract additional useful information
            commit_info = ""
            if "commits" in payload and payload["commits"]:
                commit = payload["commits"][0]
                commit_id = commit.get("id", "")[:8] if commit.get("id") else ""
                commit_message = commit.get("message", "No message")
                commit_author = commit.get("author", {}).get("name", "Unknown") if commit.get("author") else "Unknown"
                commit_info = f"""
                <tr>
                    <td style="padding: 10px 15px; font-weight: bold;">Latest Commit:</td>
                    <td style="padding: 10px 15px;">{commit_id} - {commit_message[:50]}{'...' if len(commit_message) > 50 else ''}</td>
                </tr>
                <tr style="background-color: #e8f0fe;">
                    <td style="padding: 10px 15px; font-weight: bold;">Author:</td>
                    <td style="padding: 10px 15px;">{commit_author}</td>
                </tr>
                """
            
            # Extract branch information
            branch = "Unknown Branch"
            if "ref" in payload:
                ref = payload["ref"]
                if ref.startswith("refs/heads/"):
                    branch = ref.replace("refs/heads/", "")
                else:
                    branch = ref
            elif "branch" in payload:
                branch = payload["branch"]
            
            # Extract sender/actor information
            sender = "Unknown User"
            if "sender" in payload and isinstance(payload["sender"], dict):
                sender = payload["sender"].get("login", "Unknown User")
            elif "actor" in payload and isinstance(payload["actor"], dict):
                sender = payload["actor"].get("login", "Unknown User")
            elif "pusher" in payload and isinstance(payload["pusher"], dict):
                sender = payload["pusher"].get("name", "Unknown User")
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create a more descriptive email subject
            email_subject = f"[{event_type}] {repository_name}"
            
            # Create a more detailed and professional email body
            email_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border-radius: 12px; background: #f9fafb; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <h2 style="color: #1a73e8; text-align: center;">📢 Repository Activity Notification</h2>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr style="background-color: #e8f0fe;">
                    <td style="padding: 10px 15px; font-weight: bold;">Event Type:</td>
                    <td style="padding: 10px 15px;">{event_type}</td>
                    </tr>
                    <tr>
                    <td style="padding: 10px 15px; font-weight: bold;">Repository:</td>
                    <td style="padding: 10px 15px;">{repository_name}</td>
                    </tr>
                    <tr style="background-color: #e8f0fe;">
                    <td style="padding: 10px 15px; font-weight: bold;">Branch:</td>
                    <td style="padding: 10px 15px;">{branch}</td>
                    </tr>
                    <tr>
                    <td style="padding: 10px 15px; font-weight: bold;">Triggered By:</td>
                    <td style="padding: 10px 15px;">{sender}</td>
                    </tr>
                    {commit_info}
                    <tr style="background-color: #e8f0fe;">
                    <td style="padding: 10px 15px; font-weight: bold;">Timestamp:</td>
                    <td style="padding: 10px 15px;">{current_time}</td>
                    </tr>
                </table>
                
                <div style="margin-top: 25px; padding: 15px; background-color: #f0f7ff; border-radius: 8px; border-left: 4px solid #1a73e8;">
                    <p style="margin: 0; font-size: 14px; color: #555;">
                        <strong>📋 Summary:</strong> A <em>{event_type.lower()}</em> event was triggered in the <strong>{repository_name}</strong> repository
                        {f'on the <strong>{branch}</strong> branch' if branch != 'Unknown Branch' else ''}.
                        {f' This action was performed by <strong>{sender}</strong>.' if sender != 'Unknown User' else ''}
                    </p>
                </div>
                
                <p style="text-align: center; color: #666; margin-top: 25px; font-size: 13px;">
                    ⏱️ This notification was automatically generated by your webhook system.
                </p>
                </div>
            </body>
            </html>
            """
            
            email_sent = send_simple_email(email_subject, email_body)
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Webhook received successfully",
                    "email_sent": email_sent,
                    "event_type": event_type,
                    "repository": repository_name
                }
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

