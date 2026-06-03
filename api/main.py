"""
HU Voice AI API - Main Application
Production-ready FastAPI backend for intelligent conversational AI
"""

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging
from datetime import datetime
import uuid
import time
from functools import lru_cache
import sys
import os
import requests

# Add api directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from config import settings
from services import (
    memory,
    openrouter_service,
    language_detector,
    search_service,
    wiki_service
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# MODELS
# ============================================================================


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "क्या आप मुझे कुछ बताते हो?",
                "conversation_id": "conv_123"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    success: bool
    answer: str
    sources: List[Dict]
    language: str
    conversation_id: str
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "answer": "हाँ, बिल्कुल! मैं आपकी मदद कर सकता हूँ।",
                "sources": [
                    {
                        "type": "web",
                        "title": "Example",
                        "url": "https://example.com"
                    }
                ],
                "language": "hinglish",
                "conversation_id": "conv_123",
                "timestamp": "2024-01-01T10:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    uptime_seconds: int


class StatusResponse(BaseModel):
    """Status response"""
    status: str
    timestamp: str
    active_conversations: int
    total_requests: int
    api_configured: bool


# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready AI backend for conversational responses",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS
)

# ============================================================================
# STATISTICS
# ============================================================================

app_stats = {
    "start_time": time.time(),
    "total_requests": 0,
    "chat_requests": 0,
    "errors": 0
}

# ============================================================================
# RATE LIMITING
# ============================================================================

request_history = {}


def check_rate_limit(client_ip: str) -> bool:
    """
    Check if client has exceeded rate limit
    
    Args:
        client_ip: Client IP address
    
    Returns:
        True if within limit, False otherwise
    """
    if not settings.RATE_LIMIT_ENABLED:
        return True
    
    current_time = time.time()
    
    if client_ip not in request_history:
        request_history[client_ip] = []
    
    # Remove old requests outside the window
    request_history[client_ip] = [
        req_time for req_time in request_history[client_ip]
        if current_time - req_time < settings.RATE_LIMIT_WINDOW
    ]
    
    # Check limit
    if len(request_history[client_ip]) >= settings.RATE_LIMIT_REQUESTS:
        return False
    
    request_history[client_ip].append(current_time)
    return True


async def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    return request.client.host if request.client else "unknown"

# ============================================================================
# UNIVERSITY KNOWLEDGE BASE
# ============================================================================


UNIVERSITY_KB = {
    "admissions": {
        "eligibility": "Bachelor's programs require 10+2 or equivalent qualification",
        "application_deadline": "31st July",
        "entrance_exam": "JEE Main / Board scores",
        "counselling": "Online counselling portal available"
    },
    "courses": {
        "engineering": "4-year BTech programs in various branches",
        "management": "2-year MBA program with specializations",
        "science": "3-year BSc in Physics, Chemistry, Mathematics",
        "arts": "3-year BA in various disciplines"
    },
    "placements": {
        "average_package": "8-12 LPA",
        "top_package": "22+ LPA",
        "recruitment_season": "July-December",
        "companies": "TCS, Infosys, Goldman Sachs, Microsoft, Amazon"
    },
    "scholarships": {
        "merit_based": "50% to 100% tuition fee waiver",
        "need_based": "Additional financial support available",
        "sports_scholarship": "For sports achievers",
        "minority_scholarships": "As per government guidelines"
    },
    "hostel": {
        "capacity": "3500+ students",
        "mess_charges": "₹12000-15000 per semester",
        "facilities": "Wi-Fi, Gym, Sports, Study rooms",
        "accommodation": "On-campus housing available for all years"
    },
    "faculty": {
        "total": "400+ faculty members",
        "qualification": "PhD from reputed institutions",
        "research": "Active in research and publications",
        "contact": "Departmental offices and email"
    },
    "fees": {
        "engineering": "₹3 lakhs per annum",
        "management": "₹5 lakhs per annum",
        "science": "₹1.5 lakhs per annum",
        "arts": "₹80000 per annum"
    },
    "campus": {
        "area": "500+ acres",
        "library": "Central library with 500K+ books",
        "labs": "State-of-the-art research labs",
        "sports": "International-standard sports facilities"
    }
}


