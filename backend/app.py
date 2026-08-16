from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

chat_history = []

HF_TOKEN = os.getenv('HUGGINGFACE_API_KEY')
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")

hf_client = None
if HF_TOKEN:
    hf_client = InferenceClient(
    model=HF_MODEL,
    token=HF_TOKEN
)


def generate_bot_response(messages):
    if not hf_client:
        raise RuntimeError(
            'Hugging Face API key not configured. Set HUGGINGFACE_API_KEY in .env'
        )

    response = hf_client.chat_completion(
        messages=messages,
        max_tokens=int(os.getenv('HF_MAX_TOKENS', '500')),
    )
    bot_response = response.choices[0].message.content.strip()
    
    return bot_response

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        chat_history.append({
            'role': 'user',
            'content': user_message
        })

        messages = [
            {
                "role": "system",
                "content": (
                    "content": (
                        "You are GenChat, a helpful and professional AI assistant. "
                        "Answer the user's question directly and naturally. "
                        "Do not talk about yourself, your creator, Utkarsh, your development, "
                        "your model, Hugging Face, or your technology unless the user specifically asks. "
                        "Do not use Markdown formatting. "
                        "Do not use #, ##, ###, **, *, bullet points, numbered lists, or Markdown symbols. "
                        "Write clean plain-text responses. "
                        "Avoid unnecessary introductions and do not repeat or restate the user's question. "
                        "Give only the information relevant to what the user asked."
                    )
                )
            }
        ]

        messages.extend(chat_history[-10:])

        try:
            bot_response = generate_bot_response(messages)
        except Exception as e:
            chat_history.pop()
            return jsonify({
                'error': f'AI request failed: {str(e)}'
            }), 502

        chat_history.append({
            'role': 'assistant',
            'content': bot_response
        })

        return jsonify({
            'message': bot_response,
            'history': chat_history
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    status = {
        'status': 'Backend is running!',
        'ai_enabled': hf_client is not None,
        'model': HF_MODEL if hf_client else None,
    }
    return jsonify(status)


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    global chat_history
    chat_history = []
    return jsonify({'status': 'Chat cleared'})


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=debug, port=port)
