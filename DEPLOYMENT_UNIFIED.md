# 🚀 Deployment Guide: Haridwar University AI (Unified Flask)

## Overview

This guide explains how to deploy the **unified Haridwar University AI** application to **Render.com**. This is a single Flask web service that combines the FastAPI backend and Flask dashboard into one application.

---

## ✨ What Changed

### Before (2 Services):
- ❌ FastAPI backend on port 8000 (`api/main.py`)
- ❌ Flask dashboard on port 5000 (`huvoice_agent.py`)
- ❌ Complex localhost communication
- ❌ Difficult to deploy (multiple services)

### After (1 Unified Service):
- ✅ Single Flask application (`app.py`)
- ✅ Dashboard UI + AI backend merged
- ✅ Single PORT environment variable
- ✅ Easy to deploy (1 web service)
- ✅ All endpoints in `/api/*` routes

---

## 📋 Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Render.com Account** - Free tier available at https://render.com
3. **OpenRouter API Key** - Get from https://openrouter.ai/keys

---

## 🔧 Step 1: Local Testing

Before deploying, test the unified app locally:

```bash
cd "d:\Users\pop\Desktop\Haridwar University AI"

# Install unified requirements
pip install -r requirements-unified.txt

# Run the app
python app.py
```

Expected output:
```
============================================================
✓ HARIDWAR UNIVERSITY AI - Starting Application
✓ Port: 5000
✓ Debug Mode: True
✓ Flask/Unified Application Mode
============================================================
 * Running on http://127.0.0.1:5000
```

Test in browser: http://localhost:5000

---

## 📤 Step 2: Push to GitHub

```powershell
cd "d:\Users\pop\Desktop\Haridwar University AI"

# Initialize git (if not already done)
git init

# Stage all files
git add .

# Commit with message
git commit -m "Merge FastAPI backend and Flask dashboard into unified Flask app"

# Set main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/haridwar-university-ai.git

# Push to GitHub
git push -u origin main
```

---

## 🌐 Step 3: Deploy to Render.com

### 3.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easier)
3. Authorize Render to access your GitHub repos

### 3.2 Create New Web Service
1. Go to Dashboard → New +
2. Select "Web Service"
3. Select your GitHub repository: `haridwar-university-ai`
4. Connect repository

### 3.3 Configure Service
Fill in the configuration form:

| Field | Value |
|-------|-------|
| **Name** | `haridwar-university-ai` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements-unified.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT app:app` |
| **Plan** | `Free` (for testing) |

### 3.4 Add Environment Variables
Click "Advanced" → "Add Environment Variable"

Add these variables:

```
FLASK_ENV = production
OPENROUTER_API_KEY = sk-or-v1-YOUR_KEY_HERE
SECRET_KEY = (auto-generated, leave empty)
```

**To get OPENROUTER_API_KEY:**
1. Go to https://openrouter.ai/keys
2. Copy your API key
3. Paste in Render environment variable

### 3.5 Deploy
1. Scroll to bottom → "Create Web Service"
2. Render will start building (2-5 minutes)
3. View logs in real-time
4. Wait for "✓ Your service is live"

---

## ✅ Step 4: Verify Deployment

Once deployment completes:

1. **Check Service URL**: Look for "Your service is live at:" with URL like:
   ```
   https://haridwar-university-ai-xxxx.onrender.com
   ```

2. **Test in Browser**:
   - Open https://haridwar-university-ai-xxxx.onrender.com
   - Should see login page
   - Try signup → login → chat

3. **Test API Directly**:
   ```bash
   # Create an account first via web UI
   # Then test chat endpoint
   curl -X POST https://haridwar-university-ai-xxxx.onrender.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"Hello"}'
   ```

---

## 🔑 Key Endpoints (After Merge)

All endpoints are now in the single Flask app:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Login page |
| `/dashboard` | GET | Main dashboard (requires login) |
| `/api/signup` | POST | Create account |
| `/api/login` | POST | Login |
| `/api/logout` | POST | Logout |
| `/api/chat` | POST | Send message & get AI response |
| `/api/ask` | POST | Ask question (alias for /chat) |
| `/api/history` | GET | Get conversation history |
| `/api/clear-history` | POST | Clear history |
| `/api/status` | GET | Get app status |
| `/api/image` | POST | Image analysis |
| `/api/voice-input` | POST | Voice input (placeholder) |
| `/webhook/<id>` | POST | Public webhook endpoint |

---

## 📊 Architecture (Unified)

```
┌─────────────────────────────────────┐
│   Render.com (Single Web Service)   │
├─────────────────────────────────────┤
│                                     │
│    app.py (Unified Flask)           │
│  ┌──────────────────────────────┐   │
│  │ Flask Routing               │   │
│  │ • /dashboard                │   │
│  │ • /api/chat                 │   │
│  │ • /api/login                │   │
│  │ • /api/image                │   │
│  └──────────────────────────────┘   │
│              ↓                      │
│  ┌──────────────────────────────┐   │
│  │ Unified Services             │   │
│  │ • LanguageDetector           │   │
│  │ • ConversationMemory         │   │
│  │ • OpenRouterService (AI)     │   │
│  │ • SearchService (Web)        │   │
│  │ • WikipediaService           │   │
│  └──────────────────────────────┘   │
│              ↓                      │
│  ┌──────────────────────────────┐   │
│  │ External APIs                │   │
│  │ • OpenRouter (AI)            │   │
│  │ • Wikipedia                  │   │
│  │ • DuckDuckGo (Search)        │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
      ↑ HTTPS ↑
      └───────┘
    Web Browser (User)
