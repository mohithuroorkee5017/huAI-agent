# 🚀 Deployment Options for Haridwar University AI

## ⚠️ Important: This is a 2-Service Application

Haridwar University AI requires:
- **FastAPI backend** (port 8000)
- **Flask frontend** (port 5000)

These need to run **simultaneously**. Choose your platform based on this requirement.

---

## 🥇 Option 1: Render.com (RECOMMENDED for Python)

### Why Render is Best:
✅ Native Python support  
✅ Can run multiple services  
✅ Free tier available  
✅ PostgreSQL database included  
✅ Environment variables management  
✅ Auto-deploy from GitHub  

### Setup Steps:

**1. Create GitHub Repository**
```bash
cd "d:\Users\pop\Desktop\Haridwar University AI"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/haridwar-ai.git
git push -u origin main
```

**2. Go to render.com**
- Sign up with GitHub
- Create new service: Web Service
- Connect your repository

**3. Create Two Services:**

**Service 1 - Backend:**
- Name: `haridwar-api`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `cd api && uvicorn main:app --host 0.0.0.0 --port 8000`
- Port: `8000`

**Service 2 - Frontend:**
- Name: `haridwar-web`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python huvoice_agent.py`
- Port: `5000`
- Environment Variables:
  ```
  HARIDWAR_BACKEND_URL=https://haridwar-api.onrender.com
  OPENROUTER_API_KEY=your_key_here
  ```

### Cost: FREE (with limitations)

---

## 🥈 Option 2: Railway.app (EASY Setup)

### Why Railway:
✅ Simple GitHub integration  
✅ Great for Python microservices  
✅ Pay-as-you-go pricing  
✅ Built-in database support  
✅ Easy environment management  

### Setup:
1. Go to railway.app
2. Create project
3. Connect GitHub repo
4. Deploy as Python app
5. Set environment variables

### Cost: $5-20/month for 2 services

---

## 🥉 Option 3: PythonAnywhere

### Why PythonAnywhere:
✅ Purpose-built for Python  
✅ Very beginner-friendly  
✅ No credit card for free tier  
✅ Web framework support built-in  

### Setup:
1. Go to pythonanywhere.com
2. Create account
3. Upload files
4. Configure WSGI
5. Start web app

### Cost: FREE ($5-15/month for production)

---

## ❌ Option 4: Vercel (NOT Recommended for This Project)

### Why Vercel is Difficult:
⚠️ Primarily designed for Node.js  
⚠️ Python support is limited to serverless functions  
⚠️ Can't easily run two simultaneous services  
⚠️ Cold starts cause delays  
⚠️ Not ideal for real-time chat  

### If you still want Vercel:
See `VERCEL_DEPLOYMENT.md`

---

## 🎯 Recommended Path:

### For Beginners:
**→ Use PythonAnywhere (easiest)**

### For Best Performance:
**→ Use Render.com (free tier works great)**

### For Production:
**→ Use Railway.app or AWS**

---

## Environment Variables Needed:

For any platform, you'll need:

```
OPENROUTER_API_KEY=sk-or-v1-...your-key...
HARIDWAR_BACKEND_URL=https://your-backend-url
HARIDWAR_FRONTEND_URL=https://your-frontend-url
SECRET_KEY=random-secret-key
FLASK_ENV=production
```

---

## Quick Deployment Checklist:

- [ ] Push code to GitHub
- [ ] Create account on chosen platform
- [ ] Connect GitHub repository
- [ ] Set environment variables
- [ ] Configure start commands
- [ ] Deploy
- [ ] Test endpoints
- [ ] Monitor logs

