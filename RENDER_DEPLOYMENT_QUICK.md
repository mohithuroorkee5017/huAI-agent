# 🚀 QUICK START: Deploy to Render.com (RECOMMENDED)

## Why Render > Vercel?

✅ **Free tier** works perfectly for this project  
✅ **Python-first** platform (not Node.js)  
✅ **No timeouts** on responses  
✅ **Always-on services** (no cold starts)  
✅ **Built-in database** (PostgreSQL)  
✅ **Auto-deploy** from GitHub  
✅ **Better pricing** ($5+ instead of $20+)  

---

## 5-Minute Deployment

### Step 1: Create GitHub Repository

```powershell
cd "d:\Users\pop\Desktop\Haridwar University AI"
git init
git add .
git commit -m "Initial commit: Haridwar University AI full stack"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/haridwar-ai.git
git push -u origin main
```

### Step 2: Go to render.com

1. Sign up at **render.com** (use GitHub login)
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repository
4. Click **"Connect"**

### Step 3: Deploy Backend Service

**Fill in these settings:**

| Setting | Value |
|---------|-------|
| **Name** | `huvoice-api` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r api/requirements.txt` |
| **Start Command** | `cd api && uvicorn main:app --host 0.0.0.0 --port 8000` |
| **Free Plan** | Select (it's fine) |

**Add Environment Variables:**
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Click **"Deploy"** - Wait 2-5 minutes ⏳

When done, you'll see: `https://huvoice-api.onrender.com` ✅

### Step 4: Deploy Frontend Service

Back on Render dashboard, click **"New +"** → **"Web Service"** again

**Fill in these settings:**

| Setting | Value |
|---------|-------|
| **Name** | `huvoice-web` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python huvoice_agent.py` |
| **Free Plan** | Select |

**Add Environment Variables:**
```
HUVOICE_BACKEND_URL=https://huvoice-api.onrender.com
OPENROUTER_API_KEY=sk-or-v1-your-key-here
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
```

Click **"Deploy"** - Wait 2-5 minutes ⏳

When done, you'll see: `https://huvoice-web.onrender.com` ✅

---

## Step 5: Test Your Deployment

### Test Backend API:
```bash
curl -X POST https://huvoice-api.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello","conversation_id":"test"}'
```

Expected response:
```json
{"success":true,"answer":"...AI response..."}
```

### Test Frontend:
Open in browser: `https://huvoice-web.onrender.com`

Login and ask a question. You should see proper AI responses! 🎉

---

## Troubleshooting

### Problem: "No module named 'main'"
**Solution:** Make sure `cd api &&` is in Start Command

### Problem: Backend returns 503 error
**Solution:** Check API key is set in environment variables

### Problem: Frontend doesn't start
**Solution:** Check all requirements are in `requirements.txt`

### Problem: "Connection refused"
**Solution:** Make sure HUVOICE_BACKEND_URL uses full https URL

---

## Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **huvoice-api** | ✅ 750 hours/month | $7/month |
| **huvoice-web** | ✅ 750 hours/month | $7/month |
| **Database** | ✅ FREE PostgreSQL | Included |
| **Total** | **FREE** | **$14/month** |

You get **750 hours/month free** for each service = plenty for development!

---

## Keep Services Running 24/7

By default, free services sleep after 15 mins of inactivity. To keep them always on:

1. Go to your service dashboard
2. Click **Settings**
3. Under "Plan", click **"Upgrade"** to Paid ($7/month)

OR use a free uptime monitoring service to ping regularly.

---

## Next Steps

✅ Deploy now to Render  
✅ Test in browser  
✅ Share your URL with others  
✅ Monitor logs in Render dashboard  

**That's it! Your HUVoice AI is now live on the internet!** 🚀

---

## Alternative: Deploy to Railway.app

If you prefer Railway (also great):

1. Go to railway.app
2. Click "New Project"
3. Select "GitHub Repo"
4. Add environment variables
5. Deploy

Railway also offers a free tier and works great for Python!

---

**Ready? Let's deploy! 🚀**

