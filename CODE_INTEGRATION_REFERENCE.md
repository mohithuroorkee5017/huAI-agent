# 🔍 Haridwar University AI - Code Integration Reference

**Complete Map of FastAPI ↔ Flask Integration**

---

## 📍 FILE LOCATIONS

### Flask Agent
```
📁 d:\Users\pop\Desktop\HUVoice AI\
├── huvoice_agent.py (Main Flask application + HaridwarUniversityAI class)
├── .env (Configuration)
└── requirements.txt (Flask dependencies)
```

### FastAPI Backend
```
📁 d:\Users\pop\Desktop\Haridwar University AI\api\
├── main.py (FastAPI application)
├── config.py (FastAPI configuration)
├── requirements.txt (FastAPI dependencies)
└── services/
    ├── memory.py (Conversation memory)
    ├── openrouter.py (OpenRouter integration)
    ├── search.py (Web search)
    └── wiki.py (Wikipedia search)
```

---

## 🔗 INTEGRATION POINTS

### 1. CONFIGURATION (.env)
**File**: `d:\Users\pop\Desktop\Haridwar University AI\.env`

```
HARIDWAR_BACKEND_URL=http://127.0.0.1:8000
OPENROUTER_REQUEST_TIMEOUT=30
OPENROUTER_RETRY_ATTEMPTS=3
FLASK_PORT=5000
```

**Purpose**: 
- Tells Flask agent where FastAPI backend is located
- Sets timeout and retry parameters
- Configures Flask port

---

### 2. FLASK AGENT - INITIALIZATION

**File**: `huvoice_agent.py`  
**Lines**: 30-48

```python
class HaridwarUniversityAI:
    def __init__(self, api_key, webhook_url=None):
        # FastAPI Backend Configuration
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.backend_url = os.getenv('HARIDWAR_BACKEND_URL', 'http://127.0.0.1:8000')
        self.backend_chat_endpoint = f"{self.backend_url}/chat"
        self.request_timeout = int(os.getenv('OPENROUTER_REQUEST_TIMEOUT', '30'))
        self.retry_attempts = int(os.getenv('OPENROUTER_RETRY_ATTEMPTS', '3'))
```

**What It Does**:
- Reads FastAPI URL from `.env`
- Constructs chat endpoint URL: `http://127.0.0.1:8000/chat`
- Sets timeout (30s) and retry attempts (3)

**Key Variables**:
- `self.backend_url`: Where FastAPI is running
- `self.backend_chat_endpoint`: Full chat endpoint URL
- `self.request_timeout`: Timeout in seconds
- `self.retry_attempts`: Number of retry attempts

---

### 3. FLASK AGENT - REUSABLE FUNCTION

**File**: `huvoice_agent.py`  
**Lines**: 355-460  
**Function**: `call_hu_api(message, conversation_id)`

```python
def call_hu_api(self, message, conversation_id):
    """Call HU Voice AI FastAPI backend with proper error handling"""
    
    # RETRY LOOP
    for attempt in range(self.retry_attempts):  # 3 attempts
        try:
            logger.info(f"[BACKEND] Attempt {attempt + 1}/{self.retry_attempts}")
            logger.info(f"[BACKEND] Calling {self.backend_chat_endpoint}")
            
            # PREPARE REQUEST
            payload = {
                "message": message,
                "conversation_id": conversation_id
            }
            
            # SEND REQUEST
            response = requests.post(
                self.backend_chat_endpoint,  # http://127.0.0.1:8000/chat
                json=payload,
                timeout=self.request_timeout,  # 30 seconds
                headers={'Content-Type': 'application/json'}
            )
            
            logger.info(f"[BACKEND] Response status: {response.status_code}")
            
            # PARSE RESPONSE
            if response.status_code == 200:
                data = response.json()
                
                # EXTRACT ANSWER
                if data.get('success') and 'answer' in data:
                    answer = data.get('answer', '').strip()
                    if answer:
                        logger.info(f"[BACKEND] ✓ SUCCESS")
                        return answer  # ← RETURN EXTRACTED ANSWER
            
            # ERROR HANDLING
            elif response.status_code == 422:
                logger.error(f"[BACKEND] Validation error (422)")
                return None
            elif response.status_code == 500:
                logger.error(f"[BACKEND] Server error (500)")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2)
                    continue
        
        except requests.exceptions.Timeout:
            logger.error(f"[BACKEND] Request timeout ({self.request_timeout}s)")
            if attempt < self.retry_attempts - 1:
                time.sleep(1)
                continue
        
        except requests.exceptions.ConnectionError:
            logger.error(f"[BACKEND] Connection error")
            logger.error(f"[BACKEND] Backend must be running at {self.backend_chat_endpoint}")
            if attempt < self.retry_attempts - 1:
                time.sleep(1)
                continue
        
        except Exception as e:
            logger.error(f"[BACKEND] Unexpected error: {str(e)}")
    
    logger.error(f"[BACKEND] All {self.retry_attempts} attempts failed")
    return None
```

