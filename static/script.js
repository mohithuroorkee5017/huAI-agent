// HARIDWAR UNIVERSITY AI - Modern Dashboard Script

let isRecording = false;
let conversationActive = false;

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserInfo();
    updateStatus();
    setInterval(updateStatus, 5000);
});

function initializeApp() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer && !messagesContainer.querySelector('.welcome-banner')) {
        showWelcomeBanner();
    }
}

function setupEventListeners() {
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keypress', handleInputKeyPress);
    }
}

function loadUserInfo() {
    const userDisplay = document.getElementById('userDisplay');
    const userData = localStorage.getItem('user');
    if (userData) {
        try {
            const user = JSON.parse(userData);
            userDisplay.textContent = '👤 ' + (user.fullname || user.email);
        } catch (e) {
            userDisplay.textContent = '👤 User';
        }
    }
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        if (!response.ok) throw new Error('Status check failed');
        const data = await response.json();
        const statusBadge = document.getElementById('statusBadge');
        if (statusBadge) {
            statusBadge.textContent = data.status === 'active' ? '🟢 Online' : '🔴 Offline';
        }
    } catch (error) {
        console.error('Status update failed:', error);
    }
}

function handleInputKeyPress(event) {
    if (event.key === 'Enter') {
        if (event.shiftKey) return true;
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const imageInput = document.getElementById('imageInput');
    const message = messageInput.value.trim();
    
    if (!message && imageInput.files.length === 0) {
        return;
    }
    
    addMessage(message, 'user');
    messageInput.value = '';
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        const agentResponse = (data.response || data.answer || '').trim();
        
        if (agentResponse) {
            addMessage(agentResponse, 'agent');
            scrollToBottom();
        } else {
            addMessage('Unable to process your request. Please try again.', 'agent');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addMessage('Network error. Please check your connection.', 'agent');
    }
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    const welcomeBanner = messagesContainer.querySelector('.welcome-banner');
    if (welcomeBanner && sender === 'user') welcomeBanner.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender + '-message';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'block';
    }
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

function clearConversation() {
    if (!confirm('Clear all conversations?')) return;
    fetch('/api/clear-history', {method: 'POST'}).then(() => {
        const messagesContainer = document.getElementById('messagesContainer');
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
            showWelcomeBanner();
        }
    });
}

function startNewConversation() {
    clearConversation();
}

function showWelcomeBanner() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    const banner = document.createElement('div');
    banner.className = 'welcome-banner';
    banner.innerHTML = '<h2>Welcome to HU Voice AI! 👋</h2><p>Ask me anything about Haridwar University, courses, admissions, or general topics.</p>';
    
    messagesContainer.appendChild(banner);
}

function sendQuickPrompt(prompt) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = prompt;
    sendMessage();
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

function closeSidebarOnMobile() {
    if (window.innerWidth < 768) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.remove('active');
        }
    }
}

function handleLogout() {
    if (!confirm('Logout?')) return;
    fetch('/api/logout', {method: 'POST'}).then(() => {
        window.location.href = '/';
    });
}

function toggleVoiceInput() {
    console.log('Voice input not available');
}

function handleImageSelect(event) {
    console.log('Image upload not available in web');
}

function removeImagePreview() {
    const imagePreview = document.getElementById('imagePreview');
    if (imagePreview) imagePreview.style.display = 'none';
}
