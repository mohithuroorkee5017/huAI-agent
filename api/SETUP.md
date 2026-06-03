# HU Voice AI API - Setup Guide

Complete step-by-step guide to set up and run the HU Voice AI API.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Server](#running-the-server)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB for dependencies
- **Internet Connection**: Required for OpenRouter API and web search

### Recommended

- Python 3.11 or higher
- 4GB+ RAM
- 2GB+ disk space
- Stable internet connection

### Check Python Installation

```bash
# Windows
python --version

# macOS/Linux
python3 --version
```

Should show Python 3.8 or higher.

---

## Installation Steps

### Step 1: Download/Clone the Project

```bash
# Navigate to your desired location
cd Desktop

# If cloning from git
git clone <repository_url>
cd api

# Or if downloading as ZIP
# Extract the ZIP file and navigate to the api folder
```

### Step 2: Create Virtual Environment

Virtual environments isolate project dependencies and prevent conflicts.

#### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the beginning of your terminal line
```

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) at the beginning of your terminal line
```

### Step 3: Install Dependencies

With the virtual environment activated:

```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- FastAPI: Web framework
- Uvicorn: ASGI server
- Requests: HTTP client
- Wikipedia: Wikipedia API
- DuckDuckGo Search: Web search
- langdetect: Language detection
- Pydantic: Data validation
- And more...

### Step 4: Get OpenRouter API Key

1. Visit https://openrouter.ai/keys
2. Sign up/Log in to your account
3. Create a new API key
4. Copy your API key (you'll need it in the next step)

---

## Configuration

### Step 1: Create .env File

```bash
# Copy the example file
copy .env.example .env          # Windows
cp .env.example .env            # macOS/Linux
```

### Step 2: Edit .env File

Open `.env` in a text editor and update these values:

```env
# Most Important: Add your OpenRouter API key
OPENROUTER_API_KEY=sk_live_your_actual_key_here

# Keep other settings as default or adjust as needed
OPENROUTER_MODEL=openai/gpt-4o-mini
PORT=5000
LOG_LEVEL=INFO
MAX_CONVERSATION_HISTORY=20
RATE_LIMIT_REQUESTS=100
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `OPENROUTER_API_KEY` | - | **Required** - Your API key from OpenRouter |
| `OPENROUTER_MODEL` | openai/gpt-4o-mini | AI model to use |
| `PORT` | 5000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `DEBUG` | False | Debug mode (False for production) |
| `MAX_CONVERSATION_HISTORY` | 20 | Messages to keep in memory |
| `RATE_LIMIT_REQUESTS` | 100 | Max requests per window |
| `RATE_LIMIT_WINDOW` | 60 | Rate limit window in seconds |
| `LOG_LEVEL` | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |

---

## Running the Server

### Option 1: Using Startup Scripts (Recommended)

#### Windows

```bash
# Double-click start.bat in the project folder
# Or run from command prompt:
start.bat
```

#### macOS/Linux

```bash
# Make script executable
chmod +x start.sh

# Run the script
./start.sh
# Or
bash start.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment (if not already active)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the server
python main.py
```

### Option 3: Using Uvicorn Directly

```bash
# With virtual environment activated
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Successful Startup

You should see output like:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to stop)
```

### Access the API

- **Main API**: http://localhost:5000
- **Interactive Docs**: http://localhost:5000/docs
- **Alternative Docs**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

---

## Testing

### Option 1: Using Interactive Docs

1. Open http://localhost:5000/docs in your browser
2. Click on "POST /chat" endpoint
3. Click "Try it out"
4. Enter a test message
5. Click "Execute"

### Option 2: Using Test Script

```bash
# Make sure server is running in another terminal

# Run the comprehensive test suite
python test_api.py
```

This will:
- Check API health
- Test English conversation
- Test Hindi conversation
- Test Hinglish conversation
- Test multiple conversations
- Test university knowledge base
- And more...

### Option 3: Using cURL

```bash
# Test health check
curl http://localhost:5000/health

# Send a message
curl -X POST "http://localhost:5000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello", "conversation_id":"test123"}'

# Get conversation history
curl http://localhost:5000/conversations/test123
```

### Option 4: Using Python

```python
import requests

response = requests.post(
    "http://localhost:5000/chat",
    json={
        "message": "Tell me about admissions",
        "conversation_id": "student_1"
    }
)

print(response.json())
```

---

## Troubleshooting

### Issue 1: Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
- Windows: Install Python from python.org, make sure to check "Add Python to PATH" during installation
- macOS/Linux: Install Python 3 via Homebrew or package manager

**Test**:
```bash
python --version
# or
python3 --version
```

### Issue 2: Virtual Environment Not Activating

**Error**: `venv\Scripts\activate is not recognized`

**Solution**: Make sure you're in the correct directory:

```bash
# Check current directory
cd path/to/api

# Then try again
venv\Scripts\activate
```

### Issue 3: Dependencies Installation Fails

**Error**: `ERROR: Could not install packages due to an EnvironmentError`

**Solution**:

```bash
# Make sure virtual environment is activated
# Then try:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Issue 4: OpenRouter API Key Not Working

**Error**: `OpenRouter API error: 401`

**Solution**:
1. Verify API key is correct in `.env` file
2. Check if key starts with `sk_live_` or similar
3. Visit https://openrouter.ai/keys to verify key is valid
4. Make sure .env file is in the project root

**Test API Key**:
```bash
# Add to a temporary Python script
import os
from config import settings
print(f"API Key configured: {bool(settings.OPENROUTER_API_KEY)}")
```

### Issue 5: Port 5000 Already in Use

**Error**: `Address already in use`

**Solution 1**: Change port in `.env`
```env
PORT=8000
```

**Solution 2**: Find and stop the process using port 5000

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

macOS/Linux:
```bash
lsof -i :5000
kill -9 <PID>
```

### Issue 6: Internet Connection Issues

**Error**: `Connection error with Wikipedia/DuckDuckGo`

**Solution**:
- Check internet connection
- Increase timeouts in `.env`:
  ```env
  WIKIPEDIA_TIMEOUT=10
  DUCKDUCKGO_TIMEOUT=10
  ```

### Issue 7: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
1. Verify virtual environment is activated (you should see `(venv)` in terminal)
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue 8: Permission Denied (macOS/Linux)

**Error**: `Permission denied: './start.sh'`

**Solution**:
```bash
chmod +x start.sh
./start.sh
```

### Check Logs

For detailed error information:

```bash
# View logs
tail -f app.log              # macOS/Linux
type app.log                 # Windows

# Search for errors
grep ERROR app.log           # macOS/Linux
findstr ERROR app.log        # Windows
```

---

## Quick Reference

### Common Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run tests
python test_api.py

# View logs
tail -f app.log

# Check if port is in use
# Windows:
netstat -ano | findstr :5000
# macOS/Linux:
lsof -i :5000
```

### API Quick Test

```bash
# Health check
curl http://localhost:5000/health

# Send message
curl -X POST "http://localhost:5000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'

# Get status
curl http://localhost:5000/status
```

---

## Next Steps

1. ✅ Server is running
2. Test basic functionality in `/docs`
3. Read the README.md for detailed API documentation
4. Review `services/` modules to understand the architecture
5. Customize university knowledge base in `main.py`
6. Deploy to production when ready

---

## Support

For issues:
1. Check this troubleshooting guide
2. Review logs in `app.log`
3. Visit http://localhost:5000/docs to test endpoints
4. Check configuration in `.env`

---

**Happy coding! 🚀**
