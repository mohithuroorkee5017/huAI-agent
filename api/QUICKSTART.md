# 🚀 HU Voice AI API - Quick Start

Get your AI backend running in under 5 minutes!

## ⚡ Super Quick Start (5 min)

### 1. Prerequisites
- Python 3.8+ installed
- OpenRouter API key (get free one at https://openrouter.ai/keys)

### 2. Setup (Windows)

```bash
# Open Command Prompt in the api folder and run:
start.bat
```

**That's it!** The script will:
- Create virtual environment
- Install dependencies
- Ask for OpenRouter API key
- Start the server

### 3. Setup (macOS/Linux)

```bash
bash start.sh
```

### 4. Test It

Open your browser and go to:
```
http://localhost:5000/docs
```

Click **POST /chat**, then **Try it out**, enter a message, and hit **Execute**!

---

## 📝 Manual Setup (If scripts don't work)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env and add OPENROUTER_API_KEY
python main.py
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add OPENROUTER_API_KEY
python main.py
```

---

## 🧪 Quick Test

### Using cURL

```bash
# Test if server is running
curl http://localhost:5000/health

# Send a message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello","conversation_id":"test1"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:5000/chat",
    json={"message": "Tell me about your features"}
)

print(response.json())
```

### Using Interactive Docs

1. Go to http://localhost:5000/docs
2. Click any endpoint (try **GET /health** first)
3. Click **Try it out**
4. Click **Execute**

---

## 🔧 Configuration (Optional)

Edit `.env` file:

```env
# REQUIRED: Add your OpenRouter API key
OPENROUTER_API_KEY=your_key_here

# Optional: Change port if 5000 is in use
PORT=8000

# Optional: Change log level
LOG_LEVEL=INFO
```

---

## 📚 API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | POST | Send message, get AI response |
| `/health` | GET | Server health check |
| `/status` | GET | Server statistics |
| `/conversations/{id}` | GET | Get conversation history |
| `/conversations/{id}` | DELETE | Clear conversation |
| `/docs` | GET | Interactive API docs |

---

## 💬 Example Messages to Try

### English
- "What are the admission requirements?"
- "Tell me about placements"
- "What scholarships are available?"

### Hindi
- "प्रवेश के लिए क्या योग्यता चाहिए?"
- "छात्रवृत्ति के बारे में बताइये"
- "कैंपस की सुविधाएं क्या हैं?"

### Hinglish
- "admission ke baare mein batao"
- "campus facilities kaisi hain?"
- "hostel ke charges kya hain?"

### Current Affairs
- "What's new in AI?"
- "Tell me recent tech news"
- "Latest developments in 2025"

---

## ❌ Troubleshooting

### "Port 5000 already in use"
```bash
# Change PORT in .env to 8000
PORT=8000
```

### "OPENROUTER_API_KEY not configured"
1. Edit `.env`
2. Add: `OPENROUTER_API_KEY=your_key_from_openrouter.ai`

### "No module named 'fastapi'"
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### "Connection error"
- Check internet connection
- Check firewall settings
- Verify OpenRouter API key

---

## 📖 Next Steps

1. ✅ Server running
2. 📚 Read [README.md](README.md) for detailed API documentation
3. ⚙️ Check [SETUP.md](SETUP.md) for advanced configuration
4. 🔍 Review [SPECIFICATION.md](SPECIFICATION.md) for technical details
5. 🧪 Run `python test_api.py` for comprehensive testing

---

## 🎯 Common Tasks

### Get conversation history
```bash
curl http://localhost:5000/conversations/conv_id
```

### Clear a conversation
```bash
curl -X DELETE http://localhost:5000/conversations/conv_id
```

### Check API status
```bash
curl http://localhost:5000/status
```

### View logs
```bash
tail -f app.log         # macOS/Linux
type app.log            # Windows
```

---

## 📊 What's Inside

```
api/
├── main.py              ← Main application (FastAPI)
├── config.py            ← Configuration
├── requirements.txt     ← Dependencies
├── .env.example         ← Config template
├── services/
│   ├── openrouter.py    ← AI + Language detection
│   ├── memory.py        ← Conversation memory
│   ├── wiki.py          ← Wikipedia search
│   └── search.py        ← Web search
├── README.md            ← Full documentation
├── SETUP.md             ← Setup guide
└── SPECIFICATION.md     ← Technical spec
```

---

## ✨ Features

✅ Multi-language support (Hindi, English, Hinglish)  
✅ Conversation memory (last 20 messages)  
✅ Wikipedia integration  
✅ Web search capability  
✅ University knowledge base  
✅ Rate limiting (100 req/min)  
✅ CORS support  
✅ Error handling & logging  
✅ Production-ready  

---

## 🚀 Deployment

### Heroku
```bash
# Coming soon - check README.md
```

### Docker
```bash
docker build -t hu-voice-ai .
docker run -p 5000:5000 -e OPENROUTER_API_KEY=your_key hu-voice-ai
```

### AWS/Azure
- Deploy with Gunicorn
- Use managed databases
- Set up CDN
- Enable monitoring

---

## 📞 Need Help?

1. Check logs: `tail -f app.log`
2. Review API docs: http://localhost:5000/docs
3. Read [SETUP.md](SETUP.md)
4. Read [SPECIFICATION.md](SPECIFICATION.md)

---

**Happy coding! 🎉**

**Version**: 1.0.0  
**Status**: Production Ready ✅
