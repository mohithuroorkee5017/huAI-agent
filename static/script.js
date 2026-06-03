/* ========================================================================
   HARIDWAR UNIVERSITY AI - MOBILE RESPONSIVE SCRIPT
   ========================================================================
   Updates for new mobile-responsive HTML structure:
   - Element ID mappings updated
   - Keyboard handling improved
   - Mobile viewport management
   - Focus management for accessibility
   ======================================================================== */

// Global state
let isRecording = false;
let isLoading = false;

/* ========================================================================
   INITIALIZATION
   ======================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎤 Initializing HU Voice AI...');
    
    // Setup event listeners
    setupInputListener();
    
    // Update status
    updateStatus();
    updateStatusPeriodically();
    
    // Handle viewport changes
    setupViewportHandlers();
    
    // Prevent pinch zoom on mobile
    preventPinchZoom();
    
    console.log('✅ Initialization complete');
});

/* ========================================================================
   INPUT & MESSAGE HANDLING
   ======================================================================== */

function setupInputListener() {
    const input = document.getElementById('questionInput');
    if (!input) return;
    
    // Handle Enter key
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submitQuestion();
        }
    });
    
    // Ensure input is accessible when focused
    input.addEventListener('focus', function() {
        // On mobile, scroll the input into view
        setTimeout(() => {
            this.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);
    });
}

function submitQuestion() {
    const input = document.getElementById('questionInput');
    if (!input) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    // Prevent duplicate submissions
    if (isLoading) return;
    
    isLoading = true;
    
    // Add user message to conversation
    addMessageToConversation(message, 'user');
    
    // Clear input
    input.value = '';
    
    // Blur input to hide mobile keyboard
    input.blur();
    
    // Show loading state
    showLoadingIndicator();
    
    // Send to backend
    sendMessageToBackend(message);
}

async function sendMessageToBackend(message) {
    try {
        console.log('📤 Sending message:', message.substring(0, 50) + '...');
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_id: 'web_user'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📥 Response received');
        
        // Extract answer from response
        const answer = data.answer || data.response || 'Unable to process your request.';
        
        // Add agent message
        addMessageToConversation(answer, 'agent');
        
        // Scroll to latest message
        scrollConversationToBottom();
        
    } catch (error) {
        console.error('❌ Error sending message:', error);
        
        // Add error message
        const errorMsg = 'Sorry, I encountered an error. Please check your connection and try again.';
        addMessageToConversation(errorMsg, 'agent');
        scrollConversationToBottom();
        
    } finally {
        hideLoadingIndicator();
        isLoading = false;
        
        // Re-focus input for continued interaction
        const input = document.getElementById('questionInput');
        if (input) input.focus();
    }
}

function addMessageToConversation(text, sender) {
    const conversation = document.getElementById('conversation');
    if (!conversation) return;
    
    // Remove welcome message on first user message
    if (sender === 'user') {
        const welcome = conversation.querySelector('.welcome-message');
        if (welcome) welcome.remove();
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    
    messageDiv.appendChild(bubble);
    conversation.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollConversationToBottom();
}

function scrollConversationToBottom() {
    const conversation = document.getElementById('conversation');
    if (conversation) {
        // Use setTimeout to ensure DOM has updated
        setTimeout(() => {
            conversation.scrollTop = conversation.scrollHeight;
        }, 0);
    }
}

/* ========================================================================
   UI VISIBILITY & FEEDBACK
   ======================================================================== */

function showLoadingIndicator() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.style.display = 'flex';
    }
}

function hideLoadingIndicator() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.style.display = 'none';
    }
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            const badge = document.getElementById('status');
            if (badge) {
                badge.textContent = data.status === 'active' 
                    ? '🟢 Online' 
                    : '🔴 Offline';
            }
        }
    } catch (error) {
        console.warn('⚠️ Status check failed:', error);
    }
}

function updateStatusPeriodically() {
    // Update status every 30 seconds
    setInterval(updateStatus, 30000);
}

/* ========================================================================
   VOICE INPUT HANDLING
   ======================================================================== */

function toggleVoiceInput() {
    if (isRecording) {
        stopVoiceRecording();
    } else {
        startVoiceRecording();
    }
}

function startVoiceRecording() {
    console.log('🎤 Voice recording requested...');
    
    // Check browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Speech Recognition not supported in your browser');
        return;
    }
    
    isRecording = true;
    const btn = document.getElementById('voiceBtn');
    if (btn) {
        btn.classList.add('recording');
        btn.textContent = '⏹️ Stop Recording';
    }
    
    console.log('🎙️ Voice recording started');
    // Additional voice recording logic would go here
}

