# HU Voice AI - Quick Testing & Deployment Guide

## 🚀 Quick Start - 5 Minutes

### Step 1: Verify Backend is Running
```bash
# Check if backend is accessible
curl http://localhost:5000/api/status
# Should return: {"status": "online", ...}
```

### Step 2: Open Frontend in Browser
```
http://localhost:3000/
or
http://your-domain.com/
```

### Step 3: Send a Test Message
1. Type: "What is HU Voice AI?"
2. Click **Send Button** (➤) or press **Enter**
3. Should see:
   - Message appears in chat
   - Loading spinner shows
   - API response appears below
   - Toast notification: "Message sent! ✓"

### Step 4: Check Console Logs
Press **F12** → **Console** tab
```
📤 Sending message (attempt 1/3)...
📥 Response received successfully
Message sent! ✓
```

---

## ✅ VERIFICATION CHECKLIST

### Desktop (Chrome/Firefox/Safari)
- [ ] Send button works
- [ ] Messages appear
- [ ] API responses show
- [ ] Toast notifications display
- [ ] Console logs show 📤📥✅

### Mobile (iOS iPhone 12+)
- [ ] Can tap send button
- [ ] Input box stays visible
- [ ] Keyboard doesn't cover input
- [ ] Messages send and appear
- [ ] Notch area respected

### Mobile (Android Galaxy S21+)
- [ ] Can tap send button  
- [ ] Input box stays visible
- [ ] Keyboard doesn't cover input
- [ ] Messages send and appear
- [ ] Safe areas respected

### Chat History
- [ ] Send 2-3 messages
- [ ] **Refresh page** (Ctrl+R)
- [ ] Previous messages should still appear
- [ ] Conversation ID should be the same

---

## 🔧 CONFIGURATION CHECKLIST

### Backend (.env)
```bash
✓ OPENROUTER_API_KEY=sk-...
✓ OPENROUTER_MODEL=openai/gpt-4o-mini
✓ RATE_LIMIT_ENABLED=true
✓ CORS_ORIGINS=*
```

### Frontend (static/script.js)
```javascript
✓ CONFIG.API_BASE_URL = window.location.origin
✓ CONFIG.API_TIMEOUT = 30000
✓ CONFIG.MAX_RETRIES = 3
```

### Deployment (Render/Railway/Vercel)
```bash
✓ Backend URL = https://your-app.onrender.com
✓ Frontend URL = https://your-app.onrender.com
✓ Same domain = CORS works automatically
```

---

## 🐛 TROUBLESHOOTING

### Problem: Send button doesn't work
**Check:**
1. Open DevTools Console (F12)
2. Look for error starting with ❌
3. Try clicking again, check for `📤 Submit button clicked`
4. **Solution**: Reload page, check if button is enabled

### Problem: No response from API
**Check:**
1. Console should show `📤 Sending message...`
2. Check if `📥 Response received` appears
3. If you see `🔄 Retrying in 1000ms`, network is slow
4. If you see `❌ All retries failed`, backend is down
5. **Solution**: Check backend status at `/api/status`

### Problem: Messages disappear after refresh
**Check:**
1. Is localStorage enabled? (DevTools → Application → LocalStorage)
2. Is conversation ID saved? Check: `localStorage.getItem('hu_voice_ai_conversation_id')`
3. Are messages in storage? Check: `localStorage.getItem('hu_voice_ai_chat_history')`
4. **Solution**: Clear localStorage and try again:
   ```javascript
   localStorage.clear()
   location.reload()
   ```

### Problem: Keyboard covers input on mobile
**Check:**
1. Is footer visible when keyboard opens?
2. Input box still accessible?
3. **Solution**: 
   - Make sure `.app-footer` has `flex-shrink: 0`
   - Check if `100dvh` is supported (older phones fallback to `100vh`)
   - Try in incognito mode to clear cache

### Problem: Toast notifications not showing
**Check:**
1. Is `toastContainer` element in HTML?
2. CSS for `.toast` exists?
3. Open DevTools, check for JavaScript errors
4. **Solution**: Reload and try sending message again

### Problem: Nothing works!
**Nuclear Option:**
```javascript
// In browser console
localStorage.clear()
location.reload()
```

---

## 📊 PERFORMANCE METRICS

