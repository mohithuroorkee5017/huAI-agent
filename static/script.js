/* ========================================================================
   HARIDWAR UNIVERSITY AI - COMPREHENSIVE SCRIPT WITH ALL FIXES
   ========================================================================
   IMPROVEMENTS:
   ✓ Toast notifications for errors, success, and info messages
   ✓ Chat history persistence to localStorage
   ✓ Retry logic with exponential backoff
   ✓ Timeout handling for API calls
   ✓ Enhanced error logging and debugging
   ✓ Loading states with visual feedback
   ✓ Input validation and sanitization
   ✓ Conversation ID management for chat history
   ✓ Mobile keyboard detection and handling
   ✓ Accessibility features (aria-labels)
   ========================================================================
   DEBUG LOGGING: All operations logged with prefixes:
   📤 = Sending data
   📥 = Receiving data
   ✅ = Success
   ❌ = Error
   ⚠️  = Warning
   ⌨️  = Keyboard
   🎤 = Voice/Recording
   🗑️  = Clear/Delete
   💾 = Storage
   🔄 = Retry
   ======================================================================== */

/* ========================================================================
   GLOBAL STATE & CONFIGURATION
   ======================================================================== */

const CONFIG = {
    // Use current origin + /api for API calls (supports both unified and separate servers)
    API_BASE_URL: `${window.location.protocol}//${window.location.host}/api`,
    API_TIMEOUT: 30000,  // 30 seconds
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,   // 1 second base delay
    TOAST_TIMEOUT: 5000, // 5 seconds
    KEYBOARD_DETECTION_THRESHOLD: 100,  // pixels
    STATUS_UPDATE_INTERVAL: 30000,  // 30 seconds
    CHAT_HISTORY_KEY: 'hu_voice_ai_chat_history',
    CONVERSATION_ID_KEY: 'hu_voice_ai_conversation_id'
};

// Global application state
const AppState = {
    isRecording: false,
    isLoading: false,
    conversationId: null,
    messageHistory: [],
    originalViewportHeight: window.innerHeight,
    currentRetryCount: 0,
    lastError: null
};

/* ========================================================================
   INITIALIZATION
   ======================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    debugLog('🎤 Initializing HU Voice AI...');
    
    try {
        // Initialize conversation
        initializeConversation();
        
        // Setup event listeners
        setupInputListener();
        setupSubmitButton();
        
        // Load chat history
        loadChatHistory();
        
        // Update status
        updateStatus();
        updateStatusPeriodically();
        
        // Handle viewport changes
        setupViewportHandlers();
        
        // Prevent pinch zoom on mobile
        preventPinchZoom();
        
        // Setup global error handler
        setupGlobalErrorHandler();
        
        showToast('HU Voice AI ready! 🎤', 'success');
        debugLog('✅ Initialization complete');
        
    } catch (error) {
        debugLog('❌ Initialization error: ' + error.message, 'error');
        showToast('Failed to initialize. Refreshing may help.', 'error');
    }
});

/* ========================================================================
   CONVERSATION MANAGEMENT
   ======================================================================== */

function initializeConversation() {
    // Check if conversation ID exists in storage
    AppState.conversationId = localStorage.getItem(CONFIG.CONVERSATION_ID_KEY);
    
    if (!AppState.conversationId) {
        // Generate new conversation ID
        AppState.conversationId = generateConversationId();
        localStorage.setItem(CONFIG.CONVERSATION_ID_KEY, AppState.conversationId);
        debugLog('💾 New conversation created: ' + AppState.conversationId.substring(0, 8));
    } else {
        debugLog('💾 Loaded existing conversation: ' + AppState.conversationId.substring(0, 8));
    }
}

function generateConversationId() {
    return 'conv_' + Date.now() + '_' + Math.random().toString(36).substring(7);
}

/* ========================================================================
   CHAT HISTORY PERSISTENCE
   ======================================================================== */