**What It Does**:
1. Attempts to call FastAPI backend (up to 3 times)
2. Sends message + conversation_id as JSON
3. Handles timeouts, connection errors, and HTTP errors
4. Extracts answer from response
5. Returns answer or None

**Called By**: `get_ai_response()`

---

### 4. FLASK AGENT - AI RESPONSE HANDLER

**File**: `huvoice_agent.py`  
**Lines**: 462-481  
**Function**: `get_ai_response(question, user_id, lang)`

```python
def get_ai_response(self, question, user_id, lang):
    """Get response from FastAPI backend via call_hu_api function"""
    try:
        logger.info(f"[AI] Processing question: {question[:80]}...")
        logger.info(f"[AI] User ID: {user_id}")
        logger.info(f"[AI] Detected Language: {lang}")
        
        # CALL REUSABLE FUNCTION
        answer = self.call_hu_api(question, user_id)  # ← CALLS call_hu_api()
        
        if answer:
            logger.info(f"[AI] ✓ Got response from backend")
            return answer
        else:
            logger.error(f"[AI] Backend returned None")
            return None
```

**What It Does**:
- Simple wrapper around `call_hu_api()`
- Delegates all backend communication to `call_hu_api()`
- Returns answer or None

**Called By**: `process_user_input()`

---

### 5. FLASK AGENT - REQUEST PROCESSING

**File**: `huvoice_agent.py`  
**Lines**: 545-586  
**Function**: `process_user_input(user_input, user_id='default')`

```python
def process_user_input(self, user_input, user_id='default'):
    """Process user input and generate response via FastAPI backend"""
    try:
        logger.info(f"[PROCESS] Input: {user_input}")
        logger.info(f"[PROCESS] User ID: {user_id}")
        
        # 1. DETECT LANGUAGE
        lang = self.detect_language(user_input)
        logger.info(f"[LANG] Detected: {lang}")
        
        # 2. STORE USER MESSAGE IN HISTORY
        self.add_to_history(user_id, 'user', user_input)
        
        # 3. MAIN PATH: CALL FASTAPI BACKEND
        logger.info(f"[PROCESS] Calling FastAPI backend...")
        ai_response = self.get_ai_response(user_input, user_id, lang)  # ← Gets answer
        
        if ai_response:
            logger.info(f"[PROCESS] ✓ Backend returned response")
            self.add_to_history(user_id, 'assistant', ai_response)
            return ai_response
        
        # 4. FALLBACK 1: TRY SEARCH
        logger.warning(f"[PROCESS] Backend failed, trying search...")
        search_result = self.search_local_knowledge(user_input, lang)
        if search_result:
            logger.info(f"[PROCESS] ✓ Search found result")
            self.add_to_history(user_id, 'assistant', search_result)
            return search_result
        
        # 5. FALLBACK 2: ERROR MESSAGE
        logger.error(f"[PROCESS] Both backend and search failed")
        error_msg = self.get_meaningful_error(lang)
        self.add_to_history(user_id, 'assistant', error_msg)
        return error_msg
```

**Request Priority**:
1. ✅ FastAPI Backend (PRIMARY)
2. ⚠️ Local Search (FALLBACK 1)
3. ❌ Error Message (FALLBACK 2)

**Called By**: Flask routes (`/api/ask`, `/webhook/<id>`)

---

### 6. FLASK WEB ROUTES

#### Route 1: Webhook (Public, No Auth Required)

**File**: `huvoice_agent.py`  
**Lines**: ~920-940

```python
@app.route('/webhook/<path:webhook_id>', methods=['POST', 'GET'])
def webhook_handler(webhook_id):
    """Webhook handler"""
    data = request.json or {}
    question = data.get('question') or data.get('q') or data.get('message')
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    answer = agent.process_user_input(question, webhook_id)  # ← Calls process_user_input
    
    return jsonify({
        'success': True,
        'question': question,
        'answer': answer,
        'agent': agent.agent_name,
        'webhook_id': webhook_id,
        'timestamp': datetime.now().isoformat()
    })
```

**Usage**:
```
POST http://localhost:5000/webhook/test_user
{
  "message": "Hello bhai kaise ho"
}
```