function stopVoiceRecording() {
    console.log('⏹️ Voice recording stopped');
    isRecording = false;
    
    const btn = document.getElementById('voiceBtn');
    if (btn) {
        btn.classList.remove('recording');
        btn.textContent = '🎤 Voice';
    }
}

/* ========================================================================
   TEXT INPUT FOCUS
   ======================================================================== */

function focusTextInput() {
    const input = document.getElementById('questionInput');
    if (input) {
        input.focus();
        // On mobile, this will trigger keyboard opening
        // The footer is sticky so it will stay above the keyboard
    }
}

/* ========================================================================
   CONVERSATION MANAGEMENT
   ======================================================================== */

function clearConversation() {
    if (!confirm('Clear all conversations? This cannot be undone.')) {
        return;
    }
    
    console.log('🗑️ Clearing conversation history...');
    
    const conversation = document.getElementById('conversation');
    if (conversation) {
        conversation.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome to HU Voice AI! 👋</h2>
                <p>I'm your intelligent university assistant. Ask me anything about:</p>
                <ul class="welcome-topics">
                    <li>📚 Courses & Admissions</li>
                    <li>🏫 Campus Information</li>
                    <li>🎓 Career Guidance</li>
                    <li>💡 General Knowledge</li>
                </ul>
                <p class="welcome-hint">Use voice or text input below to get started!</p>
            </div>
        `;
    }
    
    // Clear transcript
    const transcript = document.getElementById('transcript');
    if (transcript) {
        transcript.innerHTML = '<p class="transcript-empty">📝 No transcripts yet...</p>';
    }
    
    console.log('✅ Conversation cleared');
}

/* ========================================================================
   VIEWPORT & MOBILE HANDLING
   ======================================================================== */

function setupViewportHandlers() {
    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
        console.log('📱 Orientation changed to:', window.orientation);
        // Allow time for DOM to adjust
        setTimeout(() => {
            const input = document.getElementById('questionInput');
            if (input) input.focus();
        }, 200);
    });
    
    // Handle resize
    window.addEventListener('resize', () => {
        // Scroll footer into view when keyboard opens
        const footer = document.querySelector('.app-footer');
        if (footer && window.innerHeight < window.screen.height) {
            // Keyboard is likely open
            footer.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    });
}

function preventPinchZoom() {
    // Prevent pinch zoom on mobile (better for fixed layouts)
    document.addEventListener('touchmove', function(event) {
        if (event.touches.length > 1) {
            event.preventDefault();
        }
    }, false);
}

/* ========================================================================
   KEYBOARD MANAGEMENT
   ======================================================================== */

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift+Enter: new line (allow default)
            return;
        }
        // Enter alone: send message
        event.preventDefault();
        submitQuestion();
    }
}

/* ========================================================================
   MOBILE KEYBOARD DETECTION
   ========================================================================
   Detects when mobile keyboard opens/closes
   ======================================================================== */

const originalHeight = window.innerHeight;

window.addEventListener('resize', () => {
    const currentHeight = window.innerHeight;
    
    // If height decreased significantly, keyboard is likely open
    if (currentHeight < originalHeight - 100) {
        console.log('⌨️ Keyboard appears to be open');
        // Ensure footer stays visible
        const footer = document.querySelector('.app-footer');
        if (footer) {
            // Small delay to let browser finish layout
            setTimeout(() => {
                footer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }
    }
});

/* ========================================================================
   ACCESSIBILITY HELPERS
   ======================================================================== */

// Add aria-labels for better screen reader support
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('questionInput');
    if (input && !input.getAttribute('aria-label')) {
        input.setAttribute('aria-label', 'Message input field');
    }
    
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn && !submitBtn.getAttribute('aria-label')) {
        submitBtn.setAttribute('aria-label', 'Send message');
    }
    
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn && !voiceBtn.getAttribute('aria-label')) {
        voiceBtn.setAttribute('aria-label', 'Voice input');
    }
    
    const textBtn = document.getElementById('textBtn');
    if (textBtn && !textBtn.getAttribute('aria-label')) {
        textBtn.setAttribute('aria-label', 'Text input');
    }
});

/* ========================================================================
   DEBUG LOGGING
   ======================================================================== */

console.log('%c🎤 HU Voice AI - Mobile Responsive', 'color: #6366f1; font-size: 14px; font-weight: bold;');
console.log('%cViewport Height: ' + window.innerHeight, 'color: #8b5cf6');
console.log('%cViewport Width: ' + window.innerWidth, 'color: #8b5cf6');
console.log('%cDevice Pixel Ratio: ' + window.devicePixelRatio, 'color: #8b5cf6');

