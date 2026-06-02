# 🚀 Haridwar University AI - Unified Flask Application

**Status**: ✅ Ready to deploy | Single Service | FastAPI ↔️ Flask Merged

> **What's New?** FastAPI backend + Flask dashboard are now ONE unified Flask application. See `UNIFIED_MIGRATION.md` for details.

---

## 📋 Quick Start

### 1. Install Dependencies
```bash
cd "d:\Users\pop\Desktop\Haridwar University AI"
pip install -r requirements-unified.txt
```

### 2. Set Up Environment
Create `.env` file (if not exists):
```
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

Get API key from: https://openrouter.ai/keys

### 3. Run Locally
```bash
python app.py
```

Open browser: http://localhost:5000

### 4. Test
1. **Signup**: Create new account
2. **Login**: Use your credentials
3. **Chat**: Ask "Tell me about admissions"
4. **History**: View conversation

---

## 📁 Project Structure

```
Haridwar University AI/
├── app.py                      # 🎯 Main unified Flask app
├── requirements-unified.txt    # ✅ Single requirements file
├── render.yaml                 # 🌐 Render deployment config
│
├── templates/                  # 🖼️ HTML files
│   ├── index.html             # Login page
│   ├── dashboard.html         # Main interface
│   └── login.html             # Login form
│
├── static/                     # 📦 CSS/JS
│   ├── style.css
│   └── script.js
│
├── users.json                  # 👥 User database
├── .env                        # 🔑 Environment variables
│
├── DEPLOYMENT_UNIFIED.md       # 🚀 Render deployment guide
├── UNIFIED_MIGRATION.md        # 🔄 What changed
└── README.md                   # 📖 (this file)
```

---

## 🎯 Available Features

| Feature | Status | Notes |
|---------|--------|-------|
| **Login/Signup** | ✅ Working | Users stored in JSON |
| **Chat** | ✅ Working | OpenRouter API integration |
| **History** | ✅ Working | Per-user conversation history |
| **University KB** | ✅ Working | Admissions, placements, fees, etc. |
| **Web Search** | ✅ Working | DuckDuckGo integration |
| **Wikipedia** | ✅ Working | Multilingual support |
| **Language Detection** | ✅ Working | English, Hindi, Hinglish |
| **Image Analysis** | ⏳ Placeholder | Coming soon |
| **Voice Input** | ⏳ Placeholder | Browser microphone (planned) |

---

## 🔌 API Endpoints

All endpoints run on **single Flask app** (no separate backend needed):

```bash
# Authentication
POST   /api/signup              # Create account
POST   /api/login               # Login
POST   /api/logout              # Logout

# Chat & AI
POST   /api/chat                # Send message (MAIN ENDPOINT)
POST   /api/ask                 # Alias for /chat
GET    /api/history             # Get conversation history
POST   /api/clear-history       # Clear history

# Status
GET    /api/status              # Get app status

# Image & Voice
POST   /api/image               # Upload image (placeholder)
POST   /api/voice-input         # Voice input (placeholder)

# Public
POST   /webhook/<id>            # Webhook endpoint
GET    /webhook/<id>            # Webhook GET
```

---

## 🧪 Test in Terminal

### Test Chat Endpoint
```bash
# 1. Create account
curl -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "John Doe",
    "email": "john@test.com",
    "password": "test123"
  }'

# 2. Login & get session
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@test.com",
    "password": "test123"
  }'

# 3. Send message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "What is the admission process?"
  }'
```

---

## 🌐 Deploy to Render

### Quick Deploy (5 minutes):

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Unified Flask app ready for deployment"
   git push origin main
   ```

2. **Go to Render.com** → New Web Service
   - Select GitHub repo
   - Runtime: Python 3
   - Build: `pip install -r requirements-unified.txt`
   - Start: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

3. **Add Environment Variables**
   ```
   FLASK_ENV = production
   OPENROUTER_API_KEY = sk-or-v1-...
   ```

4. **Deploy!** → Wait 2-5 minutes

