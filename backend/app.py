import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Optional imports handled gracefully
try:
    from huggingface_hub import InferenceClient
except Exception:
    InferenceClient = None

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Load .env located in the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if load_dotenv:
    try:
        load_dotenv(os.path.join(BASE_DIR, ".env"))
    except Exception:
        pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

chat_history = []

# Initialize Hugging Face InferenceClient
hf_api = None
hf_api_key = os.getenv("HF_API_KEY")

if InferenceClient is None:
    logger.warning(
        "huggingface_hub.InferenceClient not available. Install huggingface-hub to enable HF API calls."
    )

elif not hf_api_key:
    logger.info("HF_API_KEY not set; Hugging Face client will not be initialized.")

else:
    try:
        hf_api = InferenceClient(token=hf_api_key)
        logger.info("Hugging Face InferenceClient initialized.")
    except Exception as e:
        hf_api = None
        logger.exception(
            "Failed to initialize Hugging Face InferenceClient: %s", e
        )


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # Read JSON request
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Store user message
        chat_history.append({
            "role": "user",
            "content": user_message
        })

        # Generate AI response
        if hf_api:
            response = hf_api.chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                model="Qwen/Qwen2.5-7B-Instruct",
                max_tokens=300
            )

            bot_response = response.choices[0].message.content

        else:
            bot_response = (
                "Hugging Face API is not configured. "
                "Please add your HF_API_KEY in the .env file."
            )

        # Store bot response
        chat_history.append({
            "role": "assistant",
            "content": bot_response
        })

        return jsonify({
            "message": bot_response,
            "history": chat_history
        })

    except Exception as e:
        logger.exception("Error in /api/chat: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Backend is running! ✅"
    })


@app.route("/api/clear", methods=["POST"])
def clear_chat():
    global chat_history
    chat_history = []

    return jsonify({
        "status": "Chat cleared"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    logger.info("Starting Flask app on 0.0.0.0:%s", port)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )