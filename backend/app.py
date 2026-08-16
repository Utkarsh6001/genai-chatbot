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
    bot_response = re.sub(r'\*\*(.*?)\*\*', r'\1', bot_response)
    bot_response = re.sub(r'(?<!\w)\*(.*?)(?<!\w)\*', r'\1', bot_response)
    bot_response = re.sub(r'`+', '', bot_response)
    bot_response = re.sub(r'^#{1,6}\s*', '', bot_response, flags=re.MULTILINE)
    
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
                    "You are GenChat, an AI assistant in an application developed by Utkarsh. "
                    "Answer the user's question directly and naturally. "
                    "Do not talk about yourself, your creator, your model, Hugging Face, OpenAI, "
                    "or how you were built unless the user specifically asks about those things. "

                    "If the user asks who created, built, made, or developed you, answer: "
                    "GenChat was developed by Utkarsh. "

                    "If the user asks what AI model you use, answer: "
                    "GenChat uses the Qwen 2.5 Instruct model through the Hugging Face API. "

                    "If the user asks who provides your AI capabilities, answer: "
                    "The AI capabilities are powered by the Qwen 2.5 Instruct model through Hugging Face. "

                    "Do not claim that you were built or created by OpenAI. "
                    "Do not claim to be ChatGPT. "
                    "Do not mention OpenAI unless the user specifically asks about OpenAI. "

                    "Keep answers relevant to the user's question. "
                    "Do not add unnecessary information about GenChat or its creator. "
                    "Do not use markdown headings with #. "
                    "Do not use asterisks (*) for formatting. "
                    "Use plain text, normal paragraphs, or simple numbered lists when needed."
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
