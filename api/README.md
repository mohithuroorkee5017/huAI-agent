# Haridwar University AI API

A production-ready FastAPI backend for intelligent conversational AI with multilingual support (Hindi, English, Hinglish).

## 🌟 Features

- **Multi-language Support**: Automatic language detection for Hindi, English, and Hinglish
- **Conversational AI**: Natural, human-like responses using OpenRouter API
- **Context-Aware**: Maintains conversation history (last 20 messages)
- **Multiple Knowledge Sources**:
  - Wikipedia integration for general knowledge
  - Web search via DuckDuckGo for latest information
  - University knowledge base for student queries
- **Production Ready**:
  - Error handling and logging
  - Rate limiting (100 requests per minute)
  - CORS support
  - Health check endpoints
  - Request/response validation

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key (get one from: https://openrouter.ai/keys)
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone/Download the Project

```bash
cd api
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
# OPENROUTER_API_KEY=your_key_here
```

### 5. Run the Server

```bash
python main.py
```

The API will start on `http://localhost:5000`

## 📚 API Documentation

### Interactive Docs

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

### Endpoints

#### Health Check
```
GET /health
```

Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T10:00:00",
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

#### Status
```
GET /status
```

Returns API statistics and status.

**Response:**
```json
{
  "status": "online",
  "timestamp": "2024-01-01T10:00:00",
  "active_conversations": 5,
  "total_requests": 150,
  "api_configured": true
}
```

#### Chat (Main Endpoint)
```
POST /chat
```

Send a message and get an AI response.

**Request:**
```json
{
  "message": "क्या आप मुझे कुछ बता सकते हो?",
  "conversation_id": "optional_id"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "हाँ, बिल्कुल! मैं आपकी मदद कर सकता हूँ। क्या आप मुझसे कोई सवाल पूछना चाहते हैं?",
  "sources": [
    {
      "type": "University Knowledge",
      "title": "admissions",
      "url": ""
    }
  ],
  "language": "hinglish",
  "conversation_id": "conv_abc123",
  "timestamp": "2024-01-01T10:00:00"
}
```

#### Get Conversation History
```
GET /conversations/{conversation_id}
```

Retrieve conversation history.

**Response:**
```json
{
  "conversation_id": "conv_abc123",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "language": "en",
      "timestamp": "2024-01-01T10:00:00"
    },
    {
      "role": "assistant",
      "content": "Hi there! How can I help you?",
      "language": "en",
      "timestamp": "2024-01-01T10:00:05"
    }
  ],
  "count": 2
}
```

#### Clear Conversation
```
DELETE /conversations/{conversation_id}
```

Clear conversation history.

**Response:**
```json
{
  "success": true,
  "message": "Conversation conv_abc123 cleared",
  "timestamp": "2024-01-01T10:00:00"
}
```

## 💬 Usage Examples

### Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Send a message
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "message": "What are the admission requirements?",
        "conversation_id": "student_123"
    }
)

print(response.json())

# Get conversation history
history = requests.get(
    f"{BASE_URL}/conversations/student_123"
)

print(history.json())
```

### cURL

```bash
# Send a message
curl -X POST "http://localhost:5000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "tell me about campus facilities",
    "conversation_id": "conv_123"
  }'

# Get health status
curl -X GET "http://localhost:5000/health"

# Get API status
curl -X GET "http://localhost:5000/status"
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