#### Route 2: Authenticated API Endpoint

**File**: `huvoice_agent.py`  
**Lines**: ~860-882

```python
@app.route('/api/ask', methods=['POST'])
@login_required  # ← Requires authentication
def ask_question():
    """Ask question API"""
    data = request.json
    question = data.get('question', '')
    user_email = session['user']['email']
    
    answer = agent.process_user_input(question, user_email)  # ← Calls process_user_input
    
    return jsonify({
        'success': True,
        'question': question,
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })
```

**Usage**:
```
POST http://localhost:5000/api/ask
Headers: Cookie: session=<auth_token>
{
  "question": "Hello bhai kaise ho"
}
```

---

### 7. FASTAPI BACKEND - CHAT ENDPOINT

**File**: `api/main.py`  
**Lines**: 350-450  
**Endpoint**: `POST /chat`

```python
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """Main chat endpoint"""
    
    # REQUEST MODEL
    # Receives: {"message": "...", "conversation_id": "..."}
    
    # EXTRACT PARAMETERS
    conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:12]}"
    user_message = request.message.strip()
    
    logger.info(f"Processing message for conversation: {conversation_id}")
    
    # LANGUAGE DETECTION
    user_language = language_detector.detect_language(user_message)
    
    # GET CONVERSATION HISTORY
    history = memory.get_history(conversation_id)
    
    # GATHER SOURCES (University KB, Wikipedia, Web Search)
    sources = []
    uni_knowledge = get_university_knowledge(user_message)
    if uni_knowledge:
        sources.append(uni_knowledge)
    
    # CALL OPENROUTER API (via service)
    ai_answer, success = openrouter_service.get_ai_response(
        user_message=user_message,
        conversation_history=history,
        user_language=user_language,
        sources=sources
    )
    
    if not success or not ai_answer:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable."
        )
    
    # STORE IN MEMORY
    memory.add_message(
        conversation_id=conversation_id,
        role="user",
        content=user_message,
        language=user_language
    )
    memory.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_answer,
        language=user_language
    )
    
    # RESPONSE MODEL
    return {
        "success": True,
        "answer": ai_answer,  # ← Extracted answer
        "sources": [...],
        "language": user_language,
        "conversation_id": conversation_id,
        "timestamp": datetime.now().isoformat()
    }
```

**Request Contract**:
```json
POST http://127.0.0.1:8000/chat
{
  "message": "Hello bhai kaise ho",
  "conversation_id": "test_user"
}
```

**Response Contract**:
```json
{
  "success": true,
  "answer": "Kya haal hai bhai! Sab badhiya?",
  "sources": [],
  "language": "en",
  "conversation_id": "test_user",
  "timestamp": "2026-06-01T16:24:02.497911"
}
```

---

## 🔄 COMPLETE REQUEST/RESPONSE FLOW

### Step-by-Step with Line Numbers

```
1. USER SENDS REQUEST
   POST http://localhost:5000/webhook/test_user
   Body: {"message": "Hello bhai kaise ho"}
   
2. FLASK ROUTE (huvoice_agent.py ~920)
   webhook_handler(webhook_id)
   ↓
   agent.process_user_input(question, webhook_id)

3. PROCESS USER INPUT (huvoice_agent.py ~545)
   process_user_input(user_input, user_id)
   ├─ detect_language(user_input)          [Line ~548]
   ├─ add_to_history(user_id, 'user', ...) [Line ~549]
   └─ get_ai_response(...)                  [Line ~550]
   
4. GET AI RESPONSE (huvoice_agent.py ~462)
   get_ai_response(question, user_id, lang)
   └─ call_hu_api(question, user_id)       [Line ~465]
   
5. CALL REUSABLE FUNCTION (huvoice_agent.py ~355)
   call_hu_api(message, conversation_id)
   ├─ Prepare payload:
   │  {
   │    "message": "Hello bhai kaise ho",
   │    "conversation_id": "test_user"
   │  }
   ├─ POST requests.post(                   [Line ~375]
   │    "http://127.0.0.1:8000/chat",
   │    json=payload,
   │    timeout=30
   │  )
   ├─ response.status_code == 200          [Line ~385]
   ├─ data = response.json()                [Line ~388]
   ├─ answer = data.get('answer')           [Line ~392]
   └─ return answer                         [Line ~395]

6. FASTAPI BACKEND RECEIVES REQUEST
   POST http://127.0.0.1:8000/chat
   api/main.py ~350
   ├─ conversation_id = "test_user"
   ├─ user_message = "Hello bhai kaise ho"
   ├─ user_language = detect_language()
   ├─ history = memory.get_history(conversation_id)
   ├─ ai_answer = openrouter_service.get_ai_response(...)
   │  └─ Calls OpenRouter API
   └─ Returns JSON with answer

7. FLASK AGENT RECEIVES RESPONSE
   {
     "success": true,
     "answer": "Kya haal hai bhai! Sab badhiya?",
     "sources": [],
     ...
   }
   
8. EXTRACT ANSWER (huvoice_agent.py ~392)
   answer = data.get('answer')
   → "Kya haal hai bhai! Sab badhiya?"

9. STORE IN HISTORY (huvoice_agent.py ~551)
   add_to_history(user_id, 'assistant', answer)

10. RETURN TO FLASK (huvoice_agent.py ~552)
    return answer

11. FLASK RETURNS TO USER (huvoice_agent.py ~935)
    jsonify({
      'success': True,
      'question': 'Hello bhai kaise ho',
      'answer': 'Kya haal hai bhai! Sab badhiya?',
      'agent': 'HU Voice Agent',
      'webhook_id': 'test_user',
      'timestamp': '2026-06-01T16:24:32.374788'
    })

12. USER SEES RESPONSE ✅
    "Kya haal hai bhai! Sab badhiya?"
```

