# HU Voice AI API - Getting Started Checklist

Quick checklist to get your AI backend up and running!

## ✅ Pre-Setup Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] OpenRouter API key (get from https://openrouter.ai/keys)
- [ ] Internet connection available
- [ ] 500MB disk space available
- [ ] 2GB RAM available

## ✅ 5-Minute Setup (Windows)

- [ ] Download/Extract project to folder
- [ ] Open Command Prompt in project folder
- [ ] Run: `start.bat`
- [ ] Wait for dependencies to install
- [ ] Enter your OpenRouter API key when prompted
- [ ] Server starts on http://localhost:5000

## ✅ 5-Minute Setup (macOS/Linux)

- [ ] Download/Extract project to folder
- [ ] Open Terminal in project folder
- [ ] Run: `bash start.sh`
- [ ] Wait for dependencies to install
- [ ] Enter your OpenRouter API key when prompted
- [ ] Server starts on http://localhost:5000

## ✅ Manual Setup (If Scripts Don't Work)

### Windows
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate: `venv\Scripts\activate`
- [ ] Install: `pip install -r requirements.txt`
- [ ] Copy: `copy .env.example .env`
- [ ] Edit `.env` and add: `OPENROUTER_API_KEY=your_key`
- [ ] Start: `python main.py`

### macOS/Linux
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate: `source venv/bin/activate`
- [ ] Install: `pip install -r requirements.txt`
- [ ] Copy: `cp .env.example .env`
- [ ] Edit `.env` and add: `OPENROUTER_API_KEY=your_key`
- [ ] Start: `python main.py`

## ✅ First Time Configuration

- [ ] Obtain OpenRouter API key from https://openrouter.ai/keys
- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` in text editor
- [ ] Find line: `OPENROUTER_API_KEY=`
- [ ] Paste your key: `OPENROUTER_API_KEY=sk_live_xxxxx`
- [ ] Save `.env` file
- [ ] Restart server (if already running)

## ✅ Testing Your Setup

### Test 1: Health Check
- [ ] Open browser: http://localhost:5000/health
- [ ] Should see JSON response with `"status": "healthy"`

### Test 2: Interactive Docs
- [ ] Open browser: http://localhost:5000/docs
- [ ] Click on `POST /chat`
- [ ] Click `Try it out`
- [ ] Enter test message: `hello`
- [ ] Click `Execute`
- [ ] Should see response with AI answer

### Test 3: Command Line (cURL)
- [ ] Open terminal/command prompt
- [ ] Run:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```
- [ ] Should see JSON response

### Test 4: Python Test
- [ ] Make sure server is running
- [ ] Open another terminal in project folder
- [ ] Run: `python test_api.py`
- [ ] Should see comprehensive test results

## ✅ Verify All Features

- [ ] ✓ Health endpoint works
- [ ] ✓ Status endpoint works
- [ ] ✓ Chat endpoint responds
- [ ] ✓ English messages work
- [ ] ✓ Hindi messages work
- [ ] ✓ Hinglish messages work
- [ ] ✓ Language detection correct
- [ ] ✓ Sources appear in responses
- [ ] ✓ Conversation history works
- [ ] ✓ Rate limiting works

## ✅ Troubleshooting Checklist

### If you see: "Connection refused"
- [ ] Check if server is running
- [ ] Check port in `.env` (default 5000)
- [ ] Check if port is available: `netstat -ano | findstr :5000` (Windows)

### If you see: "API Key not configured"
- [ ] Check `.env` file exists in project root
- [ ] Check `OPENROUTER_API_KEY` is not empty
- [ ] Check no extra spaces in key
- [ ] Restart server after editing `.env`

### If you see: "Port 5000 already in use"
- [ ] Edit `.env` and change: `PORT=8000`
- [ ] Restart server
- [ ] Access at: http://localhost:8000

### If you see: "No module named 'fastapi'"
- [ ] Check virtual environment is activated
- [ ] See `(venv)` at start of terminal line
- [ ] Run: `pip install -r requirements.txt`
- [ ] Try again

### If server won't start
- [ ] Check Python version: `python --version` (need 3.8+)
- [ ] Check dependencies: `pip install -r requirements.txt`
- [ ] Check `.env` file syntax
- [ ] Check logs in `app.log`
- [ ] Try: `python -m pip install --upgrade pip`

