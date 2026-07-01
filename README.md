# 🤖 GenAI Chatbot

A simple AI chatbot built using **Flask** for the backend and **HTML, CSS, and JavaScript** for the frontend. The project demonstrates how a frontend communicates with a Python backend through REST APIs and is designed to be easily extendable with AI models such as Hugging Face.

---

## 🚀 Features

- Clean and responsive chat interface
- Flask REST API backend
- Frontend and backend communication using Fetch API
- CORS enabled for cross-origin requests
- Environment variables managed using `.env`
- Chat history support
- Clear chat functionality
- Health check API for backend status

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Python Dotenv

### AI
- Hugging Face API (Environment Variable Support)

---

## 📁 Project Structure

```
genai-chatbot/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── .env
│   └── requirements.txt
│
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/genai-chatbot.git
```

### 2. Move into the project folder

```bash
cd genai-chatbot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
HUGGINGFACE_API_KEY=your_api_key_here
```

### 5. Run the backend

```bash
python app.py
```

### 6. Open the frontend

Simply open `index.html` in your browser.

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/chat` | Send a message to the chatbot |
| POST | `/api/clear` | Clear chat history |
| GET | `/api/health` | Check backend status |

---

## 🎯 Learning Objectives

This project helped me understand:

- Frontend and Backend Integration
- REST API Development using Flask
- Handling JSON Requests and Responses
- Environment Variables using Dotenv
- Basic AI API Integration
- Project Structure and Organization

---

## 🔒 Security

Sensitive information such as API keys is stored using environment variables (`.env`) and is excluded from the repository through `.gitignore`.

---

## 🚀 Future Improvements

- Real AI-generated responses
- User authentication
- Database integration
- Chat history storage
- Better UI/UX
- Dark Mode
- Multiple AI model support

---

## 👨‍💻 Author

**Utkarsh Kaushal**

If you found this project helpful, feel free to ⭐ the repository.