async function chat() {
  try {
    const response = await axios.post('http://localhost:5000/chat', {
      message: 'What are the placement statistics?',
      conversation_id: 'conv_123'
    });
    
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

chat();
```

## 🏗️ Project Structure

```
api/
├── main.py                 # Main FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your environment variables (create this)
├── app.log               # Application logs (auto-generated)
└── services/
    ├── __init__.py       # Services package
    ├── openrouter.py     # OpenRouter AI integration
    ├── search.py         # DuckDuckGo web search
    ├── wiki.py           # Wikipedia integration
    └── memory.py         # Conversation memory management
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# API Settings
PORT=5000
DEBUG=False

# OpenRouter API
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini

# Conversation Settings
MAX_CONVERSATION_HISTORY=20
CONVERSATION_TIMEOUT=3600

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## 🎯 Knowledge Sources

### 1. University Knowledge Base

Covers topics like:
- Admissions and eligibility
- Courses and programs
- Placements and statistics
- Scholarships and financial aid
- Hostel facilities
- Faculty information
- Fees structure
- Campus facilities

### 2. Wikipedia

Automatically searches Wikipedia for:
- General knowledge questions
- Technical topics
- Historical information
- Scientific concepts

### 3. Web Search (DuckDuckGo)

Activated for queries about:
- Latest news and current affairs
- Recent events
- 2024/2025 developments
- Trending topics

## 🔐 Security Features

- **Rate Limiting**: 100 requests per 60 seconds per IP
- **Input Validation**: Pydantic models validate all inputs
- **Error Handling**: Graceful error responses without leaking internal details
- **CORS**: Configurable Cross-Origin Resource Sharing
- **Logging**: All requests and errors are logged

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
tail -f app.log

# Search for errors
grep ERROR app.log

# Search for specific conversation
grep "conversation_id" app.log
```

### Check Health

```bash
curl http://localhost:5000/health
```

### Monitor Statistics

```bash
curl http://localhost:5000/status
```

## 🐛 Troubleshooting

### 1. ImportError: No module named 'fastapi'

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### 2. OPENROUTER_API_KEY not configured

**Solution**: 
- Get API key from https://openrouter.ai/keys
- Create `.env` file with your key
```bash
OPENROUTER_API_KEY=your_key_here
```

### 3. Port 5000 already in use

**Solution**: Change port in `.env`
```bash
PORT=8000
```

### 4. Connection errors with external services

**Solution**: Check internet connection and timeouts
```bash
WIKIPEDIA_TIMEOUT=10
DUCKDUCKGO_TIMEOUT=10
```

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn

gunicorn main:app --workers 4 --bind 0.0.0.0:5000
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

Build and run:
```bash
docker build -t hu-voice-ai .
docker run -p 5000:5000 -e OPENROUTER_API_KEY=your_key hu-voice-ai
```

## 📝 Response Format

All responses follow a consistent format:

**Success:**
```json
{
  "success": true,
  "answer": "Response text",
  "sources": [...],
  "language": "en",
  "conversation_id": "conv_123",
  "timestamp": "2024-01-01T10:00:00"
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2024-01-01T10:00:00"
}
```

## 🌐 Language Support

The API automatically detects and responds in:

- **Hindi** (हिंदी): `language: "hi"`
- **English**: `language: "en"`
- **Hinglish** (हिंग्लिश): `language: "hinglish"`

Mix of Hindi and English in natural conversation.

## 📚 System Behavior

- **Context-Aware**: Uses conversation history for better responses
- **Natural Responses**: Replies like a friendly human assistant
- **No Dictionary Mode**: Doesn't give dictionary definitions unless asked
- **No Repetition**: Each response is unique and varied
- **Follow-up Handling**: Understands and addresses follow-up questions
- **Source Integration**: Mentions sources used for response generation

## 🔄 Conversation Flow

1. User sends message
2. Language auto-detected
3. Conversation history retrieved
4. Knowledge sources searched (Wikipedia, Web, University KB)
5. AI generates response using OpenRouter
6. Response returned with sources and metadata
7. Conversation stored in memory

## 📄 License

MIT License - Feel free to use for any purpose

## 🤝 Support

For issues or questions:
1. Check logs: `tail -f app.log`
2. Review configuration in `.env`
3. Verify OpenRouter API key
4. Check internet connection
5. Inspect endpoint responses in `/docs`

## 🎓 Educational Use

Perfect for:
- University student assistant
- Campus information chatbot
- Course inquiry system
- Admission guidance bot
- Career placement help

## 🌟 Future Enhancements

- PostgreSQL database integration
- User authentication and profiles
- Conversation analytics
- Custom knowledge base management
- Multi-modal input (voice, images)
- Sentiment analysis
- Response quality metrics

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production Ready ✅
