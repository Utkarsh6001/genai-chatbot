# GenAI Chatbot

A simple full-stack chatbot with a Flask backend and vanilla HTML/CSS/JS frontend. Responses are generated via the [Hugging Face Inference API](https://huggingface.co/docs/huggingface_hub/guides/inference) using `InferenceClient`.

## Prerequisites

- Python 3.10+
- A [Hugging Face account](https://huggingface.co/) and API token

## Setup

1. Clone or download this repository.

2. Create a virtual environment and install dependencies:

   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```

3. Copy the example environment file and add your API key:

   ```bash
   copy .env.example .env       # Windows
   # cp .env.example .env       # macOS/Linux
   ```

   Edit `.env` and set `HUGGINGFACE_API_KEY` to your token from [Hugging Face settings](https://huggingface.co/settings/tokens).

## Run

1. Start the backend (from the `backend` directory):

   ```bash
   python app.py
   ```

   The API runs at `http://localhost:5000` by default.

2. Open the frontend:

   - Open `frontend/index.html` in your browser, or
   - Serve the folder with any static file server.

3. Chat in the UI. The frontend calls `POST /api/chat` on the backend.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check; includes `ai_enabled` and `model` |
| `POST` | `/api/chat` | Send `{ "message": "..." }`, get AI response |
| `POST` | `/api/clear` | Clear server-side chat history |

## Configuration

Environment variables (set in `backend/.env`):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HUGGINGFACE_API_KEY` | Yes | — | Hugging Face API token |
| `HF_MODEL` | No | `meta-llama/Meta-Llama-3-8B-Instruct` | Model ID for chat completion |
| `HF_MAX_TOKENS` | No | `500` | Max tokens per response |
| `FLASK_DEBUG` | No | `false` | Enable Flask debug mode |
| `PORT` | No | `5000` | Backend port |

## Project Structure

```
genai-chatbot/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/
│   ├── index.html          # Chat UI
│   ├── script.js           # Frontend logic
│   └── styles.css          # Styles
└── README.md
```

## Notes

- Chat history is stored in memory on the server and is lost when the backend restarts.
- Some models may require a paid Hugging Face plan or specific model access. If a model fails, try another `HF_MODEL` value.
- The frontend expects the backend at `http://localhost:5000` (see `frontend/script.js`).
