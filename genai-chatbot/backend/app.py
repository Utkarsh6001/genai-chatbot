from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

chat_history = []

# Initialize Hugging Face API (free option)
try:
    hf_api = InferenceApi(api_key=os.getenv('HUGGINGFACE_API_KEY', 'hf_default'))
except:
    hf_api = None

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        chat_history.append({'role': 'user', 'content': user_message})
        
        # Simple response (can be upgraded with real AI)
        bot_response = f"Thanks for: {user_message}. I'm learning to respond better!"
        
        chat_history.append({'role': 'assistant', 'content': bot_response})
        
        return jsonify({
            'message': bot_response,
            'history': chat_history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend is running! ✅'})

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    global chat_history
    chat_history = []
    return jsonify({'status': 'Chat cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)