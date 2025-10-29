from fastapi import FastAPI
import uvicorn
from routes import create_routes

# Initialize FastAPI app
app = FastAPI(
    title="Webhook Receiver",
    description="Webhook endpoint to capture changes from action-repo",
    version="1.0.0"
)

# Register all routes
create_routes(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )