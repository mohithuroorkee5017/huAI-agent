// HUVOICE AGENT - Frontend JavaScript

let isRecording = false;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Display logged-in user
    const userDisplay = document.getElementById('user-display');
    if (userDisplay) {
        const userData = localStorage.getItem('user');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                userDisplay.textContent = `👤 ${user.fullname || user.email}`;
            } catch (e) {
                console.log('Could not parse user data');
            }
        }
    }
    
    updateStatus();
    setInterval(updateStatus, 5000); // Update status every 5 seconds
});

// Update agent status
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusBadge = document.getElementById('status');
        
        if (data.status === 'active') {
            statusBadge.textContent = '🟢 Online';
            statusBadge.className = 'status-badge active';
            
            if (data.listening) {
                statusBadge.textContent = '🎤 Listening...';
                statusBadge.className = 'status-badge listening';
            }
        } else {
            statusBadge.textContent = '🔴 Offline';
            statusBadge.className = 'status-badge';
        }
    } catch (error) {
        console.error('Status update failed:', error);
    }
}

// Toggle voice input
async function toggleVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    
    if (isRecording) {
        isRecording = false;
        voiceBtn.classList.remove('recording');
        return;
    }
    
    isRecording = true;
    voiceBtn.classList.add('recording');
    voiceBtn.innerHTML = '<span class="mic-icon">🎤</span> Stop Recording';
    
    showLoading(true);
    
    try {
        // Request voice input from backend
        const response = await fetch('/api/voice-input', {
            method: 'POST'
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success && data.heard) {
            // Add question to input and display
            document.getElementById('questionInput').value = data.heard;
            addMessage(data.heard, 'user');
            addMessage(data.answer, 'agent');
            
            // Update transcript
            updateTranscript(data.heard);
        }
        
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<span class="mic-icon">🎤</span> Voice Input';
        
    } catch (error) {
        console.error('Voice input error:', error);
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<span class="mic-icon">🎤</span> Voice Input';
        showLoading(false);
        addMessage('Error with voice input. Please try again.', 'agent');
    }
}

// Focus text input
function focusTextInput() {
    document.getElementById('questionInput').focus();
}

// Handle key press in input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        submitQuestion();
    }
}

// Submit question
async function submitQuestion() {
    const input = document.getElementById('questionInput');
    const imageInput = document.getElementById('imageInput');
    const question = input.value.trim();
    
    // Check if image is selected
    if (imageInput.files.length > 0) {
        // Send image instead
        const file = imageInput.files[0];
        const prompt = question || 'Please analyze this image and describe what you see.';
        
        showLoading(true);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('prompt', prompt);
            
            const response = await fetch('/api/image', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            showLoading(false);
            
            if (data.success) {
                // Add image message
                addImageMessage(file.name);
                
                // Add analysis result
                addMessage(data.answer, 'agent');
                
                // Show detected objects if any
                if (data.objects && data.objects.length > 0) {
                    const objectsText = `📌 Detected: ${data.objects.join(', ')}`;
                    addMessage(objectsText, 'agent');
                }
                
                // Clear inputs
                removeImagePreview();
                input.value = '';
            } else {
                addMessage('Error analyzing image: ' + (data.error || 'Unknown error'), 'agent');
            }
        } catch (error) {
            console.error('Image upload error:', error);
            showLoading(false);
            addMessage('Error uploading image. Please try again.', 'agent');
        }
        return;
    }
    
    // Normal text question
    if (!question) {
        alert('Please enter a question or select an image');
        return;
    }
    
    // Add question message
    addMessage(question, 'user');
    input.value = '';
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            // Add answer message
            addMessage(data.answer, 'agent');
            
            // Update transcript
            updateTranscript(question);
        } else {
            addMessage('Error: ' + (data.error || 'Unknown error'), 'agent');
        }
        
    } catch (error) {
        console.error('Submit error:', error);
        showLoading(false);
        addMessage('Error submitting question. Please try again.', 'agent');
    }
}