**Full guide**: See `DEPLOYMENT_UNIFIED.md`

---

## 📊 What Changed (Merge Summary)

### Before (2 Services)
- ❌ `api/main.py` (FastAPI on port 8000)
- ❌ `huvoice_agent.py` (Flask on port 5000)
- ❌ 2 requirements files
- ❌ 2 terminal windows

### After (1 Service)
- ✅ `app.py` (Unified Flask)
- ✅ `requirements-unified.txt`
- ✅ 1 terminal window
- ✅ Same API endpoints
- ✅ Same UI/UX

**All user-facing functionality is identical!** The merge is purely backend consolidation.

---

## 🔐 Security Checklist

- [ ] `.env` file in `.gitignore` (never commit API keys)
- [ ] Strong SECRET_KEY set in production
- [ ] OPENROUTER_API_KEY stored in environment variables
- [ ] FLASK_ENV=production in production
- [ ] No debug mode in production
- [ ] HTTPS enabled (Render provides automatically)

---

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Need 3.8+

# Check dependencies
pip install -r requirements-unified.txt

# Check .env file
cat .env  # Should have OPENROUTER_API_KEY
```

### Chat not working
```bash
# Check logs
# Look for error messages in console

# Verify API key
echo $OPENROUTER_API_KEY

# Test API key
curl -H "Authorization: Bearer sk-or-v1-..." \
  https://openrouter.ai/api/v1/models
```

### Port already in use
```bash
# Windows: Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or run on different port
python app.py --port 8080
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **app.py** | Main application code |
| **UNIFIED_MIGRATION.md** | What changed in the merge |
| **DEPLOYMENT_UNIFIED.md** | How to deploy to Render |
| **requirements-unified.txt** | All Python dependencies |
| **render.yaml** | Render deployment config |

---

## 🎓 Architecture

```
┌─────────────────────────────────────────┐
│        Haridwar University AI            │
│        (Unified Flask Application)       │
├─────────────────────────────────────────┤
│                                         │
│  Web Interface                          │
│  ├─ Login/Signup (templates)            │
│  ├─ Dashboard UI (templates)            │
│  └─ Static files (CSS/JS)               │
│                    ↓                    │
│  Flask Routes (/api/*)                  │
│  ├─ Authentication routes               │
│  ├─ Chat endpoint (MAIN)                │
│  ├─ History management                  │
│  └─ Webhook handlers                    │
│                    ↓                    │
│  Core Services (Python Classes)         │
│  ├─ LanguageDetector                    │
│  ├─ ConversationMemory                  │
│  ├─ OpenRouterService (AI)              │
│  ├─ SearchService (Web)                 │
│  └─ WikipediaService                    │
│                    ↓                    │
│  External APIs                          │
│  ├─ OpenRouter (AI responses)           │
│  ├─ Wikipedia (Knowledge)               │
│  └─ DuckDuckGo (Web search)             │
│                                         │
└─────────────────────────────────────────┘
        ↑ Single PORT (Flask app) ↑
```

---

## 🚀 Ready to Deploy!

The unified Flask application is production-ready for:
- ✅ Local development (`python app.py`)
- ✅ Render.com deployment (single Web Service)
- ✅ Docker deployment (create Dockerfile)
- ✅ Traditional servers (gunicorn)

---

## 🤝 Contributing

To add features:

1. **Edit app.py** - Add new routes or services
2. **Test locally** - Run `python app.py`
3. **Test endpoints** - Use curl or browser
4. **Deploy** - Push to GitHub, Render redeploys automatically

---

## 📞 Support

**Errors?** Check:
1. Console output (`python app.py`)
2. Browser console (F12 → Console)
3. Network tab (F12 → Network)
4. `.env` file for missing variables

---

## 🎉 You're All Set!

Start developing: `python app.py`

Deploy to production: Follow `DEPLOYMENT_UNIFIED.md`

Questions? Check `UNIFIED_MIGRATION.md` for architecture details.

