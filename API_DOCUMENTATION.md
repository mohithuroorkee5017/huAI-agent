# 🎤 Haridwar University AI - API Documentation

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### 1. Ask Question
**Endpoint:** `POST /api/ask`

Ask a question and get an answer from Google search.

**Request:**
```json
{
  "question": "What is artificial intelligence?"
}
```

**Response (Success):**
```json
{
  "success": true,
  "question": "What is artificial intelligence?",
  "answer": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
  "timestamp": "2026-05-25T10:30:45.123456"
}
```

**Response (Error):**
```json
{
  "error": "No question provided"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing question)
- `500` - Server error

---

### 2. Voice Input
**Endpoint:** `POST /api/voice-input`

Record voice input and get answer.

**Request:**
```
No request body required
```

**Response (Success):**
```json
{
  "success": true,
  "heard": "What is Python?",
  "answer": "Python is a high-level, interpreted programming language..."
}
```

**Response (Failure):**
```json
{
  "success": false,
  "text": null
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error (microphone/API issue)

---

### 3. Get Conversation History
**Endpoint:** `GET /api/history`

Retrieve all conversation messages.

**Request:**
```
No request body required
```

**Response:**
```json
{
  "history": [
    {
      "timestamp": "2026-05-25T10:30:45.123456",
      "question": "What is Python?",
      "type": "user"
    },
    {
      "timestamp": "2026-05-25T10:30:50.123456",
      "answer": "Python is a high-level programming language...",
      "type": "agent"
    }
  ]
}
```

---

### 4. Get Agent Status
**Endpoint:** `GET /api/status`

Check agent status and statistics.

**Request:**
```
No request body required
```

**Response:**
```json
{
  "status": "active",
  "agent_name": "HARIDWAR UNIVERSITY AI",
  "listening": false,
  "conversation_count": 5
}
```

**Status Values:**
- `active` - Agent is running
- `listening` - Currently recording voice
- `not_initialized` - Agent not initialized

---

### 5. Clear Conversation History
**Endpoint:** `POST /api/clear-history`

Delete all conversation history.

**Request:**
```
No request body required
```

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

## cURL Examples

### Ask a Question
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'
```

### Get Agent Status
```bash
curl http://localhost:5000/api/status
```

### Get Conversation History
```bash
curl http://localhost:5000/api/history
```

### Clear History
```bash
curl -X POST http://localhost:5000/api/clear-history
```

---

## Python Examples

### Using Requests Library
```python
import requests

BASE_URL = 'http://localhost:5000'

# Ask a question
response = requests.post(
    f'{BASE_URL}/api/ask',
    json={'question': 'What is Python?'}
)
data = response.json()
print(data['answer'])

# Get status
status = requests.get(f'{BASE_URL}/api/status').json()
print(f"Agent: {status['agent_name']} - {status['status']}")

# Get history
history = requests.get(f'{BASE_URL}/api/history').json()
print(f"Conversations: {len(history['history'])}")
```

### Using the Agent Directly
```python
from huvoice_agent import HUVoiceAgent

# Initialize agent
agent = HUVoiceAgent('sk-or-v1-YOUR_KEY_HERE')

# Ask a question
answer = agent.process_question("What is AI?")
print(answer)

# Get history
history = agent.get_conversation_history()
for entry in history:
    print(entry)

# Clear history
agent.clear_history()
```

---

## JavaScript Examples

### Using Fetch API
```javascript
// Ask a question
const response = await fetch('http://localhost:5000/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: 'What is JavaScript?' })
});

const data = await response.json();
console.log(data.answer);

// Get status
const status = await fetch('http://localhost:5000/api/status').then(r => r.json());
console.log(`Agent: ${status.agent_name} - ${status.status}`);

// Voice input
const voice = await fetch('http://localhost:5000/api/voice-input', {
    method: 'POST'
}).then(r => r.json());
console.log(`Heard: ${voice.heard}`);
console.log(`Answer: ${voice.answer}`);
```

---

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "No question provided"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Agent not initialized"
}
```

**Network Timeout:**
```
Request timeout after 30 seconds
```

---

## Rate Limiting

Currently no rate limiting is implemented. However:
- Google searches may be throttled if excessive requests
- Microphone access is limited to one session at a time
- Conversation history is in-memory only

---

## Performance Notes

- Average response time: 2-5 seconds
- Voice input processing: 5-10 seconds
- Google search: 1-3 seconds
- Text-to-speech: 2-5 seconds

---

## Troubleshooting

### 500 Error - Agent not initialized
- Ensure the Flask app is running
- Check that API key is configured in .env

### Connection refused
- Check if server is running on port 5000
- Try changing port in .env

### No answers returned
- Verify internet connection
- Check Google search restrictions in your region
- Try simpler question wording

### Voice input failing
- Ensure microphone is connected
- Check microphone permissions
- Try using text input instead

---

## Version
API Version: 1.0
Last Updated: May 25, 2026
