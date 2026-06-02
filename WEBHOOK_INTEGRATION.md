# 🔗 HUVOICE AGENT - N8N Webhook Integration Guide

## Overview
HUVOICE AGENT is now fully integrated with n8n workflow automation platform via webhooks, allowing bidirectional communication between the voice agent and n8n workflows.

---

## 🔗 Webhook Configuration

### N8N Webhook URL
```
https://huassist2010.app.n8n.cloud/webhook/38f72ae7-8140-4887-b3b5-ce7e118f7c13
```

### Status
✅ **ACTIVE & CONFIGURED**
- Webhook is properly registered in agent
- Fallback to Google Search enabled
- Real-time response handling

---

## 📨 Webhook Endpoints

### 1. Internal Webhook Endpoint
**Endpoint:** `POST /api/webhook`
**Purpose:** Process questions and send to external webhook

**Request:**
```json
{
  "question": "What is AI?"
}
```

**Response:**
```json
{
  "success": true,
  "question": "What is AI?",
  "answer": "Answer from webhook or Google...",
  "agent": "HUVOICE AGENT",
  "timestamp": "2026-05-25T16:32:08.943090"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/webhook \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

---

### 2. External Webhook Handler
**Endpoint:** `POST /webhook/<webhook_id>`
**Purpose:** Receive webhook calls from external sources (n8n)

**Parameters:**
- `webhook_id`: Unique webhook identifier
- `question` or `q` or `message`: The question to process

**Request Examples:**

```bash
# POST with JSON
POST /webhook/external-id
Content-Type: application/json

{
  "question": "What is machine learning?",
  "user": "john_doe"
}
```

```bash
# GET with query parameters
GET /webhook/external-id?question=What%20is%20AI&user=john
```

**Response:**
```json
{
  "success": true,
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of AI...",
  "agent": "HUVOICE AGENT",
  "webhook_id": "external-id",
  "timestamp": "2026-05-25T16:32:08.943090"
}
```

---

## 🔄 Data Flow

### Flow 1: Question via Web Interface
```
User Question 
    ↓
Web Interface (/api/ask)
    ↓
HUVOICE AGENT
    ├→ Try N8N Webhook (if configured)
    └→ Fall back to Google Search
    ↓
Return Answer
    ↓
Display in Chat
```

### Flow 2: N8N to HUVOICE AGENT
```
N8N Workflow
    ↓
POST to /api/webhook
    ↓
HUVOICE AGENT processes
    ↓
Returns JSON response
    ↓
N8N receives result
    ↓
Continue workflow...
```

### Flow 3: External Webhook
```
External App
    ↓
POST to /webhook/<id>
    ↓
HUVOICE AGENT processes
    ↓
Returns JSON response
    ↓
External app gets result
```

---

## 🔧 Configuration

### Environment Variables (.env)
```env
# N8N Webhook URL
WEBHOOK_URL=https://huassist2010.app.n8n.cloud/webhook/38f72ae7-8140-4887-b3b5-ce7e118f7c13

# Enable/disable webhook
WEBHOOK_ENABLED=True

# Fallback to Google if webhook fails
GOOGLE_SEARCH_ENABLED=True
```

---

## 📊 Use Cases

### 1. N8N to Voice Agent
- Send question from n8n workflow
- Get answer from HUVOICE AGENT
- Continue workflow with answer

**N8N HTTP Request Node:**
```
Method: POST
URL: http://localhost:5000/api/webhook
Body:
{
  "question": "{{ $json.userQuestion }}"
}
```

### 2. Voice Agent to N8N
- HUVOICE AGENT sends question to n8n
- N8N processes and returns answer
- Agent speaks the response

**Automatic Flow:**
```
User Question (text/voice)
    ↓
HUVOICE tries n8n webhook first
    ↓
If n8n responds: use that answer
    ↓
If n8n fails/timeout: fallback to Google
    ↓
Return answer to user
```

### 3. External Integration
- Any app can POST to `/webhook/<id>`
- Get AI-processed answers
- No authentication required (open)

---

## 🧪 Testing

### Test 1: Internal Webhook
```powershell
$body = @{question="What is N8N?"} | ConvertTo-Json
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/webhook" `
  -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json
