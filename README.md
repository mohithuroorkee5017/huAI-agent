# 🎤 HARIDWAR UNIVERSITY AI - Complete Setup & Usage Guide

## Overview
**HARIDWAR UNIVERSITY AI** is an advanced voice-based AI assistant that:
- ✅ Accepts voice input and processes queries
- ✅ Fetches real-time data from Google
- ✅ Provides voice output responses
- ✅ Maintains conversation history
- ✅ Works via Web Interface or Python API
- ✅ Uses your provided API key for integration

---

## 📋 Project Structure

```
Haridwar University AI/
├── huvoice_agent.py          # Main agent application
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── README.md                 # This file
├── templates/
│   └── index.html           # Web interface
└── static/
    ├── style.css            # UI styling
    └── script.js            # Frontend logic
```

---

## 🚀 Installation & Setup

### Step 1: Prerequisites
- Python 3.8+
- pip (Python package manager)
- Microphone (for voice input)
- Internet connection

### Step 2: Install Dependencies
```bash
cd "d:\Users\pop\Desktop\Haridwar University AI"
pip install -r requirements.txt
```

**Note:** If you encounter issues with PyAudio on Windows, install it separately:
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 3: Verify API Key
The API key is already configured in `.env`:
```
API_KEY=sk-or-v1-YOUR_KEY_HERE
```

---

## 🎯 Running HARIDWAR UNIVERSITY AI

### Option 1: Start Web Interface (Recommended)
```bash
python huvoice_agent.py
```

Then open your browser to: **http://localhost:5000**

### Option 2: Command Line Interface
Modify `huvoice_agent.py` to call the voice interaction method:
```python
if __name__ == '__main__':
    agent = HaridwarUniversityAI(API_KEY)
    agent.voice_interaction()  # Start voice loop
```

---

## 💡 Usage Guide

### Web Interface Features

#### 1. **Voice Input** 🎤
- Click "Voice Input" button
- Speak your question clearly
- Agent processes and responds with voice

#### 2. **Text Input** ⌨️
- Type your question in the input field
- Press Enter or click "Send"
- Get instant answer from Google search

#### 3. **View Conversation History**
- All Q&A pairs are displayed in real-time
- See timestamps for each interaction
- Questions appear in blue, answers in light blue

#### 4. **Clear History**
- Click "Clear History" to reset conversation
- Counters reset to 0

#### 5. **Live Transcript**
- See last voice/text input
- Timestamp of input
- Useful for debugging

### API Endpoints

#### Ask Question (POST)
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

Response:
```json
{
  "success": true,
  "question": "What is Python?",
  "answer": "Python is a high-level programming language...",
  "timestamp": "2026-05-25T10:30:45.123456"
}
```

#### Voice Input (POST)
```bash
curl -X POST http://localhost:5000/api/voice-input
```

#### Get Conversation History (GET)
```bash
curl http://localhost:5000/api/history
```

#### Get Agent Status (GET)
```bash
curl http://localhost:5000/api/status
```

Response:
```json
{
  "status": "active",
  "agent_name": "HUVOICE AGENT",
  "listening": false,
  "conversation_count": 5
}
```

#### Clear History (POST)
```bash
curl -X POST http://localhost:5000/api/clear-history
```

---

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Agent Settings
AGENT_NAME=HUVOICE AGENT
FLASK_PORT=5000
LOG_LEVEL=INFO

# Features
VOICE_ENABLED=True
GOOGLE_SEARCH_ENABLED=True
```

---

## 🎨 Features

### 1. **Google Search Integration**
- Real-time data fetching
- Featured snippets extraction
- Top 3 results processing
- Answer synthesis

### 2. **Voice Processing**
- Speech-to-text conversion
- Text-to-speech output
- Ambient noise adjustment
- Timeout handling

### 3. **Web Interface**
- Modern responsive design
- Real-time updates
- Conversation display
- Status indicators
- Statistics tracking

### 4. **API Integration**
- RESTful API endpoints
- JSON responses
- Error handling
- Status monitoring

### 5. **Conversation Management**
- History tracking
- Timestamping
- Session management
- Export capability

---

## 🔍 Example Questions

Try asking HUVOICE AGENT:

```
"What is artificial intelligence?"
"Who is the president of the United States?"
"What is the capital of France?"
"How does photosynthesis work?"
"What are the benefits of exercise?"
"Tell me about quantum computing"
"What is machine learning?"
"How far is Mars from Earth?"
```

---

## 🐛 Troubleshooting

### Issue: Microphone not detected
**Solution:** 
```bash
python -m pip install --upgrade pyaudio
```

### Issue: Speech recognition fails
**Solution:**
- Ensure microphone is working
- Check internet connection (uses Google Speech API)
- Speak clearly and slowly
- Reduce background noise

### Issue: Port 5000 already in use
**Solution:**
```bash
# Change port in .env file
FLASK_PORT=5001
```

### Issue: Google search returns no results
**Solution:**
- Check internet connection
- Try rephrasing question more simply
- Check for firewall restrictions

---

## 📊 Performance Tips

1. **For faster responses:**
   - Use typed input instead of voice
   - Ask specific questions

2. **For better voice recognition:**
   - Use a good quality microphone
   - Reduce ambient noise
   - Speak clearly and at normal pace

3. **For better answers:**
   - Be specific in your questions
   - Use keywords
   - Ask one question at a time

---

## 🔐 Security

- API key is stored locally in `.env`
- All data processing is local except Google Search
- No data is stored on remote servers
- Conversation history is in-memory only

---

## 📝 Logs

Check logs in the console for:
- Agent initialization
- Voice input/output events
- Search queries
- API requests
- Errors and warnings

---

## 🚀 Advanced Usage

### Integrate with External Systems

```python
from huvoice_agent import HUVoiceAgent

# Create agent instance
agent = HUVoiceAgent('your-api-key')

# Ask a question programmatically
answer = agent.process_question("What is Python?")
print(answer)

# Get conversation history
history = agent.get_conversation_history()
```

### Extend Functionality

You can extend the agent by:
1. Adding more search backends
2. Integrating with other APIs
3. Adding sentiment analysis
4. Implementing conversation memory
5. Adding custom commands

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review logs for error messages
3. Verify all dependencies are installed
4. Ensure API key is valid

---

## 📦 Technologies Used

- **Python 3.8+** - Core language
- **Flask** - Web framework
- **SpeechRecognition** - Voice input
- **pyttsx3** - Voice output
- **BeautifulSoup4** - Web scraping
- **requests** - HTTP client
- **HTML5/CSS3/JavaScript** - Frontend

---

## 📄 License

HUVOICE AGENT is created for educational and personal use.

---

## ✨ Features Coming Soon

- 🎵 Music search and playback
- 📊 Data visualization
- 🗣️ Multi-language support
- 🎯 Intent recognition
- 💾 Database storage
- 🔗 Social media integration

---

**Last Updated:** May 25, 2026
**Version:** 1.0
**Agent Name:** HUVOICE AGENT

---

🎉 **Enjoy using HUVOICE AGENT!** 🎉