function saveChatHistory() {
    try {
        const history = {
            conversationId: AppState.conversationId,
            messages: AppState.messageHistory,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem(CONFIG.CHAT_HISTORY_KEY, JSON.stringify(history));
        debugLog('💾 Chat history saved (' + AppState.messageHistory.length + ' messages)');
    } catch (error) {
        debugLog('⚠️  Failed to save chat history: ' + error.message, 'warning');
    }
}

function loadChatHistory() {
    try {
        const stored = localStorage.getItem(CONFIG.CHAT_HISTORY_KEY);
        if (stored) {
            const history = JSON.parse(stored);
            
            // Verify it's the same conversation
            if (history.conversationId === AppState.conversationId) {
                AppState.messageHistory = history.messages || [];
                
                // Restore messages to UI if any exist
                if (AppState.messageHistory.length > 0) {
                    const conversation = document.getElementById('conversation');
                    if (conversation) {
                        // Clear welcome message if we have history
                        const welcome = conversation.querySelector('.welcome-message');
                        if (welcome) welcome.remove();
                        
                        // Restore all messages
                        AppState.messageHistory.forEach(msg => {
                            addMessageToConversationDirect(msg.text, msg.sender);
                        });
                        
                        debugLog('💾 Loaded ' + AppState.messageHistory.length + ' previous messages');
                        showToast('Previous messages loaded ✓', 'info');
                    }
                }
            } else {
                debugLog('💾 Chat history is from different conversation, starting fresh');
                localStorage.removeItem(CONFIG.CHAT_HISTORY_KEY);
            }
        }
    } catch (error) {
        debugLog('⚠️  Failed to load chat history: ' + error.message, 'warning');
    }
}

/* ========================================================================
   INPUT & MESSAGE HANDLING
   ======================================================================== */

function setupInputListener() {
    const input = document.getElementById('questionInput');
    if (!input) {
        debugLog('❌ Input field not found', 'error');
        return;
    }
    
    // Handle Enter key
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submitQuestion();
        }
    });
    
    // Prevent form submission
    input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
        }
    });
    
    // Ensure input is accessible when focused
    input.addEventListener('focus', function() {
        debugLog('⌨️  Input focused');
        // On mobile, scroll the input into view
        setTimeout(() => {
            this.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);
    });
    
    debugLog('✅ Input listener setup complete');
}

function setupSubmitButton() {
    const button = document.getElementById('submitBtn');
    if (!button) {
        debugLog('❌ Submit button not found', 'error');
        return;
    }
    
    // Add click handler (inline handler also exists in HTML)
    button.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        debugLog('📤 Submit button clicked');
        submitQuestion();
    });
    
    debugLog('✅ Submit button setup complete');
}

function submitQuestion() {
    debugLog('📤 Submit question called');
    
    const input = document.getElementById('questionInput');
    if (!input) {
        debugLog('❌ Input field not found', 'error');
        return;
    }
    
    const message = input.value.trim();
    
    // Validate input
    if (!message) {
        debugLog('⚠️  Empty message submitted', 'warning');
        showToast('Please enter a message', 'warning');
        return;
    }
    
    if (message.length > 2000) {
        debugLog('⚠️  Message too long: ' + message.length, 'warning');
        showToast('Message is too long (max 2000 characters)', 'warning');
        return;
    }
    
    // Prevent duplicate submissions
    if (AppState.isLoading) {
        debugLog('⚠️  Submit already in progress', 'warning');
        showToast('Please wait for the previous message to be processed', 'warning');
        return;
    }
    
    AppState.isLoading = true;
    AppState.currentRetryCount = 0;
    
    // Add user message to conversation
    addMessageToConversation(message, 'user');
    
    // Save to history
    AppState.messageHistory.push({
        text: message,
        sender: 'user',
        timestamp: new Date().toISOString()
    });
    
    // Clear input
    input.value = '';
    
    // Blur input to hide mobile keyboard
    input.blur();
    
    // Show loading state
    showLoadingIndicator();
    
    // Reset button state
    updateSubmitButtonState();
    
    // Send to backend with retry
    sendMessageWithRetry(message);
}

