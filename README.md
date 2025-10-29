# webhook-repo

Webhook endpoint code to capture changes done on action-repo.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /` - Root endpoint to check if the server is running
- `POST /webhook` - Receive webhook events from action-repo
- `GET /health` - Health check endpoint

## Usage

Send POST requests to `http://localhost:8000/webhook` with your webhook payload.

## Development

To run the server in development mode with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
