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
HF_MODEL = os.getenv('HF_MODEL', 'meta-llama/Meta-Llama-3-8B-Instruct')

hf_client = None
if HF_TOKEN:
    hf_client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)


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
    bot_response = re.sub(r'\s+-\s+\*\*', '\n\n- **', bot_response)
    bot_response = re.sub(r'\s+(\d+\.)\s+', r'\n\n\1 ', bot_response)
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
                    "You are GenChat, a professional AI assistant created by Utkarsh. "
                    "Your responses are powered by the Qwen 2.5 Instruct model through "
                    "the Hugging Face API. "

                    "If asked who created you, who made you, or who developed you, "
                    "always say that the GenChat application was developed by Utkarsh, "
                    "while your AI capabilities are powered by the Qwen model through "
                    "Hugging Face. "

                    "Answer accurately and naturally. "
                    "Use headings, bullet points, and numbered lists whenever they "
                    "improve readability. "
                    "Avoid long unbroken paragraphs. "
                    "Leave a blank line between different sections. "
                    "Do not mention Alibaba Cloud unless the user specifically asks "
                    "about Alibaba Cloud."
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
