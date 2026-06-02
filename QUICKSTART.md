# ⚡ QUICKSTART - Get HUVOICE AGENT Running in 5 Minutes

## 🎯 Your Goal
Start the HUVOICE AGENT voice assistant and ask it questions.

---

## ✅ Prerequisites
- Windows/Mac/Linux computer
- Python 3.8+ installed ([Download Python](https://www.python.org/downloads/))
- Internet connection
- Microphone (optional, for voice input)

---

## 🚀 Step 1: Prepare (1 minute)

### On Windows:
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project folder:
   ```bash
   cd "d:\Users\pop\Desktop\HUVoice AI"
   ```

### On Mac/Linux:
1. Open **Terminal**
2. Navigate to the project folder:
   ```bash
   cd ~/Desktop/HUVoice\ AI
   ```

---

## 📦 Step 2: Install Dependencies (2 minutes)

Run this single command:

```bash
pip install -r requirements.txt
```

✓ Done! All libraries are installed.

---

## 🧪 Step 3: Verify Setup (1 minute)

Run the test to make sure everything works:

```bash
python test_setup.py
```

You should see:
```
✓ Module Imports: PASS
✓ Environment Config: PASS
✓ Project Structure: PASS
✓ Network Connectivity: PASS
✓ Audio Capabilities: PASS

All tests passed! HUVOICE AGENT is ready to use.
```

---

## 🎤 Step 4: Start HUVOICE AGENT (1 minute)

### Option A: Windows (Easiest)
Double-click: **run.bat**

### Option B: Mac/Linux
```bash
bash run.sh
```

### Option C: Any System
```bash
python huvoice_agent.py
```

You'll see:
```
╔════════════════════════════════════════╗
║     HUVOICE AGENT - Starting...       ║
║  Advanced Voice-Based AI Assistant     ║
╚════════════════════════════════════════╝

[INFO] Starting Flask server...
[INFO] Web Interface: http://localhost:5000
[INFO] API Base: http://localhost:5000/api
```

✓ Agent is running!

---

## 🌐 Step 5: Open Web Interface

In your web browser, go to:
```
http://localhost:5000
```

You should see a beautiful interface with:
- 🎤 Voice Input button
- ⌨️ Text input field
- 💬 Conversation display
- 📊 Statistics

---

## ❓ Ask Your First Question

### Method 1: Text Input (Faster)
1. Type: "What is Python?"
2. Press Enter
3. Get instant answer from Google ✓

### Method 2: Voice Input
1. Click 🎤 **Voice Input** button
2. Speak: "What is artificial intelligence?"
3. Agent processes and speaks answer ✓

---

## 🎨 Features You Can Try

```
"What is machine learning?"
"Who won the World Cup 2022?"
"How does photosynthesis work?"
"What is the population of Earth?"
"Tell me about quantum computers"
"What are renewable energy sources?"
"How far is the Moon from Earth?"
"What is blockchain technology?"
```

---

## 🛑 Stop the Agent

Press: **Ctrl + C** in the terminal

---

## 🔧 Customize (Optional)

Edit `.env` file to change:
```env
# Change port if 5000 is busy
FLASK_PORT=5001

# Change agent name
AGENT_NAME=MY_VOICE_BOT

# Enable/disable features
VOICE_ENABLED=True
GOOGLE_SEARCH_ENABLED=True
```

Then restart the agent.

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port 5000 in use" | Change `FLASK_PORT` in `.env` |
| Microphone not detected | Use text input instead, or install PyAudio |
| No internet | Google search won't work; try later |
| Python not found | Install Python from python.org |
| Dependencies fail | Run: `pip install --upgrade pip` |

---

## 📚 Next Steps

1. **Read full documentation:** See `README.md`
2. **Explore API:** See `API_DOCUMENTATION.md`
3. **View configuration:** See `config.json`
4. **Integrate with code:** Import from `huvoice_agent.py`

---

## 🎉 You're All Set!

HUVOICE AGENT is now ready to:
- ✅ Listen to your voice
- ✅ Search Google for answers
- ✅ Speak responses back to you
- ✅ Remember conversation history
- ✅ Provide API endpoints

**Enjoy using HUVOICE AGENT!** 🎤🤖

---

**Need help?** Check `README.md` or `API_DOCUMENTATION.md`

**Version:** 1.0
**Last Updated:** May 25, 2026