async function sendMessageWithRetry(message, retryCount = 0) {
    try {
        debugLog('📤 Sending message (attempt ' + (retryCount + 1) + '/' + CONFIG.MAX_RETRIES + '): ' + message.substring(0, 50) + '...');
        
        const response = await fetchWithTimeout(
            CONFIG.API_BASE_URL + '/chat',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: AppState.conversationId,
                    user_id: 'web_user'
                })
            },
            CONFIG.API_TIMEOUT
        );
        
        if (!response.ok) {
            throw new Error('HTTP ' + response.status + ': ' + response.statusText);
        }
        
        const data = await response.json();
        debugLog('📥 Response received successfully');
        
        // Validate response
        if (!data || typeof data !== 'object') {
            throw new Error('Invalid response format');
        }
        
        if (data.success === false) {
            throw new Error(data.error || 'API returned error');
        }
        
        // Extract answer from response
        const answer = data.answer || data.response || data.message || 'Unable to process your request.';
        
        if (!answer || typeof answer !== 'string') {
            throw new Error('Invalid answer format in response');
        }
        
        // Add agent message
        addMessageToConversation(answer, 'agent');
        
        // Save to history
        AppState.messageHistory.push({
            text: answer,
            sender: 'agent',
            timestamp: new Date().toISOString()
        });
        
        // Save history to storage
        saveChatHistory();
        
        // Scroll to latest message
        scrollConversationToBottom();
        
        showToast('Message sent! ✓', 'success');
        
    } catch (error) {
        debugLog('❌ Error sending message: ' + error.message, 'error');
        AppState.lastError = error;
        
        // Retry logic
        if (retryCount < CONFIG.MAX_RETRIES - 1) {
            const delay = CONFIG.RETRY_DELAY * Math.pow(2, retryCount);  // Exponential backoff
            debugLog('🔄 Retrying in ' + delay + 'ms...');
            showToast('Retrying... (attempt ' + (retryCount + 2) + ')', 'info');
            
            setTimeout(() => {
                sendMessageWithRetry(message, retryCount + 1);
            }, delay);
        } else {
            // All retries failed
            debugLog('❌ All retries failed', 'error');
            
            let errorMessage = 'Sorry, I couldn\'t process your request. ';
            
            if (error.message.includes('timeout')) {
                errorMessage += 'The request timed out. Please check your connection and try again.';
            } else if (error.message.includes('HTTP 429')) {
                errorMessage += 'Too many requests. Please wait a moment and try again.';
            } else if (error.message.includes('HTTP 500')) {
                errorMessage += 'Server error. The backend might be temporarily unavailable.';
            } else if (error.message.includes('Failed to fetch')) {
                errorMessage += 'Network error. Please check your internet connection.';
            } else if (error.message.includes('Invalid')) {
                errorMessage += 'There was an issue with the response format.';
            } else {
                errorMessage += error.message;
            }
            
            // Add error message to conversation
            addMessageToConversation(errorMessage, 'agent');
            scrollConversationToBottom();
            
            // Show error toast
            showToast(errorMessage, 'error');
        }
    } finally {
        hideLoadingIndicator();
        AppState.isLoading = false;
        updateSubmitButtonState();
        
        // Re-focus input for continued interaction
        const input = document.getElementById('questionInput');
        if (input) input.focus();
    }
}

function addMessageToConversation(text, sender) {
    debugLog('📝 Adding ' + sender + ' message');
    addMessageToConversationDirect(text, sender);
}

