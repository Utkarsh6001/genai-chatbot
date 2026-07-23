const BACKEND_URL = 'https://genai-chatbot-1kng.onrender.com';

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, 'user');
    userInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send message to backend
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response to chat
        if (data.message) {
            addMessageToChat(data.message, 'bot');
        } else if (data.error) {
            addMessageToChat('Error: ' + data.error, 'bot');
        }

    } catch (error) {
        removeTypingIndicator();
        addMessageToChat('Connection error. Make sure backend is running on port 5000.', 'bot');
        console.error('Error:', error);
    }
}

function addMessageToChat(text, sender) {
    const chatWindow = document.getElementById('chatWindow');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const textDiv = document.createElement('div');
    textDiv.className = 'text';
    textDiv.textContent = text;

    messageDiv.appendChild(textDiv);
    chatWindow.appendChild(messageDiv);

    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showTypingIndicator() {
    const chatWindow = document.getElementById('chatWindow');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'typingIndicator';

    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';

    messageDiv.appendChild(typingDiv);
    chatWindow.appendChild(messageDiv);

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

async function clearChat() {
    try {
        await fetch(`${BACKEND_URL}/api/clear`, { method: 'POST' });

        const chatWindow = document.getElementById('chatWindow');
        chatWindow.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome! 👋</h2>
                <p>Start chatting with our AI assistant</p>
            </div>
        `;
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}