```

### Test 2: External Webhook
```powershell
$body = @{question="Tell me about webhooks", user="testuser"} | ConvertTo-Json
$response = Invoke-WebRequest -Uri "http://localhost:5000/webhook/test-123" `
  -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json
```

### Test 3: Query Parameter
```
http://localhost:5000/webhook/test-123?question=What%20is%20AI&user=john
```

---

## 🛡️ Security Notes

- **Current Status:** Open endpoints (development mode)
- **Recommended for Production:**
  - Add API key validation
  - Implement rate limiting
  - Use HTTPS
  - Add request signing
  - Validate webhook sources

---

## 🔗 N8N Workflow Integration

### Example: Simple Question Workflow

```
Trigger: HTTP Request
  ↓
Extract Question
  ↓
POST to HUVOICE /api/webhook
  ↓
Parse Response
  ↓
Send Email with Answer
```

### Example: Chat with Voice Agent

```
Slack Message (via n8n Slack integration)
  ↓
Extract message text
  ↓
POST to HUVOICE /api/webhook
  ↓
Get answer
  ↓
Reply in Slack
```

---

## 📱 API Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Answer returned |
| 400 | Bad Request | Missing question |
| 500 | Server Error | Agent not initialized |

---

## 🔄 Retry & Fallback Logic

### Current Implementation
1. Try to send question to n8n webhook
2. Wait for response (10 second timeout)
3. If successful: return n8n answer
4. If failed/timeout: automatically use Google Search
5. Return best available answer

---

## 📝 Webhook Payload Examples

### Minimal Request
```json
{
  "question": "What is AI?"
}
```

### Full Request
```json
{
  "question": "What is machine learning?",
  "user": "john_doe",
  "session_id": "abc123",
  "context": "learning about AI"
}
```

### Response Structure
```json
{
  "success": true,
  "question": "Original question",
  "answer": "The answer",
  "agent": "HUVOICE AGENT",
  "webhook_id": "if external",
  "timestamp": "ISO 8601 timestamp",
  "source": "n8n" or "google" or "direct"
}
```

---

## 🐛 Troubleshooting

### Issue: Webhook not responding
**Solution:** 
- Check n8n webhook URL is correct
- Verify n8n workflow is active
- Check network connectivity
- Agent will automatically fallback to Google Search

### Issue: Timeout errors
**Solution:**
- Increase timeout in code (currently 10s)
- Check n8n workflow performance
- Ensure fast response in n8n

### Issue: No answer returned
**Solution:**
- Check question is valid
- Verify Google search is enabled (fallback)
- Check logs for error messages

---

## 📊 Monitoring

### Check Agent Status
```
GET http://localhost:5000/api/status
```

### View Conversation History
```
GET http://localhost:5000/api/history
```

### Recent Logs
Check terminal output for webhook-related logs:
```
[WEBHOOK] Sending data to: ...
[WEBHOOK] Response: 200
[WEBHOOK] Answer received: ...
```

---

## 🚀 Production Deployment

### Recommended Setup
1. Use production Flask server (Gunicorn)
2. Add HTTPS with SSL certificate
3. Implement API key authentication
4. Add request validation
5. Set up monitoring/logging
6. Configure rate limiting
7. Use reverse proxy (nginx)

### Example Gunicorn Command
```bash
gunicorn -w 4 -b 0.0.0.0:5000 huvoice_agent:app
```

---

## 📚 N8N Resources
- Official: https://n8n.io/
- Webhook Docs: https://docs.n8n.io/nodes/n8n-nodes-base.webhook/
- HTTP Trigger: https://docs.n8n.io/nodes/n8n-nodes-base.httpRequest/

---

## ✅ Verification Checklist

- [x] N8N webhook URL configured
- [x] Internal webhook endpoint working
- [x] External webhook endpoint created
- [x] Fallback to Google Search enabled
- [x] JSON responses properly formatted
- [x] Error handling implemented
- [x] Logging configured
- [x] Testing completed

---

**Status:** ✅ **FULLY FUNCTIONAL**

HUVOICE AGENT is ready to integrate with n8n workflows!

Last Updated: May 25, 2026