function addMessageToConversationDirect(text, sender) {
    const conversation = document.getElementById('conversation');
    if (!conversation) {
        debugLog('❌ Conversation container not found', 'error');
        return;
    }
    
    // Remove welcome message on first user message
    if (sender === 'user') {
        const welcome = conversation.querySelector('.welcome-message');
        if (welcome) {
            welcome.remove();
            debugLog('✅ Welcome message removed');
        }
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender + '-message';
    messageDiv.setAttribute('role', 'article');
    messageDiv.setAttribute('aria-label', sender + ' message');
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    bubble.style.wordWrap = 'break-word';
    bubble.style.overflowWrap = 'break-word';
    
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
            try {
                conversation.scrollTop = conversation.scrollHeight;
                debugLog('✅ Scrolled to bottom');
            } catch (error) {
                debugLog('⚠️  Scroll failed: ' + error.message, 'warning');
            }
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
        debugLog('✅ Loading indicator shown');
    } else {
        debugLog('⚠️  Loading indicator element not found', 'warning');
    }
}

function hideLoadingIndicator() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.style.display = 'none';
        debugLog('✅ Loading indicator hidden');
    }
}

function updateSubmitButtonState() {
    const btn = document.getElementById('submitBtn');
    if (btn) {
        btn.disabled = AppState.isLoading;
        btn.style.opacity = AppState.isLoading ? '0.6' : '1';
        btn.style.cursor = AppState.isLoading ? 'not-allowed' : 'pointer';
    }
}

/* ========================================================================
   TOAST NOTIFICATIONS
   ======================================================================== */

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) {
        debugLog('⚠️  Toast container not found', 'warning');
        console.log('Toast: ' + message + ' (' + type + ')');
        return;
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    
    // Add to container
    container.appendChild(toast);
    
    debugLog('🔔 Toast shown: ' + message.substring(0, 50));
    
    // Auto-remove after timeout
    setTimeout(() => {
        toast.classList.add('toast-removing');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, CONFIG.TOAST_TIMEOUT);
}

/* ========================================================================
   STATUS UPDATES
   ======================================================================== */

async function updateStatus() {
    try {
        debugLog('🔍 Checking API status...');
        
        const response = await fetchWithTimeout(
            CONFIG.API_BASE_URL + '/status',
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            },
            5000  // 5 second timeout for status
        );
        
        if (response.ok) {
            const data = await response.json();
            const badge = document.getElementById('status');
            if (badge) {
                const isOnline = data.status === 'online' || data.status === 'active';
                badge.textContent = isOnline ? '🟢 Online' : '🔴 Offline';
                badge.classList.toggle('status-offline', !isOnline);
                debugLog('✅ Status updated: ' + (isOnline ? 'Online' : 'Offline'));
            }
        } else {
            throw new Error('Status check returned ' + response.status);
        }
    } catch (error) {
        debugLog('⚠️  Status check failed: ' + error.message, 'warning');
        const badge = document.getElementById('status');
        if (badge) {
            badge.textContent = '🔴 Offline';
            badge.classList.add('status-offline');
        }
    }
}

function updateStatusPeriodically() {
    // Update status every 30 seconds
    setInterval(updateStatus, CONFIG.STATUS_UPDATE_INTERVAL);
}

/* ========================================================================
   VOICE INPUT HANDLING
   ======================================================================== */

function toggleVoiceInput() {
    if (AppState.isRecording) {
        stopVoiceRecording();
    } else {
        startVoiceRecording();
    }
}

function startVoiceRecording() {
    debugLog('🎤 Voice recording requested');
    
    // Check browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        debugLog('❌ Speech Recognition not supported', 'error');
        showToast('Speech Recognition not supported in your browser', 'error');
        return;
    }
    
    AppState.isRecording = true;
    const btn = document.getElementById('voiceBtn');
    if (btn) {
        btn.classList.add('recording');
        btn.innerHTML = '<span class="btn-icon">⏹️</span><span class="btn-text">Stop</span>';
    }
    
    debugLog('🎙️ Voice recording started');
    showToast('Recording... speak now', 'info');
}

function stopVoiceRecording() {
    debugLog('⏹️ Voice recording stopped');
    AppState.isRecording = false;
    
    const btn = document.getElementById('voiceBtn');
    if (btn) {
        btn.classList.remove('recording');
        btn.innerHTML = '<span class="btn-icon">🎤</span><span class="btn-text">Voice</span>';
    }
    
    showToast('Recording stopped', 'info');
}

