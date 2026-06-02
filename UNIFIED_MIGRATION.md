# 🔄 Unified App: FastAPI → Flask Migration Guide

## What Happened?

The Haridwar University AI project has been **consolidated from 2 services into 1 unified Flask application**.

### Before Merge (2 Services)
```
📦 Project Structure
├── api/
│   ├── main.py (FastAPI on port 8000)
│   ├── services/
│   │   ├── openrouter.py
│   │   ├── memory.py
│   │   └── ...
│   └── requirements.txt
├── huvoice_agent.py (Flask on port 5000)
├── requirements.txt
└── templates/
```

**To run locally:**
```bash
# Terminal 1: Start FastAPI backend
cd api
python -m uvicorn main:app --port 8000

# Terminal 2: Start Flask frontend
cd ..
python huvoice_agent.py
```

---

### After Merge (1 Service)
```
📦 Project Structure
├── app.py (Unified Flask app)
├── requirements-unified.txt
├── render.yaml
└── templates/
    ├── index.html
    ├── dashboard.html
    └── login.html
```

**To run locally:**
```bash
# Single command - that's it!
python app.py
```

---

## 🎯 Key Changes

### Code Consolidation

| Component | Before | After |
|-----------|--------|-------|
| **AI Processing** | `api/main.py` (FastAPI) | `app.py` (Flask route `/api/chat`) |
| **Memory/History** | `api/services/memory.py` | `app.py` (ConversationMemory class) |
| **Language Detection** | `api/services/openrouter.py` | `app.py` (LanguageDetector class) |
| **OpenRouter AI** | `api/services/openrouter.py` | `app.py` (OpenRouterService class) |
| **Web Search** | `api/services/search.py` | `app.py` (SearchService class) |
| **Wikipedia** | `api/services/wiki.py` | `app.py` (WikipediaService class) |
| **Dashboard** | `huvoice_agent.py` (Flask routes) | `app.py` (Flask routes) |
| **Authentication** | `huvoice_agent.py` | `app.py` |

### Port Configuration

| Before | After |
|--------|-------|
| Port 5000 (Flask) | PORT environment variable |
| Port 8000 (FastAPI) | (merged into PORT) |
| Hardcoded localhost | Uses dynamic PORT from Render |

### API Endpoints (No Changes to Frontend)

All endpoints remain the same! The frontend doesn't need changes:

```
✅ Same endpoints:
/api/login
/api/signup
/api/chat
/api/ask
/api/history
/api/clear-history
/api/image
/api/voice-input
/webhook/<id>
```

---

## 🚀 Local Testing

### Prerequisites
```bash
pip install -r requirements-unified.txt
```

### Run Unified App
```bash
python app.py
```

### Expected Output
```
============================================================
✓ HARIDWAR UNIVERSITY AI - Starting Application
✓ Port: 5000
✓ Debug Mode: True
✓ Flask/Unified Application Mode
============================================================
 * Running on http://127.0.0.1:5000
```

### Test Endpoints
```bash
# 1. Open browser
http://localhost:5000

# 2. Signup
http://localhost:5000/api/signup (POST)
{
  "fullname": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}

# 3. Chat
http://localhost:5000/api/chat (POST)
{
  "message": "Hello! Tell me about admissions"
}
```

---

## 📁 Files Involved

### New Files Created
- ✅ `app.py` - Unified Flask application (merged)
- ✅ `requirements-unified.txt` - Updated dependencies
- ✅ `render.yaml` - Render deployment config
- ✅ `DEPLOYMENT_UNIFIED.md` - Deployment instructions
- ✅ `UNIFIED_MIGRATION.md` - This file

### Files to Keep
- ✅ `templates/` - HTML templates (unchanged)
- ✅ `static/` - CSS/JS (unchanged)
- ✅ `users.json` - User database (unchanged)

### Old Files (Can be archived/deleted)
- ❌ `huvoice_agent.py` - Merged into app.py
- ❌ `api/main.py` - Merged into app.py
- ❌ `api/services/` - Merged into app.py
- ❌ `api/requirements.txt` - Replaced by requirements-unified.txt
- ❌ `requirements.txt` - Replaced by requirements-unified.txt

---

## 🔧 What's Inside app.py

### 1. Imported Services (Consolidated)
```python
class LanguageDetector        # Detect language
class ConversationMemory      # Store chat history
class OpenRouterService       # Call OpenRouter API
class SearchService           # DuckDuckGo search
class WikipediaService        # Wikipedia lookup
```