```

---

## 🐛 Troubleshooting

### Issue: "Build failed"
**Solution**: Check logs in Render dashboard
```bash
# Common causes:
# 1. requirements-unified.txt not found
# 2. Missing Python version specification
# 3. pip install failed
```

### Issue: "Internal Server Error"
**Solution**: Check runtime logs
1. Go to Render Dashboard → your service
2. Click "Logs" tab
3. Look for error messages
4. Common: Missing OPENROUTER_API_KEY environment variable

### Issue: "Module not found" errors
**Solution**: Ensure requirements-unified.txt is complete
```bash
pip freeze > requirements-unified.txt
```

### Issue: Slow response times
**Solution**: Increase number of workers in start command
```
gunicorn -w 8 -b 0.0.0.0:$PORT app:app
```

### Issue: Service goes to sleep (Free tier)
**Solution**: Set up uptime monitoring
- Use https://uptimerobot.com (free)
- Ping your service every 30 minutes
- Prevents Render free tier auto-sleep

---

## 📝 Environment Variables Reference

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `OPENROUTER_API_KEY` | Yes | `sk-or-v1-...` | Get from openrouter.ai |
| `FLASK_ENV` | No | `production` | Leave empty or set to production |
| `SECRET_KEY` | No | (auto) | Flask session key (auto-generated recommended) |
| `PORT` | No | `8000` | Render sets this automatically |

---

## 🚀 Production Checklist

- [ ] Code pushed to GitHub
- [ ] render.yaml or Web Service created on Render
- [ ] OPENROUTER_API_KEY configured
- [ ] FLASK_ENV set to "production"
- [ ] Service deployed successfully
- [ ] Login page loads
- [ ] Signup works
- [ ] Chat endpoint responds
- [ ] Uptime monitoring configured (optional)
- [ ] Custom domain added (optional)

---

## 📞 Support

**If deployment fails:**

1. Check Render logs (Dashboard → Logs)
2. Check GitHub Actions (if using CI/CD)
3. Verify all environment variables are set
4. Ensure requirements-unified.txt is in root directory
5. Check that app.py exists in root directory

---

## 🎉 Success!

Your Haridwar University AI is now live on Render.com! 🚀

**Your public URL**: https://haridwar-university-ai-xxxx.onrender.com

Share this URL with users to access your AI assistant!

---

## 🔄 Updates & Redeployment

To update your deployed app:

1. Make changes locally
2. Test with `python app.py`
3. Commit and push to GitHub
4. Render auto-deploys on push (if enabled)
5. Or manually re-deploy from Render dashboard

---

## 💡 Next Steps

1. **Scale up**: Upgrade to paid plan for better performance
2. **Add domain**: Connect custom domain (e.g., ai.yourdomain.com)
3. **SSL certificate**: Render auto-provides HTTPS
4. **Monitoring**: Set up error tracking (Sentry, etc.)
5. **Analytics**: Add user analytics (Mixpanel, Amplitude, etc.)

