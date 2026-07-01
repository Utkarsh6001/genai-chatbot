# 🤖 GenAI Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/HTML5-Frontend-orange?style=for-the-badge&logo=html5">
  <img src="https://img.shields.io/badge/CSS3-Styling-blue?style=for-the-badge&logo=css3">
  <img src="https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript">
</p>

<p align="center">
A simple AI Chatbot built using <b>Flask</b> for the backend and <b>HTML, CSS & JavaScript</b> for the frontend. The chatbot demonstrates frontend-backend communication using REST APIs and is designed for AI integration using Hugging Face.
</p>

---

# 📌 Features

- 💬 Interactive Chat Interface
- ⚡ Flask Backend API
- 🔄 Frontend & Backend Communication
- 🌐 CORS Enabled
- 🔐 Environment Variables using `.env`
- 🧹 Clear Chat API
- ❤️ Health Check API
- 🤖 Hugging Face API Integration

---

# 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Python Dotenv

### AI Integration
- Hugging Face API

---

# 📂 Project Structure

```text
genai-chatbot/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
│
└── .gitignore
```

---

# 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Utkarsh6001/genai-chatbot.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd genai-chatbot
```

### 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4️⃣ Create a `.env` File

```env
HF_API_KEY=your_huggingface_api_key
```

### 5️⃣ Start the Backend

```bash
python backend/app.py
```

### 6️⃣ Run the Frontend

Open `frontend/index.html` in your browser.

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/chat` | Send a message to the chatbot |
| POST | `/api/clear` | Clear chat |
| GET | `/api/health` | Check backend status |

---

# 📸 Screenshots

> Add your project screenshots here.

### Home Page

```
assets/home.png
```

### Chat Interface

```
assets/chat.png
```

---

# 📖 What I Learned

- Building REST APIs using Flask
- Frontend and Backend Integration
- Fetch API
- JSON Request & Response Handling
- Environment Variables using Dotenv
- AI API Integration
- Project Organization

---

# 🔒 Security

API keys are stored securely using `.env` files and are excluded from the repository using `.gitignore`.

---

# 🚀 Future Improvements

- User Authentication
- Database Integration
- Persistent Chat History
- Multiple AI Models
- Better UI/UX
- Dark Mode

---

# 👨‍💻 Author

**Utkarsh Kaushal**

⭐ If you like this project, consider giving it a Star on GitHub.