### 2. Flask Routes
```python
/                            # Login page
/dashboard                   # Dashboard (requires login)
/api/login                   # Authentication
/api/signup                  # New account
/api/logout                  # Logout
/api/chat                    # Main chat (merged from FastAPI)
/api/history                 # Get history
/api/image                   # Image analysis
/webhook/<id>                # Public webhook
```

### 3. Knowledge Base
```python
UNIVERSITY_KB                # Haridwar University info
get_university_knowledge()   # Search function
```

---

## 📊 Data Flow (Before vs After)

### Before Merge
```
User Browser
    ↓ (HTTP POST /api/ask)
Flask App (port 5000)
    ↓ (requests.post to localhost:8000)
FastAPI Backend (port 8000)
    ↓ (OpenRouter API)
OpenRouter AI
    ↓ (response)
FastAPI Backend
    ↓ (JSON response)
Flask App
    ↓ (HTTP response)
User Browser
```

**Problems:**
- ❌ 2 services to run
- ❌ Complex localhost communication
- ❌ Hard to deploy
- ❌ Port conflicts on single-port platforms

---

### After Merge
```
User Browser
    ↓ (HTTP POST /api/chat)
Flask App (single port)
    ├─ Route handler (Flask)
    ├─ Language detection (LanguageDetector)
    ├─ Memory lookup (ConversationMemory)
    ├─ AI processing (OpenRouterService)
    └─ Response (JSON)
    ↓ (internal service calls)
OpenRouter AI + Wikipedia + DuckDuckGo
    ↓ (response)
Flask App (internal)
    ↓ (HTTP response)
User Browser
```

**Benefits:**
- ✅ 1 service to run
- ✅ No localhost communication
- ✅ Easy to deploy (1 Web Service)
- ✅ Works on any port
- ✅ Cleaner code

---

## 🔐 Environment Variables

### Same as Before
```
OPENROUTER_API_KEY=sk-or-v1-...    # Required for AI
SECRET_KEY=...                      # Flask session key
FLASK_ENV=production                # For production
```

### New/Changed
```
PORT=8000                           # Set by Render (was hardcoded)
# (no more HUVOICE_BACKEND_URL needed)
```

---

## ✅ Verification Checklist

After running `python app.py`:

- [ ] Server starts on http://localhost:5000
- [ ] Login page loads
- [ ] Signup creates account
- [ ] Login works
- [ ] Chat endpoint responds
- [ ] History shows messages
- [ ] Clear history works
- [ ] Frontend UI unchanged
- [ ] No errors in console

---

## 🚨 Common Issues

### Issue: "Module not found: openrouter"
**Cause**: Old imports from api/services still in code
**Solution**: Use new `app.py` which has everything built-in

### Issue: "Connection refused on localhost:8000"
**Cause**: Still trying to call FastAPI backend
**Solution**: app.py handles everything internally - no backend needed

### Issue: "PORT already in use"
**Solution**: 
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
python app.py --port 8080
```

### Issue: "OPENROUTER_API_KEY not found"
**Solution**: 
```bash
# Make sure .env file has:
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
```

---

## 📚 Migration Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Servers** | 2 (FastAPI + Flask) | 1 (Flask) |
| **Ports** | 5000 + 8000 | Dynamic (PORT env var) |
| **Services** | Separate files | Merged in app.py |
| **Startup** | 2 terminals | 1 terminal |
| **Deployment** | Complex | Simple |
| **Code** | Split across 2 projects | Unified in 1 app.py |
| **API Compatibility** | Same | Same ✅ |
| **UI/Frontend** | Same | Same ✅ |

---

## 🎓 Learning Points

### Why Merge into Flask?

1. **Render.com Simplicity**: Free tier = 1 free service
2. **No Cold Starts**: Both services run always
3. **No IPC Issues**: No inter-process communication
4. **Easier Debugging**: Single codebase
5. **Better Performance**: No HTTP overhead between services

### When Would You Use 2 Services?

1. Different scaling needs
2. Multiple team members
3. Different deployment strategies
4. Performance bottlenecks

---

## 📖 Documentation Files

- **DEPLOYMENT_UNIFIED.md** - How to deploy to Render
- **UNIFIED_MIGRATION.md** - This file (what changed)
- **app.py** - Main application code
- **requirements-unified.txt** - All dependencies
- **render.yaml** - Render deployment config

---

## 🎉 You're Ready!

The unified app is ready to:
1. ✅ Run locally: `python app.py`
2. ✅ Deploy to Render: Follow DEPLOYMENT_UNIFIED.md
3. ✅ Scale to production: Add monitoring, analytics, etc.

**Questions?** Check app.py comments or test endpoints!

