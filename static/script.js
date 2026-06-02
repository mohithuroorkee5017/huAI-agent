// HARIDWAR UNIVERSITY AI - Modern Dashboard Script
// Fixes: Message required error, Empty response bug, OpenRouter rendering bug
// Features: Typing animation, Auto scroll, Markdown rendering, Sidebar management

let isRecording = false;
let conversationActive = false;

// Initialize on DOM load
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
        messageInput.addEventListener('focus', () => closeSidebarOnMobile());
    }
}

function loadUserInfo() {
    const userDisplay = document.getElementById('userDisplay');
    const userData = localStorage.getItem('user');
    if (userData) {
        try {
            const user = JSON.parse(userData);
            userDisplay.textContent = ?? Lines{user.fullname || user.email};
        } catch (e) {
            userDisplay.textContent = '?? User';
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
            statusBadge.textContent = data.status === 'active' ? '?? Online' : '?? Offline';
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
    if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
        event.preventDefault();
        toggleVoiceInput();
    }
    if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
        event.preventDefault();
        clearConversation();
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const imageInput = document.getElementById('imageInput');
    const message = messageInput.value.trim();
    
    if (!message && imageInput.files.length === 0) {
        console.warn('No message or image provided');
        return;
    }
    
    if (imageInput.files.length > 0) {
        await sendImageMessage();
        return;
    }
    
    addMessage(message, 'user');
    messageInput.value = '';
    conversationActive = true;
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        if (data.success && data.response) {
            const agentResponse = data.response.trim();
            if (agentResponse) {
                addMessage(agentResponse, 'agent');
                scrollToBottom();
                addToConversationHistory(message, agentResponse);
            } else {
                addMessage('I received your message but couldn\\'t generate a proper response. Please try again.', 'agent');
            }
        } else {
            const errorMsg = data.error || data.message || 'Error processing your request. Please try again.';
            addMessage(?? Lines{errorMsg}, 'agent');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addMessage('?? Network error. Please check your connection and try again.', 'agent');
    }
}

async function sendImageMessage() {
    const imageInput = document.getElementById('imageInput');
    const messageInput = document.getElementById('messageInput');
    
    if (!imageInput.files[0]) return;
    
    const file = imageInput.files[0];
    const prompt = messageInput.value.trim() || 'Please analyze this image.';
    
    addMessage(?? Sent image: Lines{file.name}, 'user');
    messageInput.value = '';
    conversationActive = true;
    showTypingIndicator();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('prompt', prompt);
        
        const response = await fetch('/api/image', {method: 'POST', body: formData});
        const data = await response.json();
        hideTypingIndicator();
        
        if (data.success) {
            const agentResponse = data.answer ? data.answer.trim() : 'Image analyzed successfully.';
            addMessage(agentResponse, 'agent');
            scrollToBottom();
            removeImagePreview();
            addToConversationHistory(Image: Lines{file.name}, agentResponse);
        } else {
            addMessage(?? Error analyzing image: Lines{data.error || 'Unknown error'}, 'agent');
        }
    } catch (error) {
        console.error('Error uploading image:', error);
        hideTypingIndicator();
        addMessage('?? Error uploading image. Please try again.', 'agent');
    }
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    const welcomeBanner = messagesContainer.querySelector('.welcome-banner');
    if (welcomeBanner && sender === 'user') welcomeBanner.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = message Lines{sender}-message;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    if (sender === 'agent') {
        bubble.innerHTML = renderMarkdown(text);
    } else {
        bubble.textContent = text;
    }
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(timeDiv);
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function renderMarkdown(text) {
    if (!text || typeof text !== 'string') return text;
    
    let html = text;
    html = html.replace(/\\\(.*?)\n([\s\S]*?)\\\/g, '<pre><code class="code-block">\</code></pre>');
    html = html.replace(/\([^\]+)\/g, '<code class="inline-code">\</code>');
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>\</strong>');
    html = html.replace(/__(.+?)__/g, '<strong>\</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>\</em>');
    html = html.replace(/_(.+?)_/g, '<em>\</em>');
    html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="\" target="_blank">\</a>');
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';
    html = html.replace(/^• (.+)\$/gm, '<li>\</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>\</ul>');
    html = html.replace(/^\d+\. (.+)\$/gm, '<li>\</li>');
    return html;
}

const style = document.createElement('style');
style.textContent = \
    .message-bubble code.code-block { display: block; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 0.9em; margin: 8px 0; }
    .message-bubble code.inline-code { background: rgba(99,102,241,0.2); padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 0.9em; }
    .message-bubble strong { font-weight: 600; color: #fff; }
    .message-bubble em { font-style: italic; opacity: 0.9; }
    .message-bubble a { color: #7dd3fc; text-decoration: underline; }
    .message-bubble a:hover { color: #38bdf8; }
    .message-bubble ul, .message-bubble ol { margin: 8px 0 8px 20px; }
    .message-bubble li { margin: 4px 0; }
    .message-bubble p { margin: 8px 0; }
\;
document.head.appendChild(style);

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'block';
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.style.display = 'none';
}

function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    if (container) {
        setTimeout(() => {
            container.parentElement.scrollTop = container.parentElement.scrollHeight;
        }, 100);
    }
}

function addToConversationHistory(userMsg, agentMsg) {
    const historyList = document.getElementById('conversationHistory');
    if (!historyList) return;
    
    const emptyMsg = historyList.querySelector('.empty-history');
    if (emptyMsg) emptyMsg.remove();
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.textContent = userMsg.substring(0, 40) + (userMsg.length > 40 ? '...' : '');
    historyItem.onclick = () => console.log('Clicked history:', userMsg);
    
    historyList.prepend(historyItem);
}

function sendQuickPrompt(prompt) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = prompt;
    messageInput.focus();
    sendMessage();
}

async function toggleVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    
    if (isRecording) {
        isRecording = false;
        voiceBtn.style.opacity = '1';
        return;
    }
    
    isRecording = true;
    voiceBtn.style.opacity = '0.5';
    voiceBtn.innerHTML = '<span>??</span>';
    
    try {
        const response = await fetch('/api/voice-input', {method: 'POST'});
        const data = await response.json();
        
        if (data.success && data.heard) {
            document.getElementById('messageInput').value = data.heard;
            sendMessage();
        } else {
            addMessage('?? Voice input failed. Please try again.', 'agent');
        }
    } catch (error) {
        console.error('Voice input error:', error);
        addMessage('?? Voice input error. Please try again.', 'agent');
    } finally {
        isRecording = false;
        voiceBtn.style.opacity = '1';
        voiceBtn.innerHTML = '<span>??</span>';
    }
}

function handleImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const maxSize = 20 * 1024 * 1024;
    if (file.size > maxSize) {
        addMessage('?? Image too large. Maximum size is 20MB.', 'agent');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImage');
        if (previewImg && previewContainer) {
            previewImg.src = e.target.result;
            previewContainer.style.display = 'block';
        }
    };
    reader.readAsDataURL(file);
}