### Expected Timings
- **API Request**: 1-3 seconds (with AI processing)
- **Retry Delay**: 1s, 2s, 4s (exponential backoff)
- **Timeout**: 30 seconds (aborts request)
- **Toast Display**: 5 seconds (auto-dismisses)
- **Status Check**: Every 30 seconds

### Browser Requirements
- **Minimum**: Chrome 88, Firefox 87, Safari 14, Edge 88
- **Recommended**: Latest version
- **Mobile**: iOS 14+, Android 8+

---

## 🔐 SECURITY NOTES

- ✅ API key stored on backend only (not exposed to frontend)
- ✅ CORS configured to allow frontend domain
- ✅ Rate limiting enabled (100 requests per 60 seconds per IP)
- ✅ Input validation on frontend and backend
- ✅ Error messages don't expose sensitive details
- ✅ All requests use HTTPS in production

---

## 📈 PRODUCTION DEPLOYMENT

### Render.com
```yaml
# render.yaml (included in project)
services:
  - type: web
    name: huvoice-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0
    
  - type: web
    name: huvoice-web
    env: static
    buildCommand: echo "Static files ready"
    staticPublishPath: .
```

### Environment Variables (Render)
Set in Dashboard → Environment:
```
OPENROUTER_API_KEY=your_key_here
DEBUG=false
LOG_LEVEL=INFO
```

### Verify Deployment
1. Visit: `https://your-app.onrender.com/api/status`
2. Should see: `{"status": "online", ...}`
3. Try sending message from frontend
4. Should work immediately

---

## 📱 MOBILE TESTING

### iOS (Safari)
1. Open: `https://your-app.com/`
2. Tap Send button → Should work
3. Open keyboard → Input should stay visible
4. Notch areas should have padding
5. Close app → Reopen → Messages persist

### Android (Chrome)
1. Open: `https://your-app.com/`
2. Tap Send button → Should work
3. Open keyboard → Input should stay visible
4. Bottom nav should not overlap
5. Close app → Reopen → Messages persist

---

## 💾 DATA STORAGE

### Browser LocalStorage
```
hu_voice_ai_conversation_id: "conv_1717420800_abc123"
hu_voice_ai_chat_history: {
  "conversationId": "conv_1717420800_abc123",
  "messages": [...],
  "timestamp": "2026-06-03T..."
}
```

### Max Storage: ~5MB per domain
- Enough for ~1000+ messages
- Auto-clears when user clicks "Clear History"

---

## 🎯 SUCCESS CRITERIA

Your implementation is working if:

1. ✅ Send button triggers message submission
2. ✅ Message appears immediately in chat
3. ✅ Loading spinner shows while processing
4. ✅ API response appears below user message
5. ✅ Toast notification shows "Message sent! ✓"
6. ✅ Console shows `📤` and `📥` logs
7. ✅ Refresh page → messages still there
8. ✅ Mobile keyboard doesn't cover input
9. ✅ Works on iPhone and Android
10. ✅ Errors show toast + console logs (not silent)

---

## 📞 DEBUGGING QUICK REFERENCE

| Symptom | Check | Fix |
|---------|-------|-----|
| Nothing happens | Console for errors | Reload page |
| Network 404 | API URL path | Check backend running |
| CORS error | Browser console | Set CORS_ORIGINS=* |
| No response | API timeout? | Check backend logs |
| Keyboard overlaps | DevTools mobile | Verify `100dvh` |
| No toast shown | Check HTML has container | Reload and retry |
| History lost | Check localStorage | Data stored after send |

---

## 🎓 LEARNING RESOURCES

### Understanding the Code

**Frontend (static/script.js)**:
- `submitQuestion()` = Main entry point for sending
- `sendMessageWithRetry()` = Handles API calls + retries
- `showToast()` = User notifications
- `loadChatHistory()` = Restore previous conversation
- Debug log pattern: `debugLog('📤 action:', 'level')`

**Backend (api/main.py)**:
- `@app.post("/chat")` = Chat endpoint
- `ChatRequest` model = Input validation
- `ChatResponse` model = Output format
- Error handlers = Graceful failure

### Key Concepts
- **localStorage API** = Persistent browser storage
- **fetch API** = Making HTTP requests
- **AbortController** = Request timeout handling
- **Exponential Backoff** = Retry with increasing delays
- **Toast Pattern** = Temporary notifications

---

**Last Updated**: June 3, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