/* ========================================================================
   TEXT INPUT FOCUS
   ======================================================================== */

function focusTextInput() {
    const input = document.getElementById('questionInput');
    if (input) {
        input.focus();
        debugLog('⌨️  Text input focused');
    }
}

/* ========================================================================
   VIEWPORT & MOBILE HANDLING
   ======================================================================== */

function setupViewportHandlers() {
    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
        debugLog('📱 Orientation changed to: ' + window.orientation);
        // Allow time for DOM to adjust
        setTimeout(() => {
            const input = document.getElementById('questionInput');
            if (input) input.focus();
        }, 200);
    });
    
    // Handle resize
    window.addEventListener('resize', () => {
        const currentHeight = window.innerHeight;
        
        // If height decreased significantly, keyboard is likely open
        if (currentHeight < AppState.originalViewportHeight - CONFIG.KEYBOARD_DETECTION_THRESHOLD) {
            debugLog('⌨️  Keyboard appears to be open');
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
    
    debugLog('✅ Viewport handlers setup complete');
}

function preventPinchZoom() {
    // Prevent pinch zoom on mobile (better for fixed layouts)
    document.addEventListener('touchmove', function(event) {
        if (event.touches.length > 1) {
            event.preventDefault();
        }
    }, { passive: false });
    
    debugLog('✅ Pinch zoom prevented');
}

/* ========================================================================
   KEYBOARD MANAGEMENT
   ======================================================================== */

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift+Enter: new line (allow default)
            debugLog('⌨️  Shift+Enter detected');
            return;
        }
        // Enter alone: send message
        event.preventDefault();
        debugLog('⌨️  Enter key detected');
        submitQuestion();
    }
}

/* ========================================================================
   FETCH WITH TIMEOUT
   ======================================================================== */

async function fetchWithTimeout(url, options = {}, timeout = CONFIG.API_TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
        controller.abort();
    }, timeout);
    
    try {
        debugLog('🌐 Fetch request to: ' + url.split('?')[0]);
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout after ' + timeout + 'ms');
        }
        throw error;
    }
}

/* ========================================================================
   ERROR HANDLING
   ======================================================================== */

function setupGlobalErrorHandler() {
    window.addEventListener('error', function(event) {
        debugLog('❌ Global error: ' + event.message, 'error');
        if (!AppState.isLoading) {
            showToast('An unexpected error occurred', 'error');
        }
    });
    
    window.addEventListener('unhandledrejection', function(event) {
        debugLog('❌ Unhandled promise rejection: ' + event.reason, 'error');
        if (!AppState.isLoading) {
            showToast('An unexpected error occurred', 'error');
        }
    });
    
    debugLog('✅ Global error handler setup complete');
}

/* ========================================================================
   DEBUG LOGGING
   ======================================================================== */

function debugLog(message, level = 'log') {
    const timestamp = new Date().toLocaleTimeString();
    const logMessage = '[' + timestamp + '] ' + message;
    
    switch (level) {
        case 'error':
            console.error(logMessage);
            break;
        case 'warning':
            console.warn(logMessage);
            break;
        default:
            console.log(logMessage);
    }
}

/* ========================================================================
   STARTUP LOGGING
   ======================================================================== */

console.log('%c🎤 HU Voice AI - Enhanced with Full Features', 'color: #6366f1; font-size: 14px; font-weight: bold;');
console.log('%cViewport Height: ' + window.innerHeight + 'px', 'color: #8b5cf6');
console.log('%cViewport Width: ' + window.innerWidth + 'px', 'color: #8b5cf6');
console.log('%cDevice Pixel Ratio: ' + window.devicePixelRatio, 'color: #8b5cf6');
console.log('%cFeatures: Toast Notifications, Chat History, Retry Logic, Timeouts, Error Handling', 'color: #10b981');
console.log('%cDebug Logs Available in Browser Console', 'color: #f59e0b');