function removeImagePreview() {
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('imagePreview');
    if (imageInput) imageInput.value = '';
    if (previewContainer) previewContainer.style.display = 'none';
}

async function clearConversation() {
    if (!confirm('Clear all conversations?')) return;
    
    try {
        const response = await fetch('/api/clear-history', {method: 'POST'});
        if (response.ok) {
            const messagesContainer = document.getElementById('messagesContainer');
            if (messagesContainer) {
                messagesContainer.innerHTML = '';
                showWelcomeBanner();
            }
            conversationActive = false;
        }
    } catch (error) {
        console.error('Clear history error:', error);
        addMessage('?? Error clearing history.', 'agent');
    }
}

function startNewConversation() {
    clearConversation();
}

function showWelcomeBanner() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    const banner = document.createElement('div');
    banner.className = 'welcome-banner';
    banner.innerHTML = \
        <h2>Welcome to HU Voice AI! ??</h2>
        <p>Ask me anything about Haridwar University, courses, admissions, or general topics.</p>
        <div class="quick-prompts">
            <button class="prompt-btn" onclick="sendQuickPrompt('What are the courses offered by Haridwar University?')">?? Courses</button>
            <button class="prompt-btn" onclick="sendQuickPrompt('How do I apply for admission?')">?? Admission</button>
            <button class="prompt-btn" onclick="sendQuickPrompt('Tell me about campus facilities')">?? Campus</button>
        </div>
    \;
    messagesContainer.appendChild(banner);
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.toggle('active');
}

function closeSidebarOnMobile() {
    if (window.innerWidth <= 768) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) sidebar.classList.remove('active');
    }
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        fetch('/api/logout', {method: 'POST'})
            .then(() => {
                localStorage.removeItem('user');
                window.location.href = '/';
            })
            .catch(error => console.error('Logout error:', error));
    }
}

document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768) {
        const sidebar = document.querySelector('.sidebar');
        const toggle = document.querySelector('.mobile-sidebar-toggle');
        if (sidebar && !sidebar.contains(event.target) && toggle && !toggle.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    }
});
