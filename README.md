# 🚀 Webhook Notification Server

A lightweight and flexible **FastAPI-based webhook listener** that receives repository events (like pushes, merges, etc.) and sends email notifications with structured summaries.

---

## ✨ Features

- ⚡ Built with FastAPI — async and high-performance.
- 📬 Sends clean email notifications on each repository event.
- 🧩 Automatically extracts event type, branch, author, and commit info.
- 🌍 Ready for GitHub, GitLab, Bitbucket, and other webhook sources.
- 🪄 Ngrok support for easy public testing.

---

## 🧠 Tech Stack

| Component | Description |
|------------|-------------|
| **FastAPI** | API Framework |
| **Celery (optional)** | Async task queue |
| **Redis** | Broker/Backend for Celery |
| **Ngrok** | Local tunneling for webhook testing |
| **SMTP / Gmail API** | Email sending |

---

## ⚙️ Setup

```bash
# Clone this repo
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Create a virtual environment
python -m venv .env
source .env/bin/activate  # (or .env\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
uvicorn main:app --reload