---

## 🎯 KEY FUNCTIONS SUMMARY

| Function | File | Lines | Purpose |
|----------|------|-------|---------|
| `call_hu_api()` | huvoice_agent.py | 355-460 | ⭐ **REUSABLE** - Single point for all backend calls |
| `get_ai_response()` | huvoice_agent.py | 462-481 | Wrapper around call_hu_api() |
| `process_user_input()` | huvoice_agent.py | 545-586 | Main request processor with fallbacks |
| `webhook_handler()` | huvoice_agent.py | ~920 | Public webhook endpoint |
| `ask_question()` | huvoice_agent.py | ~860 | Authenticated API endpoint |
| `/chat` endpoint | api/main.py | 350-450 | FastAPI chat endpoint |

---

## 📊 DATA FLOW SUMMARY

### Request Path
```
User Input
    ↓
Flask Route (webhook or /api/ask)
    ↓
process_user_input(message, user_id)
    ├─ Detect language
    ├─ Store in history
    └─ get_ai_response(message, user_id, lang)
        └─ call_hu_api(message, user_id) ◄── REUSABLE FUNCTION
            └─ POST http://127.0.0.1:8000/chat
                └─ FastAPI /chat endpoint
                    ├─ Get conversation history
                    ├─ Call OpenRouter API
                    └─ Return {"success": true, "answer": "..."}
                        └─ Extract answer
                            └─ Return to user
```

### Response Path
```
FastAPI Response
    {"success": true, "answer": "..."}
        ↓
call_hu_api() extracts answer
    ↓
get_ai_response() returns answer
    ↓
process_user_input() stores in history
    ↓
Flask route returns to user
    ↓
User sees answer
```

---

## ✅ INTEGRATION CHECKLIST

✅ **Configuration**: .env properly set  
✅ **Backend URL**: Stored in self.backend_url  
✅ **Chat Endpoint**: Constructed as http://127.0.0.1:8000/chat  
✅ **Request Payload**: {"message": "...", "conversation_id": "..."}  
✅ **Response Parsing**: data.get('answer')  
✅ **Retry Logic**: 3 attempts with backoff  
✅ **Timeout Handling**: 30 seconds per request  
✅ **Error Handling**: Connection errors, timeouts, HTTP errors  
✅ **Logging**: [BACKEND], [PROCESS], [LANG], [AI] prefixes  
✅ **Conversation History**: Preserved per user_id  
✅ **Fallback Support**: Search if backend fails  
✅ **Flask Routes**: Both webhook and /api/ask work  

---

## 🚀 DEPLOYMENT

### Start FastAPI Backend
```bash
cd d:\Users\pop\Desktop\Haridwar University AI\api
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Start Flask Agent
```bash
cd d:\Users\pop\Desktop\HUVoice AI
python huvoice_agent.py
```

### Test Integration
```bash
curl -X POST http://127.0.0.1:5000/webhook/test_user \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello bhai kaise ho"}'
```

**Response**:
```json
{
  "success": true,
  "answer": "Kya haal hai bhai! Sab badhiya?",
  "question": "Hello bhai kaise ho",
  "agent": "HU Voice Agent",
  "webhook_id": "test_user",
  "timestamp": "2026-06-01T16:24:32.374788"
}
```

---

**Integration Status**: ✅ COMPLETE  
**Reference Date**: June 1, 2026  
**All Code Locations**: ✅ VERIFIED