## ✅ Common Tasks

### Send a Message
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me about admissions"}'
```

### Get Conversation History
```bash
curl http://localhost:5000/conversations/conv_123
```

### Clear a Conversation
```bash
curl -X DELETE http://localhost:5000/conversations/conv_123
```

### View Live Logs
```bash
# Windows
type app.log

# macOS/Linux
tail -f app.log
```

### Stop the Server
- [ ] Press: `Ctrl + C` in the terminal

### Restart the Server
- [ ] Stop: `Ctrl + C`
- [ ] Wait 2 seconds
- [ ] Start: `python main.py` (or use start script)

## ✅ Before Sharing/Deploying

- [ ] Remove `.env` file (contains API key)
- [ ] Create `.env` from `.env.example` on deployment
- [ ] Set `DEBUG=False` in `.env`
- [ ] Test with production configuration
- [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Setup monitoring/logging
- [ ] Setup backup strategy
- [ ] Test error handling
- [ ] Load test the API
- [ ] Document any customizations

## ✅ Documentation to Read (In Order)

1. **First (5 min)**: [QUICKSTART.md](QUICKSTART.md)
2. **Then (10 min)**: [README.md](README.md) - Overview
3. **Details (30 min)**: [SETUP.md](SETUP.md) - Setup guide
4. **Reference (20 min)**: [SPECIFICATION.md](SPECIFICATION.md) - Technical spec
5. **For Production (30 min)**: [DEPLOYMENT.md](DEPLOYMENT.md)
6. **Overview**: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

## ✅ Key Endpoints to Know

| Endpoint | URL |
|----------|-----|
| Chat | POST /chat |
| Health | GET /health |
| Status | GET /status |
| Docs | GET /docs |
| History | GET /conversations/{id} |
| Clear | DELETE /conversations/{id} |

## ✅ Example Messages to Try

### English
- "What are the placement statistics?"
- "Tell me about scholarships"
- "What courses are available?"

### Hindi
- "प्रवेश के बारे में बताइये"
- "छात्रवृत्ति के बारे में बताइये"
- "कैंपस की सुविधाएं क्या हैं?"

### Hinglish
- "hostel ke baare mein batao"
- "fees ki structure kya hai?"
- "faculty members kaun hain?"

### Current News
- "What's new in AI technology?"
- "Tell me recent tech developments"
- "Latest news in 2025"

## ✅ Performance Optimization (Optional)

- [ ] Review `.env` settings
- [ ] Adjust `RATE_LIMIT_REQUESTS` if needed
- [ ] Adjust `MAX_CONVERSATION_HISTORY` if needed
- [ ] Set `LOG_LEVEL=WARNING` for production
- [ ] Monitor `app.log` for errors
- [ ] Check system resources: `free -h` (macOS/Linux)

## ✅ Final Verification

- [ ] Server running without errors
- [ ] API responding to requests
- [ ] Language detection working
- [ ] Responses are natural and contextual
- [ ] No errors in `app.log`
- [ ] Tests passing
- [ ] Documentation reviewed
- [ ] Ready for use/deployment

## 🎉 You're Done!

Your HU Voice AI API is now:
- ✅ Installed and configured
- ✅ Running and healthy
- ✅ Ready for testing
- ✅ Ready for integration
- ✅ Ready for deployment

## 📚 Next Steps

1. **Explore**: Use the API at http://localhost:5000/docs
2. **Test**: Run `python test_api.py` for comprehensive tests
3. **Integrate**: Use API endpoints in your applications
4. **Customize**: Modify university knowledge base in `main.py`
5. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production

## 🆘 Still Having Issues?

1. Check `.env` file configuration
2. Review logs in `app.log`
3. Read [SETUP.md](SETUP.md) troubleshooting section
4. Check internet connection
5. Verify OpenRouter API key is valid

---

**Congratulations! Your HU Voice AI API is ready! 🚀**

For detailed information, see:
- Quick questions? → [QUICKSTART.md](QUICKSTART.md)
- How to setup? → [SETUP.md](SETUP.md)
- How to use? → [README.md](README.md)
- Tech details? → [SPECIFICATION.md](SPECIFICATION.md)
- Production deployment? → [DEPLOYMENT.md](DEPLOYMENT.md)
