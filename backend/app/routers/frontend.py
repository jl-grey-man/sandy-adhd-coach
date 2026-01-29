from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# We'll serve HTML directly for now
@router.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Serve the chat interface"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADHD Coach</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial Black', 'Arial Bold', Gadget, sans-serif;
            background: #E8DCC4;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 80px;
            margin: 0;
        }
        
        .container {
            width: calc(100vw - 160px);
            height: calc(100vh - 160px);
            max-width: 1000px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        /* Login Screen */
        .login-screen {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .login-screen h1 {
            font-size: 72px;
            font-weight: 900;
            color: #0a0a0a;
            margin-bottom: 10px;
            letter-spacing: -4px;
            text-transform: uppercase;
        }
        
        .accent-dots {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 40px;
        }
        
        .accent-dot {
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }
        
        .dot-orange { background: #E84A27; }
        .dot-blue { background: #7BB5C1; }
        .dot-yellow { background: #F2B134; }
        
        .login-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 40px;
        }
        
        .login-form input {
            padding: 15px 20px;
            border: 2px solid #E8DCC4;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .login-form input:focus {
            outline: none;
            border-color: #E84A27;
        }
        
        .login-form button {
            padding: 15px;
            background: #E84A27;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .login-form button:hover {
            background: #d43d1a;
        }
        
        .error-message {
            color: #E84A27;
            font-size: 14px;
            margin-top: 10px;
        }
        
        /* Chat Screen */
        .chat-screen {
            background: #2a2a2a;
            border-radius: 0;
            border: none;
            overflow: hidden;
            height: 100%;
            width: 100%;
            display: none;
            flex-direction: column;
            position: relative;
        }
        
        .chat-screen.active {
            display: flex;
        }
        
        /* Grungy texture overlay */
        .chat-screen::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 0, 0, 0.03) 2px,
                    rgba(0, 0, 0, 0.03) 4px
                ),
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 0, 0, 0.03) 2px,
                    rgba(0, 0, 0, 0.03) 4px
                );
            opacity: 0.4;
            pointer-events: none;
            z-index: 1;
        }
        
        .chat-screen > * {
            position: relative;
            z-index: 2;
        }
        
        .chat-header {
            background: #1a1a1a;
            color: white;
            padding: 40px 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 8px solid #E84A27;
            position: relative;
        }
        
        .chat-header h2 {
            font-size: 48px;
            font-weight: 900;
            display: flex;
            align-items: center;
            gap: 20px;
            letter-spacing: -2px;
            text-transform: uppercase;
            position: relative;
            z-index: 1;
        }
        
        .header-dot {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #F2B134;
        }
        
        .logout-btn {
            background: none;
            border: 3px solid white;
            color: white;
            padding: 12px 24px;
            border-radius: 0;
            cursor: pointer;
            font-size: 16px;
            font-weight: 900;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }
        
        .logout-btn:hover {
            background: white;
            color: #0a0a0a;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 60px;
            display: flex;
            flex-direction: column;
            gap: 40px;
            background: #2a2a2a;
        }
        
        .message {
            display: flex;
            gap: 20px;
            max-width: 80%;
            animation: slideIn 0.3s ease-out;
            position: relative;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            margin-left: auto;
            flex-direction: row-reverse;
        }
        
        .message-content {
            padding: 30px 40px;
            border-radius: 0;
            line-height: 1.8;
            font-size: 16px;
            font-weight: 400;
            position: relative;
        }
        
        /* Add formatting support */
        .message-content p {
            margin: 0 0 16px 0;
            line-height: 1.7;
        }
        
        .message-content p:last-child {
            margin-bottom: 0;
        }
        
        .message-content strong {
            font-weight: 700;
        }
        
        .message-content ul, .message-content ol {
            margin: 16px 0;
            padding-left: 25px;
        }
        
        .message-content li {
            margin: 8px 0;
            line-height: 1.6;
        }
        
        .message.user .message-content {
            background: #3a3a3a;
            color: white;
            border: none;
        }
        
        .message.ai .message-content {
            background: #3a3a3a;
            color: white;
            border: none;
        }
        
        .thinking-indicator {
            display: none;
            width: 60px;
            height: 60px;
            flex-shrink: 0;
        }
        
        .thinking-indicator.active {
            display: block;
        }
        
        /* Pulsating concentric circles */
        .circles-container {
            position: relative;
            width: 60px;
            height: 60px;
            margin: 0;
        }
        
        .circle {
            position: absolute;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: pulse 2s ease-out infinite;
        }
        
        .circle:nth-child(1) {
            width: 15px;
            height: 15px;
            background: #E84A27;
            animation-delay: 0s;
        }
        
        .circle:nth-child(2) {
            width: 30px;
            height: 30px;
            border: 2px solid #E84A27;
            animation-delay: 0.3s;
        }
        
        .circle:nth-child(3) {
            width: 45px;
            height: 45px;
            border: 2px solid #F2B134;
            animation-delay: 0.6s;
        }
        
        .circle:nth-child(4) {
            width: 60px;
            height: 60px;
            border: 2px solid #E8DCC4;
            animation-delay: 0.9s;
        }
        
        @keyframes pulse {
            0% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            100% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(1.5);
            }
        }
        
        .chat-input {
            padding: 40px 60px;
            border-top: 8px solid #F2B134;
            display: flex;
            gap: 20px;
            align-items: center;
            background: #1a1a1a;
        }
        
        .chat-input input {
            flex: 1;
            padding: 20px 30px;
            border: 3px solid #3a3a3a;
            border-radius: 0;
            font-size: 20px;
            font-weight: 700;
            transition: border-color 0.3s;
            background: #2a2a2a;
            color: #E8DCC4;
        }
        
        .chat-input input:focus {
            outline: none;
            border-color: #7BB5C1;
        }
        
        .chat-input input::placeholder {
            color: #666;
            font-weight: 700;
        }
        
        .send-btn {
            padding: 20px 50px;
            background: #F2B134;
            color: #1a1a1a;
            border: none;
            border-radius: 0;
            font-size: 20px;
            font-weight: 900;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .send-btn:hover:not(:disabled) {
            background: #E84A27;
            color: white;
            transform: scale(1.05);
        }
        
        .send-btn:disabled {
            background: #333;
            color: #666;
            cursor: not-allowed;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Loading spinner */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(242, 177, 52, 0.2);
            border-top-color: #F2B134;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        /* Circular progress */
        .progress-circle {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 10px;
            vertical-align: middle;
            position: relative;
        }
        
        .progress-circle svg {
            transform: rotate(-90deg);
        }
        
        .progress-circle circle {
            fill: none;
            stroke-width: 3;
        }
        
        .progress-bg {
            stroke: rgba(242, 177, 52, 0.2);
        }
        
        .progress-bar {
            stroke: #F2B134;
            stroke-linecap: round;
            transition: stroke-dashoffset 0.3s;
        }
        
        .hidden {
            display: none !important;
        }
        
        /* Prompt Editor Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal-overlay.active {
            display: flex;
        }
        
        .modal-content {
            background: #2a2a2a;
            border: 4px solid #F2B134;
            padding: 40px;
            max-width: 800px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-content h3 {
            color: #E8DCC4;
            font-size: 32px;
            font-weight: 900;
            margin: 0 0 20px 0;
            text-transform: uppercase;
        }
        
        .modal-content textarea {
            width: 100%;
            min-height: 400px;
            background: #1a1a1a;
            border: 2px solid #3a3a3a;
            color: white;
            padding: 20px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            resize: vertical;
        }
        
        .modal-buttons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        .modal-buttons button {
            flex: 1;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 900;
            cursor: pointer;
            border: none;
            text-transform: uppercase;
        }
        
        .btn-save {
            background: #E84A27;
            color: white;
        }
        
        .btn-cancel {
            background: #3a3a3a;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Login Screen -->
        <div class="login-screen" id="loginScreen">
            <h1>ADHD Coach</h1>
            <div class="accent-dots">
                <div class="accent-dot dot-orange"></div>
                <div class="accent-dot dot-blue"></div>
                <div class="accent-dot dot-yellow"></div>
            </div>
            <p style="color: #666; font-size: 18px;">Your adaptive work companion</p>
            
            <form class="login-form" id="loginForm">
                <input type="email" id="email" placeholder="Email" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Get Started</button>
                <div class="error-message" id="loginError"></div>
            </form>
        </div>
        
        <!-- Chat Screen -->
        <div class="chat-screen" id="chatScreen">
            <div class="chat-header">
                <h2>
                    <span class="header-dot"></span>
                    ADHD Coach
                </h2>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <label for="fileUpload" class="logout-btn" style="background: none; border: 2px solid #7BB5C1; color: #7BB5C1; cursor: pointer; margin: 0;">
                        Upload Doc
                    </label>
                    <input type="file" id="fileUpload" style="display: none;" accept=".pdf,.doc,.docx,.txt,.md" onchange="handleFileUpload(event)">
                    <button class="logout-btn" onclick="showUrlDialog()" style="background: none; border: 2px solid #7BB5C1; color: #7BB5C1;">
                        Add URL
                    </button>
                    <button class="logout-btn" onclick="showPromptEditor()" style="background: none; border: 2px solid #F2B134; color: #F2B134;">
                        Edit Prompt
                    </button>
                    <button class="logout-btn" onclick="clearSession()" style="background: none; border: 2px solid #F2B134; color: #F2B134;">New Topic</button>
                    <button class="logout-btn" onclick="logout()">Logout</button>
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message ai">
                    <div class="message-content">
                        Hey! I'm here to help you work with your ADHD brain, not against it. What's on your mind today?
                    </div>
                </div>
            </div>
            
            <div class="chat-input">
                <div class="thinking-indicator" id="thinkingIndicator">
                    <div class="circles-container">
                        <div class="circle"></div>
                        <div class="circle"></div>
                        <div class="circle"></div>
                        <div class="circle"></div>
                    </div>
                </div>
                <input type="text" id="messageInput" placeholder="Type your message..." autocomplete="off">
                <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    
    <script>
        let authToken = null;
        let sessionId = null;
        
        // Generate or retrieve session ID
        function getSessionId() {
            let sid = localStorage.getItem('adhd_coach_session_id');
            if (!sid) {
                sid = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('adhd_coach_session_id', sid);
            }
            return sid;
        }
        
        // Clear session (for testing or "New Topic" feature)
        function clearSession() {
            localStorage.removeItem('adhd_coach_session_id');
            sessionId = getSessionId();
            document.getElementById('chatMessages').innerHTML = `
                <div class="message ai">
                    <div class="message-content">
                        Hey! I'm here to help you work with your ADHD brain, not against it. What's on your mind today?
                    </div>
                </div>
            `;
        }
        
        // Auto-login on page load
        window.addEventListener('DOMContentLoaded', async () => {
            sessionId = getSessionId();
            console.log('DOM loaded, starting auto-login...');
            autoLogin();
        });
        
        async function autoLogin() {
            console.log('Auto-login function called');
            const errorEl = document.getElementById('loginError');
            
            try {
                console.log('Attempting login...');
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        email: 'user@example.com', 
                        password: 'string' 
                    })
                });
                
                console.log('Login response:', response.ok);
                
                if (response.ok) {
                    const data = await response.json();
                    authToken = data.token;
                    console.log('Token received, switching to chat screen');
                    
                    // Switch to chat screen
                    const loginScreen = document.getElementById('loginScreen');
                    const chatScreen = document.getElementById('chatScreen');
                    
                    loginScreen.classList.add('hidden');
                    chatScreen.classList.add('active');
                    
                    console.log('Chat screen should be visible now');
                } else {
                    // If auto-login fails, show login form
                    console.log('Auto-login failed, showing login form');
                }
            } catch (err) {
                console.log('Auto-login error:', err);
            }
        }
        
        // Manual login form handler (if auto-login fails)
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorEl = document.getElementById('loginError');
            
            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    authToken = data.token;
                    
                    // Switch to chat screen
                    document.getElementById('loginScreen').classList.add('hidden');
                    document.getElementById('chatScreen').classList.add('active');
                    errorEl.textContent = '';
                } else {
                    const error = await response.json();
                    errorEl.textContent = error.detail || 'Login failed. Please try again.';
                }
            } catch (err) {
                errorEl.textContent = 'Connection error. Please try again.';
            }
        });
        
        // Send message
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            // Disable send button and show thinking
            const sendBtn = document.getElementById('sendBtn');
            sendBtn.disabled = true;
            document.getElementById('thinkingIndicator').classList.add('active');
            
            try {
                const response = await fetch('/chat/message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({ 
                        message, 
                        session_id: sessionId,
                        context: {} 
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    addMessage(data.ai_response, 'ai');
                } else {
                    addMessage('Sorry, I had trouble processing that. Please try again.', 'ai');
                }
            } catch (err) {
                addMessage('Connection error. Please check your internet and try again.', 'ai');
            } finally {
                sendBtn.disabled = false;
                document.getElementById('thinkingIndicator').classList.remove('active');
            }
        }
        
        // Add message to chat with markdown formatting
        function addMessage(text, type) {
            const messagesEl = document.getElementById('chatMessages');
            const messageEl = document.createElement('div');
            messageEl.className = 'message ' + type;
            
            // Simple markdown parsing for AI messages
            let formattedText = text;
            if (type === 'ai') {
                // Convert **bold** to <strong> using string operations
                while (formattedText.indexOf('**') !== -1) {
                    formattedText = formattedText.replace('**', '<strong>').replace('**', '</strong>');
                }
                
                // Split by double line breaks for paragraphs
                const paragraphs = formattedText.split('\\n\\n');
                const processedParagraphs = [];
                
                for (let i = 0; i < paragraphs.length; i++) {
                    const para = paragraphs[i].trim();
                    if (para === '') continue;
                    
                    // Check if it's a bullet list
                    const lines = para.split('\\n');
                    const isList = lines.every(line => line.trim().startsWith('- ') || line.trim() === '');
                    
                    if (isList) {
                        processedParagraphs.push('<ul>');
                        lines.forEach(line => {
                            if (line.trim().startsWith('- ')) {
                                processedParagraphs.push('<li>' + line.substring(2).trim() + '</li>');
                            }
                        });
                        processedParagraphs.push('</ul>');
                    } else {
                        processedParagraphs.push('<p>' + para.replace(/\\n/g, ' ') + '</p>');
                    }
                }
                
                formattedText = processedParagraphs.join('');
            }
            
            messageEl.innerHTML = '<div class="message-content">' + formattedText + '</div>';
            messagesEl.appendChild(messageEl);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }
        
        // Logout
        function logout() {
            authToken = null;
            document.getElementById('chatScreen').classList.remove('active');
            document.getElementById('loginScreen').classList.remove('hidden');
            document.getElementById('chatMessages').innerHTML = `
                <div class="message ai">
                    <div class="message-content">
                        Hey! I'm here to help you work with your ADHD brain, not against it. What's on your mind today?
                    </div>
                </div>
            `;
        }
        
        // Enter key to send
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !document.getElementById('sendBtn').disabled) {
                sendMessage();
            }
        });
        
        // File upload handler
        async function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            // Show uploading message with progress
            const messagesEl = document.getElementById('chatMessages');
            const uploadMsg = document.createElement('div');
            uploadMsg.className = 'message user';
            
            const progressHtml = '<svg width="20" height="20"><circle class="progress-bg" cx="10" cy="10" r="8"/><circle class="progress-bar" cx="10" cy="10" r="8" stroke-dasharray="50.27" stroke-dashoffset="50.27" id="progressCircle"/></svg>';
            uploadMsg.innerHTML = '<div class="message-content"><span class="progress-circle">' + progressHtml + '</span>Uploading ' + file.name + '...</div>';
            messagesEl.appendChild(uploadMsg);
            messagesEl.scrollTop = messagesEl.scrollHeight;
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                // Use XMLHttpRequest for progress tracking
                const xhr = new XMLHttpRequest();
                
                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        const percent = (e.loaded / e.total) * 100;
                        const circle = document.getElementById('progressCircle');
                        if (circle) {
                            const offset = 50.27 - (50.27 * percent / 100);
                            circle.style.strokeDashoffset = offset;
                        }
                    }
                });
                
                xhr.open('POST', '/chat/upload-document');
                xhr.setRequestHeader('Authorization', 'Bearer ' + authToken);
                
                xhr.onload = function() {
                    uploadMsg.remove();
                    
                    if (xhr.status === 200) {
                        const data = JSON.parse(xhr.responseText);
                        addMessage(data.message || '✓ Document uploaded!', 'ai');
                    } else {
                        const error = JSON.parse(xhr.responseText);
                        addMessage('✗ Failed: ' + (error.detail || 'Unknown error'), 'ai');
                    }
                };
                
                xhr.onerror = function() {
                    uploadMsg.remove();
                    addMessage('✗ Upload error', 'ai');
                };
                
                xhr.send(formData);
                
            } catch (err) {
                uploadMsg.remove();
                addMessage('✗ Upload error: ' + err.message, 'ai');
            }
            
            // Reset file input
            event.target.value = '';
        }
        
        // URL dialog handler
        function showUrlDialog() {
            const url = prompt('Enter URL (article, research paper, webpage):');
            if (!url || !url.trim()) return;
            
            handleUrlUpload(url.trim());
        }
        
        // URL upload handler
        async function handleUrlUpload(url) {
            // Validate URL format
            try {
                new URL(url);
            } catch {
                addMessage('Invalid URL format. Please try again.', 'ai');
                return;
            }
            
            // Show processing message with spinner
            const messagesEl = document.getElementById('chatMessages');
            const uploadMsg = document.createElement('div');
            uploadMsg.className = 'message user';
            
            const progressHtml = '<svg width="20" height="20"><circle class="progress-bg" cx="10" cy="10" r="8"/><circle class="progress-bar" cx="10" cy="10" r="8" stroke-dasharray="50.27" stroke-dashoffset="25" style="animation: spin 1.5s linear infinite;"/></svg>';
            uploadMsg.innerHTML = '<div class="message-content"><span class="progress-circle">' + progressHtml + '</span>Loading URL content...</div>';
            messagesEl.appendChild(uploadMsg);
            messagesEl.scrollTop = messagesEl.scrollHeight;
            
            try {
                const response = await fetch('/chat/upload-url', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ url })
                });
                
                // Remove spinner message
                uploadMsg.remove();
                
                if (response.ok) {
                    const data = await response.json();
                    addMessage(data.message || '✓ URL content loaded!', 'ai');
                } else {
                    const error = await response.json();
                    addMessage('✗ Failed: ' + (error.detail || 'Could not fetch URL'), 'ai');
                }
            } catch (err) {
                uploadMsg.remove();
                addMessage('✗ Error: ' + err.message, 'ai');
            }
        }
        
        // Prompt Editor
        async function showPromptEditor() {
            const modal = document.getElementById('promptModal');
            const textarea = document.getElementById('promptText');
            
            // Fetch current prompt
            try {
                const response = await fetch('/chat/get-prompt', {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    textarea.value = data.prompt;
                    modal.classList.add('active');
                } else {
                    addMessage('Failed to load prompt. Please try again.', 'ai');
                }
            } catch (err) {
                addMessage('Error loading prompt.', 'ai');
            }
        }
        
        function closePromptEditor() {
            document.getElementById('promptModal').classList.remove('active');
        }
        
        async function savePrompt() {
            const textarea = document.getElementById('promptText');
            const newPrompt = textarea.value;
            
            try {
                const response = await fetch('/chat/update-prompt', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: newPrompt })
                });
                
                if (response.ok) {
                    closePromptEditor();
                    addMessage('✓ System prompt updated!', 'ai');
                } else {
                    addMessage('Failed to save prompt. Please try again.', 'ai');
                }
            } catch (err) {
                addMessage('Error saving prompt.', 'ai');
            }
        }
    </script>
    
    <!-- Prompt Editor Modal -->
    <div class="modal-overlay" id="promptModal">
        <div class="modal-content">
            <h3>AI System Prompt</h3>
            <textarea id="promptText" placeholder="Loading..."></textarea>
            <div class="modal-buttons">
                <button class="btn-save" onclick="savePrompt()">Save</button>
                <button class="btn-cancel" onclick="closePromptEditor()">Cancel</button>
            </div>
        </div>
    </div>
    
</body>
</html>
    """
    
    return html_content