def get_university_knowledge(query: str) -> Optional[Dict]:
    """
    Search university knowledge base
    
    Args:
        query: Search query
    
    Returns:
        Knowledge dict or None
    """
    query_lower = query.lower()
    
    for category, items in UNIVERSITY_KB.items():
        if category in query_lower:
            return {
                "source": "University Knowledge",
                "category": category,
                "content": str(items)
            }
        
        for key, value in items.items():
            if key in query_lower or key.replace("_", " ") in query_lower:
                return {
                    "source": "University Knowledge",
                    "category": category,
                    "key": key,
                    "content": value
                }
    
    return None

# ============================================================================
# MIDDLEWARE & ERROR HANDLERS
# ============================================================================


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    app_stats["total_requests"] += 1
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Status: {response.status_code} | Duration: {process_time:.2f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    app_stats["errors"] += 1
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    app_stats["errors"] += 1
    logger.error(f"Unexpected error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# API ENDPOINTS
# ============================================================================


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status and uptime information
    """
    uptime = int(time.time() - app_stats["start_time"])
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "uptime_seconds": uptime
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get API status and statistics
    
    Returns:
        Current status and metrics
    """
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": len(memory.conversations),
        "total_requests": app_stats["total_requests"],
        "api_configured": bool(settings.OPENROUTER_API_KEY)
    }


# ============================================================================
# DIAGNOSTIC ENDPOINTS
# ============================================================================

@app.get("/diagnose")
async def diagnose():
    """
    Comprehensive diagnostic endpoint for troubleshooting
    
    Returns:
        Detailed configuration and integration status
    """
    import os
    
    # Check API key in environment
    env_api_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    # Check config loaded API key
    config_api_key = settings.OPENROUTER_API_KEY
    
    diagnosis = {
        "timestamp": datetime.now().isoformat(),
        "server": {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug_mode": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
            "uptime_seconds": int(time.time() - app_stats["start_time"])
        },
        "openrouter": {
            "api_key_loaded": bool(config_api_key),
            "api_key_in_env": bool(env_api_key),
            "api_key_matches": env_api_key == config_api_key if (env_api_key and config_api_key) else False,
            "primary_model": settings.OPENROUTER_MODEL,
            "fallback_models_count": len(settings.OPENROUTER_FALLBACK_MODELS),
            "api_key_preview": f"{config_api_key[:20]}...{config_api_key[-4:]}" if config_api_key else "NOT LOADED"
        },
        "services": {
            "memory": {
                "active_conversations": len(memory.conversations),
                "total_messages": sum(len(conv) for conv in memory.conversations.values())
            },
            "language_detector": "✓ Available",
            "search_service": "✓ Available",
            "wiki_service": "✓ Available"
        },
        "statistics": {
            "total_requests": app_stats["total_requests"],
            "chat_requests": app_stats["chat_requests"],
            "errors": app_stats["errors"],
            "rate_limit_enabled": settings.RATE_LIMIT_ENABLED
        },
        "warnings": []
    }
    
    # Add warnings
    if not config_api_key:
        diagnosis["warnings"].append("CRITICAL: OpenRouter API key not loaded")
    if not env_api_key:
        diagnosis["warnings"].append("WARNING: OpenRouter API key not in environment")
    if len(diagnosis["warnings"]) == 0:
        diagnosis["status"] = "✓ All systems operational"
    else:
        diagnosis["status"] = "⚠ Issues detected - see warnings"
    
    logger.info(f"Diagnostic check performed. Status: {diagnosis['status']}")
    return diagnosis


@app.post("/debug/test-openrouter")
async def test_openrouter_connection():
    """
    Test OpenRouter connection and API key validity
    
    Returns:
        Connection test results
    """
    logger.info("Starting OpenRouter connection test")
    
    test_result = {
        "timestamp": datetime.now().isoformat(),
        "test_name": "OpenRouter Connection Test",
        "results": {}
    }
    
    # Test 1: API key validation
    if not settings.OPENROUTER_API_KEY:
        test_result["results"]["api_key_check"] = "✗ FAILED: API key not configured"
        logger.error("API key test failed - key is empty")
        return test_result
    
    test_result["results"]["api_key_check"] = "✓ PASSED: API key is loaded"
    
    # Test 2: Make a simple request to OpenRouter
    try:
        logger.info("Attempting test request to OpenRouter API")
        
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://huvoiceai.example.com",
            "X-Title": "HU Voice AI"
        }
        
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Connection successful' if you receive this message."
                }
            ],
            "max_tokens": 100
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        logger.debug(f"OpenRouter response status: {response.status_code}")
        logger.debug(f"OpenRouter response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                test_result["results"]["connection_test"] = "✓ PASSED: Successfully connected to OpenRouter"
                test_result["results"]["model_response"] = data["choices"][0]["message"]["content"][:100]
            else:
                test_result["results"]["connection_test"] = "✗ FAILED: Invalid response structure"
                logger.error(f"Invalid OpenRouter response: {data}")
        else:
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"].get("message", str(error_data["error"]))
            except:
                error_msg = response.text[:200]
            
            test_result["results"]["connection_test"] = f"✗ FAILED: HTTP {response.status_code} - {error_msg}"
            logger.error(f"OpenRouter API error: {test_result['results']['connection_test']}")
    
    except requests.exceptions.Timeout:
        error_msg = "Request timeout (30 seconds)"
        test_result["results"]["connection_test"] = f"✗ FAILED: {error_msg}"
        logger.error(f"OpenRouter connection timeout: {error_msg}")
    
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error: {str(e)}"
        test_result["results"]["connection_test"] = f"✗ FAILED: {error_msg}"
        logger.error(f"OpenRouter connection error: {error_msg}")
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        test_result["results"]["connection_test"] = f"✗ FAILED: {error_msg}"
        logger.error(f"OpenRouter test error: {error_msg}", exc_info=True)
    
    return test_result


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """
    Main chat endpoint for conversational AI
    
    Args:
        request: Chat request with message and optional conversation_id
        req: FastAPI request object for rate limiting
    
    Returns:
        ChatResponse with AI answer and sources
    
    Raises:
        HTTPException: If rate limited or API key not configured
    """
    try:
        # Rate limiting
        client_ip = await get_client_ip(req)
        if not check_rate_limit(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Maximum 100 requests per 60 seconds."
            )
        
        # Check API configuration
        if not settings.OPENROUTER_API_KEY:
            logger.error("OpenRouter API key not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service not configured. Please set OPENROUTER_API_KEY."
            )
        
        app_stats["chat_requests"] += 1
        
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:12]}"
        user_message = request.message.strip()
        
        logger.info(f"Processing message for conversation: {conversation_id}")
        
        # Detect language
        user_language = language_detector.detect_language(user_message)
        logger.info(f"Detected language: {user_language}")
        
        # Get conversation history
        history = memory.get_history(conversation_id)
        
        # Gather sources
        sources = []
        
        # 1. Check University Knowledge Base
        uni_knowledge = get_university_knowledge(user_message)
        if uni_knowledge:
            sources.append(uni_knowledge)
            logger.info("Added university knowledge source")
        
        # 2. Check Wikipedia
        wiki_result = wiki_service.search(user_message, user_language)
        if wiki_result:
            sources.append(wiki_result)
            logger.info("Added Wikipedia source")
        
        # 3. Web Search (for current affairs, recent topics)
        if any(keyword in user_message.lower() for keyword in 
               ["latest", "recent", "news", "current", "today", "2024", "2025"]):
            web_results = search_service.search(user_message, max_results=2)
            if web_results:
                sources.extend(web_results)
                logger.info(f"Added {len(web_results)} web search sources")
        
        # Get AI response
        logger.info("Requesting AI response from OpenRouter...")
        ai_answer, success = openrouter_service.get_ai_response(
            user_message=user_message,
            conversation_history=history,
            user_language=user_language,
            sources=sources
        )
        
        if not success or not ai_answer:
            logger.error("="*70)
            logger.error("🔴 AI RESPONSE FAILED")
            logger.error("="*70)
            logger.error("Failed to get AI response from OpenRouter service")
            logger.error(f"  Success Flag: {success}")
            logger.error(f"  Answer: {ai_answer}")
            logger.error("TROUBLESHOOTING:")
            logger.error("  1. Check /diagnose endpoint for configuration status")
            logger.error("  2. Check /debug/test-openrouter endpoint for connection test")
            logger.error("  3. Verify OPENROUTER_API_KEY in .env file")
            logger.error("  4. Ensure API key is valid at https://openrouter.ai")
            logger.error("="*70)
            
            # Prepare fallback response with sources
            fallback_answer = f"I'm currently experiencing issues connecting to my AI service. "
            
            if sources:
                fallback_answer += f"However, I found some relevant information from {len(sources)} sources that might help: "
                source_summaries = []
                for source in sources:
                    source_summaries.append(source.get("title", source.get("summary", "Unknown")))
                fallback_answer += " | ".join(source_summaries[:2])
            else:
                fallback_answer += "Please try again in a moment, or check the /diagnose endpoint for system status."
            
            logger.warning(f"Returning fallback response: {fallback_answer[:100]}...")
            
            # Store conversation in memory (even with fallback)
            memory.add_message(
                conversation_id=conversation_id,
                role="user",
                content=user_message,
                language=user_language
            )
            
            memory.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=fallback_answer,
                language=user_language
            )
            
            # Return 503 with detailed error info
            app_stats["errors"] += 1
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "AI service is currently unavailable",
                    "message": fallback_answer,
                    "reason": "OpenRouter API connection failed",
                    "diagnostics_url": "/diagnose",
                    "test_url": "/debug/test-openrouter"
                }
            )
        
        # Store conversation in memory
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
        
        logger.info(f"Successfully processed message for conversation: {conversation_id}")
        
        # Format response
        response_sources = []
        for source in sources:
            response_sources.append({
                "type": source.get("source", "unknown"),
                "title": source.get("title", source.get("category", "")),
                "url": source.get("url", "")
            })
        
        return {
            "success": True,
            "answer": ai_answer,
            "sources": response_sources,
            "language": user_language,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        app_stats["errors"] += 1
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history
    
    Args:
        conversation_id: ID of conversation to retrieve
    
    Returns:
        Conversation history
    """
    try:
        history = memory.get_history(conversation_id)
        
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "count": len(history)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation"
        )


@app.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history
    
    Args:
        conversation_id: ID of conversation to clear
    
    Returns:
        Success message
    """
    try:
        memory.clear_conversation(conversation_id)
        
        return {
            "success": True,
            "message": f"Conversation {conversation_id} cleared",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clearing conversation"
        )


@app.get("/")
async def root():
    """
    Root endpoint with API information
    
    Returns:
        API info and available endpoints
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "health": "GET /health",
            "status": "GET /status",
            "chat": "POST /chat",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"API Key Configured: {bool(settings.OPENROUTER_API_KEY)}")
    logger.info(f"Rate Limiting: {settings.RATE_LIMIT_ENABLED}")
    logger.info(f"Debug Mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info(f"Total Requests: {app_stats['total_requests']}")
    logger.info(f"Chat Requests: {app_stats['chat_requests']}")
    logger.info(f"Errors: {app_stats['errors']}")

# ============================================================================
# RUN APPLICATION
# ============================================================================


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
