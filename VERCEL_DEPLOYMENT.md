# 🚀 Vercel Deployment Guide for Haridwar University AI

## ⚠️ IMPORTANT: Vercel Limitations

Vercel has **significant limitations** for this project:

1. **No persistent processes** - Can't run backend 24/7
2. **Serverless functions timeout** - 60 seconds max
3. **Cold starts** - Delays in responses
4. **Limited to stateless functions** - Conversation memory won't persist
5. **Not ideal for Python microservices**

### Better Alternative: [Use Render.com (See DEPLOYMENT_OPTIONS.md)](#-option-1-rendercom-recommended-for-python)

---

## If You Still Want to Use Vercel...

### Prerequisites:
- [ ] GitHub account with your code pushed
- [ ] Vercel account (vercel.com)
- [ ] OpenRouter API key

### Step 1: Prepare Project Structure

Create `api/handler.py`:
```python
# Vercel serverless function for FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Create `api.py` (for Flask):
```python
# Vercel serverless function for Flask
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from huvoice_agent import app

# Export for Vercel
handler = app
```

### Step 2: Create vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "huvoice_agent.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "huvoice_agent.py"
    }
  ],
  "env": {
    "OPENROUTER_API_KEY": "@openrouter_api_key",
    "HUVOICE_BACKEND_URL": "@huvoice_backend_url",
    "SECRET_KEY": "@secret_key"
  }
}
```

### Step 3: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# Follow prompts and set environment variables
```

### Step 4: Configure Environment Variables in Vercel Dashboard

1. Go to vercel.com/dashboard
2. Select your project
3. Settings → Environment Variables
4. Add:
   - `OPENROUTER_API_KEY`: Your API key
   - `HUVOICE_BACKEND_URL`: https://your-project.vercel.app
   - `SECRET_KEY`: Random string

### Step 5: Test

```bash
curl https://your-project.vercel.app/api/status
```

---

## Expected Issues & Solutions

### Issue 1: Timeout (60 seconds)
**Problem:** Requests over 60 seconds fail  
**Solution:** Not fixable on Vercel. Use Render instead.

### Issue 2: Cold Starts
**Problem:** First request takes 10-30 seconds  
**Solution:** Not fixable on Vercel. Use Railway instead.

### Issue 3: Memory Issues
**Problem:** ML models consume too much memory  
**Solution:** Upgrade Vercel Pro or use different platform

### Issue 4: No Persistent Storage
**Problem:** Conversation history lost after restart  
**Solution:** Add Redis/Database (not easy on Vercel)

---

## 🚨 Recommended: Use Render.com Instead

Vercel will NOT work well for this project. Here's why:

| Feature | Vercel | Render | Railway |
|---------|--------|--------|---------|
| Python Support | ⚠️ Limited | ✅ Full | ✅ Full |
| Always-On Backend | ❌ No | ✅ Yes | ✅ Yes |
| Timeout | ⚠️ 60s | ✅ None | ✅ None |
| Cost | $20+/month | FREE tier | $5-20/month |
| Best For | Node.js | Python | Microservices |

### Quick Render Setup (Recommended):

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial"
git push -u origin main

# 2. Go to render.com
# 3. Create new Web Service
# 4. Connect GitHub repo
# 5. Configure:
#    - Build: pip install -r requirements.txt && pip install -r api/requirements.txt
#    - Start: python huvoice_agent.py
# 6. Set environment variables
# 7. Deploy
```

That's it! No complex configuration needed.

---

## Summary

| Platform | Effort | Cost | Recommendation |
|----------|--------|------|-----------------|
| **Vercel** | 🟡 Medium | 🔴 Expensive | ❌ NOT recommended |
| **Render** | 🟢 Easy | 🟢 FREE | ✅ BEST CHOICE |
| **Railway** | 🟢 Easy | 🟡 $5-20/mo | ✅ GOOD CHOICE |
| **PythonAnywhere** | 🟢 Easy | 🟡 $5-15/mo | ✅ GOOD CHOICE |

**Recommendation: Use Render.com - It's free and takes 10 minutes!**

