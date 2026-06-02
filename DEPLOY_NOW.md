# 🚀 Haridwar University AI - Deployment to Render.com

## Quick Deployment Guide (5 minutes)

---

## ✅ Step 1: Verify Local Setup (1 minute)

```bash
cd "d:\Users\pop\Desktop\HUVoice AI"
python test_unified_setup.py
```

**Expected output:**
```
✅ Import Check - PASS
✅ Environment Variables - PASS
✅ Project Structure - PASS
...
🎉 All tests passed!
```

If any test fails, fix it before deploying.

---

## ✅ Step 2: Prepare GitHub Repository (2 minutes)

### Option A: If you have NO GitHub yet

```bash
cd "d:\Users\pop\Desktop\HUVoice AI"

# Initialize git
git init
git add .
git commit -m "Haridwar University AI - Unified Flask Application"

# Create repo on GitHub.com first, then:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/haridwar-university-ai.git
git push -u origin main
```

### Option B: If you already have GitHub repo

```bash
cd "d:\Users\pop\Desktop\HUVoice AI"
git add .
git commit -m "Deploy unified Flask app to Render"
git push origin main
```

---

## ✅ Step 3: Deploy to Render (2 minutes)

### Step 3a: Sign Up / Login
1. Go to: **https://render.com**
2. Click **"Sign up"** (or login if you have account)
3. Use GitHub account (recommended)

### Step 3b: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect Repository"**
3. Select your GitHub repo: **haridwar-university-ai**
4. Click **"Connect"**

### Step 3c: Configure Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | haridwar-university-ai |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements-unified.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT app:app` |

### Step 3d: Add Environment Variables

Click **"Add Environment Variable"** and add these:

```
FLASK_ENV = production
OPENROUTER_API_KEY = sk-or-v1-YOUR_KEY_HERE
SECRET_KEY = (leave empty - Render will auto-generate)
```

⚠️ **IMPORTANT**: Get your OpenRouter API key from: https://openrouter.ai/keys

### Step 3e: Deploy

1. Scroll down
2. Click **"Create Web Service"**
3. Wait 2-5 minutes for deployment

---

## 🎉 Step 4: Verify Deployment

### Check Status
- Render dashboard shows **"Live"** ✅
- Your app URL appears (e.g., `https://haridwar-university-ai-xxxx.onrender.com`)

### Test Your App
1. Open the Render URL in browser
2. **Signup** with test account
3. **Login** 
4. **Chat** - Ask a question about admissions
5. Verify response appears ✅

---

## 📋 Deployment Checklist

Before deploying:
- [ ] Local tests pass (`python test_unified_setup.py`)
- [ ] app.py runs locally (`python app.py`)
- [ ] Code pushed to GitHub
- [ ] GitHub repo is public (or Render has access)
- [ ] OpenRouter API key ready

During deployment:
- [ ] Web Service created on Render
- [ ] Build command correct
- [ ] Start command correct
- [ ] Environment variables added
- [ ] OPENROUTER_API_KEY is set

After deployment:
- [ ] Status shows "Live"
- [ ] URL is accessible
- [ ] Signup works
- [ ] Chat works
- [ ] No errors in logs

---

## 🔗 Important Links

| Link | Purpose |
|------|---------|
| https://render.com | Render dashboard |
| https://github.com | GitHub (for code) |
| https://openrouter.ai/keys | Get API key |

---

## 📖 Deployment Files

| File | Purpose |
|------|---------|
| **app.py** | Main application |
| **requirements-unified.txt** | Dependencies |
| **render.yaml** | Auto-deploy config (optional) |
| **.env** | Local only (add to .gitignore) |
| **.gitignore** | Hide .env from GitHub |

---

## ⚠️ Common Issues

### Issue: "Build failed - pip install error"
**Solution**: Check requirements-unified.txt has all packages

### Issue: "OPENROUTER_API_KEY not found"
**Solution**: Add it to Render environment variables (Step 3d)

### Issue: "502 Bad Gateway"
**Solution**: 
- Wait 1 more minute (app might still starting)
- Check app.py syntax: `python -m py_compile app.py`
- Check logs in Render dashboard

### Issue: "Module not found"
**Solution**: Reinstall dependencies
```bash
pip install -r requirements-unified.txt
```

---

## 🧪 Test Your Deployment

### Test Signup
```bash
curl -X POST https://YOUR_RENDER_URL/api/signup \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Test Login
```bash
curl -X POST https://YOUR_RENDER_URL/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Test Chat
```bash
curl -X POST https://YOUR_RENDER_URL/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "What courses do you offer?"
  }'
```

---

## 💡 Pro Tips

1. **Auto-Deploy**: Push code to GitHub → Render auto-deploys
2. **Free Tier**: Works for development/demo
3. **Custom Domain**: Add later in Render settings
4. **Logs**: Check Render dashboard for errors
5. **Uptime**: Free tier sleeps after 15 min inactivity (use UptimeRobot to prevent)

---

## 🎯 Final Steps

### After Deployment Works:

1. **Test thoroughly** on production URL
2. **Share with team** 
3. **Set up monitoring** (optional):
   - https://uptimerobot.com (keeps app awake)
   - Google Analytics (track usage)
4. **Add custom domain** (optional):
   - Buy domain (godaddy, namecheap, etc.)
   - Point to Render URL
5. **Enable auto-deploy**:
   - Every GitHub push automatically redeploys

---

## 🚨 Need Help?

1. **Check logs**: Render dashboard → Logs tab
2. **Verify API key**: Make sure OPENROUTER_API_KEY is set
3. **Test locally**: Run `python app.py` first
4. **Check GitHub**: Ensure code is pushed
5. **Render docs**: https://docs.render.com

---

## ✅ Success Indicators

✅ App is "Live" on Render  
✅ URL loads in browser  
✅ Signup/Login works  
✅ Chat responds with AI answers  
✅ No 502/503 errors  
✅ Console shows no errors  

---

**Ready? Follow the 4 steps above!** 🚀