// Add message to conversation
function addMessage(text, sender) {
    const conversation = document.getElementById('conversation');
    
    // Remove welcome message if present
    const welcomeMsg = conversation.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender}-message`;
    
    // Truncate long messages for display
    const displayText = text.length > 300 ? text.substring(0, 300) + '...' : text;
    bubble.textContent = displayText;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(timeDiv);
    
    conversation.appendChild(messageDiv);
    
    // Scroll to bottom
    conversation.scrollTop = conversation.scrollHeight;
}

// Update transcript
function updateTranscript(text) {
    const transcript = document.getElementById('transcript');
    const displayText = text.length > 150 ? text.substring(0, 150) + '...' : text;
    
    transcript.innerHTML = `
        <p><strong>Last Input:</strong> ${displayText}</p>
        <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
    `;  
}

// Clear conversation
async function clearConversation() {
    if (confirm('Are you sure you want to clear the conversation history?')) {
        try {
            const response = await fetch('/api/clear-history', {
                method: 'POST'
            });
            
            if (response.ok) {
                document.getElementById('conversation').innerHTML = `
                    <div class="welcome-message">
                        <p>👋 Welcome to HUVOICE AGENT</p>
                        <p>I can search Google and answer your questions. Ask me anything!</p>
                    </div>
                `;
                questionCount = 0;
                answerCount = 0;
                updateCounters();
            }
        } catch (error) {
            console.error('Clear history error:', error);
        }
    }
}

// Show/hide loading indicator
function showLoading(show) {
    const indicator = document.getElementById('loadingIndicator');
    if (show) {
        indicator.style.display = 'flex';
    } else {
        indicator.style.display = 'none';
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+E or Cmd+E to toggle voice
    if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
        event.preventDefault();
        toggleVoiceInput();
    }
    
    // Ctrl+L or Cmd+L to clear
    if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
        event.preventDefault();
        clearConversation();
    }
});

// Auto-update status every 3 seconds
setInterval(async function() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.status === 'active' && data.conversation_count > 0) {
            // Conversation is active, could fetch latest if needed
        }
    } catch (error) {
        // Silently fail on periodic status check
    }
}, 3000);

// Handle image selection
function handleImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file size (max 20MB)
    const maxSize = 20 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('Image file too large. Maximum size: 20MB');
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');
        previewImg.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Remove image preview
function removeImagePreview() {
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('imagePreview');
    imageInput.value = '';
    previewContainer.style.display = 'none';
}

// Submit image with optional prompt
async function submitImageWithPrompt() {
    const imageInput = document.getElementById('imageInput');
    const questionInput = document.getElementById('questionInput');
    
    if (!imageInput.files[0]) {
        alert('Please select an image');
        return;
    }
    
    const file = imageInput.files[0];
    const prompt = questionInput.value.trim() || 'Please analyze this image and describe what you see.';
    
    showLoading(true);
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('prompt', prompt);
        
        const response = await fetch('/api/image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            // Add image message
            addImageMessage(file.name);
            
            // Add analysis result
            addMessage(data.answer, 'agent');
            
            // Show detected objects if any
            if (data.objects && data.objects.length > 0) {
                const objectsText = `📌 Detected: ${data.objects.join(', ')}`;
                addMessage(objectsText, 'agent');
            }
            
            // Clear inputs
            removeImagePreview();
            questionInput.value = '';
        } else {
            addMessage('Error analyzing image: ' + (data.error || 'Unknown error'), 'agent');
        }
    } catch (error) {
        console.error('Image upload error:', error);
        showLoading(false);
        addMessage('Error uploading image. Please try again.', 'agent');
    }
}

// Add image message to conversation
function addImageMessage(filename) {
    const conversation = document.getElementById('conversation');
    
    // Remove welcome message if present
    const welcomeMsg = conversation.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble user-message';
    bubble.textContent = `📷 Sent image: ${filename}`;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(timeDiv);
    
    conversation.appendChild(messageDiv);
    
    // Scroll to bottom
    conversation.scrollTop = conversation.scrollHeight;
}
