"""
HARIDWAR UNIVERSITY AI - Unified Flask Application
Merged FastAPI Backend + Flask Dashboard into single Flask app
Production-ready for Render.com deployment
"""

import os
import json
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import OrderedDict
from functools import wraps
from typing import Optional, Dict, List, Tuple

# Core libraries
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
try:
    import speech_recognition as sr
except Exception:
    sr = None
try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# AI/ML Libraries
try:
    from langdetect import detect, LangDetectException
except Exception:
    detect = None
    LangDetectException = Exception

try:
    import wikipedia
except Exception:
    wikipedia = None

try:
    from duckduckgo_search import DDGS
except Exception:
    DDGS = None

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CORE SERVICES (Merged from api/services)
# ============================================================================

class LanguageDetector:
    """Detect user language (Hindi, English, Hinglish)"""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Detect language of input text"""
        try:
            if not text or len(text) < 2:
                return "en"
            
            if detect is None:
                # Fallback: detect by character type
                hindi_chars = any('\u0900' <= c <= '\u097F' for c in text)
                english_chars = any(c.isalpha() and ord(c) < 128 for c in text)
                
                if hindi_chars and english_chars:
                    return "hinglish"
                elif hindi_chars:
                    return "hi"
                return "en"
            
            detected = detect(text)
            
            # Hinglish detection (mixed Hindi-English)
            hindi_chars = any('\u0900' <= c <= '\u097F' for c in text)
            english_chars = any(c.isalpha() and ord(c) < 128 for c in text)
            
            if hindi_chars and english_chars:
                return "hinglish"
            elif detected == "hi":
                return "hi"
            else:
                return "en"
        
        except Exception as e:
            logger.warning(f"Language detection error: {str(e)}")
            return "en"


class ConversationMemory:
    """Manages conversation history with memory limits"""
    
    def __init__(self, max_history: int = 20, timeout_hours: int = 1):
        self.conversations: Dict[str, List[Dict]] = OrderedDict()
        self.max_history = max_history
        self.timeout = timedelta(hours=timeout_hours)
        self.timestamps = {}
    
    def add_message(self, conversation_id: str, role: str, content: str, language: str = "en") -> None:
        """Add a message to conversation history"""
        try:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
                self.timestamps[conversation_id] = datetime.now()
            
            message = {
                "role": role,
                "content": content,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
            self.conversations[conversation_id].append(message)
            
            # Keep only last N messages
            if len(self.conversations[conversation_id]) > self.max_history:
                self.conversations[conversation_id] = \
                    self.conversations[conversation_id][-self.max_history:]
            
            logger.info(f"Message added to conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
    
    def get_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history"""
        if conversation_id not in self.conversations:
            return []
        return self.conversations[conversation_id]
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Conversation {conversation_id} cleared")


class OpenRouterService:
    """Handle AI responses via OpenRouter API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = int(os.getenv('OPENROUTER_REQUEST_TIMEOUT', '30'))
        self.model = "openrouter/auto"  # Auto-select best model
    
    def generate_system_prompt(self, user_language: str) -> str:
        """Generate context-aware system prompt based on HU Voice AI rules"""
        base_prompt = """You are HU Voice AI - an intelligent multilingual AI assistant for Haridwar University.

CORE RULES:

LANGUAGE MATCHING:
• Always respond in the SAME language as the user
• Hindi → Hindi response
• English → English response  
• Hinglish → Hinglish response

RESPONSE FORMAT:
• NEVER give long paragraphs
• Always use bullet points and numbered lists
• Keep sentences short and concise
• Use structured formatting for every response
• Never answer like a dictionary

COURSE INFORMATION:
When user asks about courses, provide:
• Course Name
• Duration
• Eligibility
• Mode (Regular/Online)
• Fees (if available)
• Career Opportunities
Example:
BCA
• Duration: 3 Years
• Eligibility: 12th Pass
• Mode: Regular
• Fees: ₹[Amount]
• Career Options: Software Developer, Web Developer, Data Analyst

UNIVERSITY INFORMATION:
• Use bullet points ONLY
• Keep answers structured and concise
• Organize by category

IMAGE HANDLING:
When user uploads an image:
• Analyze the image thoroughly
• Describe objects, people, text, colors, and important details
• Give output in bullet points format
• Be specific and detailed

IMAGE GENERATION:
When user asks to "generate image", "create image", "design logo", "make poster":
• Create a detailed image prompt
• Generate the image
• Never refuse unless the request is unsafe
• Provide helpful alternatives if request is unclear

WEB SEARCH:
If information is not available:
• Search web sources automatically
• Give the best available answer
• Cite sources when relevant
• Keep answer concise with bullet points

COMPARISONS:
• Use tables when possible
• Or use bullet lists for side-by-side comparison
• Make differences clear and obvious

INSTRUCTIONS:
For step-by-step instructions:
• Use NUMBERED format (1, 2, 3...)
• Keep each step clear and actionable
• Add helpful tips where relevant

CONVERSATION STYLE:
• Talk naturally like a real friend
• Never be robotic or dictionary-like
• Respond to greetings warmly: "Hello bhai! 😊 Kaise ho?"
• Keep conversation context
• Do not repeat sentences
• Be helpful and informative
• Use emojis appropriately

GENERAL BEHAVIOR:
• Always act as a smart university assistant + general AI assistant
• Provide accurate, helpful, and relevant information
• Maintain professional but friendly tone
• Prioritize user understanding over technical accuracy
• Ask clarifying questions if user's request is unclear
• Suggest alternatives when something isn't possible"""
        
        return base_prompt
    
    def get_ai_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        user_language: str,
        sources: List[Dict] = None
    ) -> Tuple[Optional[str], bool]:
        """Get AI response from OpenRouter"""
        try:
            if not self.api_key:
                logger.error("OpenRouter API key not configured")
                return None, False
            
            # Prepare messages
            messages = []
            
            # Add conversation history
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare sources context
            sources_context = ""
            if sources:
                sources_context = "\n\nRelevant Information:\n"
                for source in sources:
                    if isinstance(source, dict):
                        sources_context += f"- {source.get('content', str(source))}\n"
            
            # Call OpenRouter API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "system": self.generate_system_prompt(user_language),
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                
                if answer:
                    logger.info(f"Got AI response: {answer[:100]}...")
                    return answer, True
                else:
                    logger.error("Empty response from OpenRouter")
                    return None, False
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None, False
        
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return None, False


class SearchService:
    """Web search via DuckDuckGo"""
    
    @staticmethod
    def search(query: str, max_results: int = 3) -> List[Dict]:
        """Search web with DuckDuckGo"""
        try:
            if DDGS is None:
                logger.warning("DuckDuckGo search not available")
                return []
            
            results = []
            ddgs = DDGS()
            search_results = ddgs.text(query, max_results=max_results, timelimit='y')
            
            for result in search_results:
                results.append({
                    "type": "web",
                    "source": "Web Search",
                    "title": result.get("title", ""),
                    "content": result.get("body", ""),
                    "url": result.get("href", "")
                })
            
            logger.info(f"Found {len(results)} web results for: {query}")
            return results
        
        except Exception as e:
            logger.warning(f"Web search error: {str(e)}")
            return []


class WikipediaService:
    """Wikipedia search"""
    
    @staticmethod
    def search(query: str, language: str = "en") -> Optional[Dict]:
        """Search Wikipedia"""
        try:
            if wikipedia is None:
                logger.warning("Wikipedia not available")
                return None
            
            # Set language
            wikipedia.set_lang('hi' if language == 'hi' else 'en')
            
            search_results = wikipedia.search(query, results=1)
            if not search_results:
                return None
            
            page = wikipedia.page(search_results[0])
            
            return {
                "type": "wikipedia",
                "source": "Wikipedia",
                "title": page.title,
                "content": page.summary[:500],
                "url": page.url
            }
        
        except Exception as e:
            logger.debug(f"Wikipedia search error: {str(e)}")
            return None


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
    "fees": {
        "engineering": "₹3 lakhs per annum",
        "management": "₹5 lakhs per annum",
        "science": "₹1.5 lakhs per annum",
        "arts": "₹80000 per annum"
    }
}


def get_university_knowledge(query: str) -> Optional[Dict]:
    """Search university knowledge base and format response nicely"""
    query_lower = query.lower()
    
    for category, items in UNIVERSITY_KB.items():
        if category in query_lower:
            # Format category response nicely
            content_list = []
            if isinstance(items, dict):
                for key, value in items.items():
                    content_list.append(f"{key}: {value}")
            formatted_content = " | ".join(content_list) if content_list else str(items)
            
            return {
                "source": "University Knowledge",
                "category": category,
                "content": formatted_content
            }
        
        for key, value in items.items():
            if key in query_lower or key.replace("_", " ") in query_lower:
                return {
                    "source": "University Knowledge",
                    "category": category,
                    "key": key,
                    "content": f"{key}: {value}"
                }
    
    return None


def generate_response_from_sources(query: str, sources: List[Dict], language: str = "en") -> str:
    """Generate a smart, natural response from gathered sources"""
    try:
        if not sources:
            if language == "hi":
                return "मुझे इसके बारे में जानकारी नहीं मिल सकी। कृपया दूसरे तरीके से पूछें।"
            elif language == "hinglish":
                return "Mujhe iska answer nahi mil paya. Kya aap kuch aur puch sakte ho?"
            else:
                return "I couldn't find information on that. Could you rephrase your question?"
        
        # Extract the best response
        best_response = ""
        
        # Priority 1: University Knowledge
        for source in sources:
            if source.get("source") == "University Knowledge":
                content = source.get("content", "")
                if content:
                    # Clean up the content - remove dictionary formatting
                    content = str(content).strip()
                    # Remove dictionary markers but keep the data
                    if content.startswith("{") and content.endswith("}"):
                        # Parse dictionary-like string
                        try:
                            import ast
                            data = ast.literal_eval(content)
                            items = []
                            for k, v in data.items():
                                items.append(f"• {k}: {v}")
                            best_response = "\n".join(items)
                        except:
                            # Fallback: just clean the string
                            content = content.replace("{", "").replace("}", "").replace("'", "")
                            best_response = content
                    else:
                        best_response = content
                    break
        
        # Priority 2: Wikipedia (if no university knowledge)
        if not best_response:
            for source in sources:
                if source.get("title") == "Wikipedia" or "wiki" in source.get("source", "").lower():
                    content = source.get("content", "")
                    if content and len(str(content).strip()) > 30:
                        best_response = str(content)[:400]
                        break
        
        # Priority 3: Web search
        if not best_response:
            for source in sources:
                content = source.get("content", "")
                if content and len(str(content).strip()) > 30:
                    best_response = str(content)[:400]
                    break
        
        # Return the response
        if best_response and len(best_response.strip()) > 15:
            # Smart truncation for longer responses
            if len(best_response) > 500:
                best_response = best_response[:500].rsplit(".", 1)[0] + "."
            return best_response.strip()
        
        # Fallback
        if language == "hi":
            return "मुझे इस विषय पर कोई स्पष्ट जानकारी नहीं मिली। कृपया पुन: प्रयास करें।"
        elif language == "hinglish":
            return "Mujhe iska clear answer nahi mil paya. Dobara try karo?"
        else:
            return "I couldn't find clear information on this. Please try asking differently."
    
    except Exception as e:
        logger.warning(f"Error generating response: {str(e)}")
        return "Let me search for more information. Please try again."


# ============================================================================
# FLASK APPLICATION
# ============================================================================

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'haridwar-secret-key-2024-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize services
memory = ConversationMemory()
language_detector = LanguageDetector()
openrouter_service = OpenRouterService()
search_service = SearchService()
wiki_service = WikipediaService()

USERS_DB = 'users.json'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_users_db():
    """Load users from JSON"""
    if os.path.exists(USERS_DB):
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}


def save_users_db(users):
    """Save users to JSON"""
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(f):
    """Protect routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated


# ============================================================================
# ROUTES: Authentication
# ============================================================================

@app.route('/')
def index():
    """Main page - redirect to dashboard if logged in"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard"""
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login endpoint"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        users = load_users_db()
        user_data = users.get(email)
        
        if not user_data or user_data['password'] != hash_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session['user'] = {
            'email': email,
            'fullname': user_data.get('fullname', 'User')
        }
        
        logger.info(f"[LOGIN] User: {email}")
        return jsonify({'success': True, 'message': 'Login successful'})
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500


@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Signup endpoint"""
    try:
        data = request.json
        fullname = data.get('fullname', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not fullname or not email or not password:
            return jsonify({'error': 'All fields required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password minimum 6 chars'}), 400
        
        if '@' not in email:
            return jsonify({'error': 'Invalid email'}), 400
        
        users = load_users_db()
        
        if email in users:
            return jsonify({'error': 'Email already registered'}), 409
        
        users[email] = {
            'fullname': fullname,
            'password': hash_password(password),
            'created_at': datetime.now().isoformat()
        }
        
        save_users_db(users)
        
        session['user'] = {
            'email': email,
            'fullname': fullname
        }
        
        logger.info(f"[SIGNUP] New user: {email}")
        return jsonify({'success': True, 'message': 'Account created'})
        
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({'error': 'Signup failed'}), 500


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout endpoint"""
    try:
        if 'user' in session:
            user_email = session['user'].get('email')
            session.pop('user', None)
            logger.info(f"[LOGOUT] User: {user_email}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500


# ============================================================================
# ROUTES: Chat & AI
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    Main chat endpoint - MERGED FROM FASTAPI
    Always responds with data from web, wiki, or university knowledge
    """
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id') or session['user']['email']
        
        if not user_message:
            return jsonify({'error': 'Message required'}), 400
        
        logger.info(f"[CHAT] Processing: {user_message[:80]}")
        
        # Detect language
        user_language = language_detector.detect_language(user_message)
        logger.info(f"[CHAT] Detected language: {user_language}")
        
        # Get conversation history
        history = memory.get_history(conversation_id)
        
        # Gather sources - ALWAYS try to collect data
        sources = []
        
        # 1. Check University Knowledge Base
        uni_knowledge = get_university_knowledge(user_message)
        if uni_knowledge:
            sources.append(uni_knowledge)
            logger.info("Added university knowledge source")
        
        # 2. Check Wikipedia (always try)
        try:
            wiki_result = wiki_service.search(user_message, user_language)
            if wiki_result:
                sources.append(wiki_result)
                logger.info("Added Wikipedia source")
        except Exception as e:
            logger.warning(f"Wikipedia search failed: {str(e)}")
        
        # 3. Web Search (always try for any query)
        try:
            web_results = search_service.search(user_message, max_results=2)
            if web_results:
                sources.extend(web_results)
                logger.info(f"Added {len(web_results)} web sources")
        except Exception as e:
            logger.warning(f"Web search failed: {str(e)}")
        
        # Try to get AI response
        ai_answer = None
        try:
            ai_answer, success = openrouter_service.get_ai_response(
                user_message=user_message,
                conversation_history=history,
                user_language=user_language,
                sources=sources
            )
            
            if success and ai_answer:
                logger.info("Got AI response from OpenRouter")
            else:
                logger.warning("OpenRouter returned no response, using fallback")
                ai_answer = None
        
        except Exception as e:
            logger.warning(f"OpenRouter API failed: {str(e)}, using fallback")
            ai_answer = None
        
        # Fallback: Generate response from gathered sources
        if not ai_answer:
            try:
                ai_answer = generate_response_from_sources(user_message, sources, user_language)
                logger.info("Generated response from gathered sources")
            except Exception as e:
                logger.error(f"Failed to generate fallback response: {str(e)}")
                # Last resort fallback
                if user_language == "hi":
                    ai_answer = "मुझे माफ करें, मुझे इस समय उत्तर देने में समस्या हो रही है। कृपया बाद में पुन: प्रयास करें।"
                elif user_language == "hinglish":
                    ai_answer = "Sorry bhai! Abhi respond nahi kar pa raha. Thoda baad me dobara try karna."
                else:
                    ai_answer = "Sorry, I'm having trouble responding right now. Please try again later."
        
        # Store in memory
        memory.add_message(conversation_id, "user", user_message, user_language)
        memory.add_message(conversation_id, "assistant", ai_answer, user_language)
        
        # Format response
        response_sources = []
        for source in sources:
            response_sources.append({
                "type": source.get("type", "unknown"),
                "title": source.get("title", source.get("category", "")),
                "url": source.get("url", "")
            })
        
        return jsonify({
            "success": True,
            "response": ai_answer,  # Changed from "answer" to "response" for consistency
            "answer": ai_answer,     # Keep both for compatibility
            "sources": response_sources,
            "language": user_language,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        # Even on critical error, return a response
        if 'user' in session:
            conversation_id = session['user']['email']
        else:
            conversation_id = "unknown"
        
        return jsonify({
            'success': False,
            'response': 'An error occurred while processing your request. Please try again.',
            'error': str(e),
            'conversation_id': conversation_id
        }), 500


@app.route('/api/ask', methods=['POST'])
@login_required
def ask_question():
    """Ask question API (legacy name)"""
    return api_chat()


@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    """Get conversation history"""
    conversation_id = session['user']['email']
    history = memory.get_history(conversation_id)
    return jsonify({'history': history})


@app.route('/api/clear-history', methods=['POST'])
@login_required
def clear_history_api():
    """Clear history"""
    conversation_id = session['user']['email']
    memory.clear_conversation(conversation_id)
    return jsonify({'success': True})


@app.route('/api/status', methods=['GET'])
@login_required
def get_status():
    """Get status"""
    conversation_id = session['user']['email']
    history = memory.get_history(conversation_id)
    
    return jsonify({
        'status': 'active',
        'agent_name': 'Haridwar University AI',
        'listening': False,
        'message_count': len(history)
    })


# ============================================================================
# ROUTES: Image Analysis
# ============================================================================

@app.route('/api/image', methods=['POST'])
@login_required
def upload_image():
    """Upload and analyze image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        prompt = request.form.get('prompt', None)
        logger.info(f"[IMAGE] Received file: {file.filename}")
        
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            file.save(tmp.name)
            temp_path = tmp.name
        
        try:
            # For now, return a placeholder response
            # In production, integrate with Google Vision API or similar
            return jsonify({
                'success': True,
                'answer': 'Image analysis feature coming soon',
                'objects': [],
                'filename': file.filename,
                'timestamp': datetime.now().isoformat()
            })
        
        finally:
            # Cleanup temp file
            if Path(temp_path).exists():
                Path(temp_path).unlink()
                logger.info(f"[IMAGE] Cleaned up temp file")
    
    except Exception as e:
        logger.error(f"[IMAGE] Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: Voice Input
# ============================================================================

@app.route('/api/voice-input', methods=['POST'])
@login_required
def voice_input():
    """Voice input API"""
    try:
        # Voice input would require microphone access from client
        # This is a placeholder
        return jsonify({
            'success': False,
            'error': 'Voice input not available in web interface. Use text input instead.'
        })
    
    except Exception as e:
        logger.error(f"Voice error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: Webhook (Public)
# ============================================================================

@app.route('/webhook/<path:webhook_id>', methods=['POST', 'GET'])
def webhook_handler(webhook_id):
    """Webhook handler - public endpoint - always responds with data"""
    try:
        if request.method == 'POST':
            data = request.json or {}
        else:
            data = request.args.to_dict()
        
        question = data.get('question') or data.get('q') or data.get('message')
        
        if not question:
            return jsonify({'error': 'Question required'}), 400
        
        conversation_id = f"webhook_{webhook_id}"
        
        # Detect language
        user_language = language_detector.detect_language(question)
        history = memory.get_history(conversation_id)
        
        # Gather sources
        sources = []
        try:
            uni_knowledge = get_university_knowledge(question)
            if uni_knowledge:
                sources.append(uni_knowledge)
        except Exception as e:
            logger.warning(f"University knowledge failed: {str(e)}")
        
        try:
            wiki_result = wiki_service.search(question, user_language)
            if wiki_result:
                sources.append(wiki_result)
        except Exception as e:
            logger.warning(f"Wikipedia failed: {str(e)}")
        
        try:
            web_results = search_service.search(question, max_results=2)
            if web_results:
                sources.extend(web_results)
        except Exception as e:
            logger.warning(f"Web search failed: {str(e)}")
        
        # Try AI response
        ai_answer = None
        try:
            ai_answer, success = openrouter_service.get_ai_response(
                user_message=question,
                conversation_history=history,
                user_language=user_language,
                sources=sources
            )
            if not success:
                ai_answer = None
        except Exception as e:
            logger.warning(f"OpenRouter failed: {str(e)}")
            ai_answer = None
        
        # Fallback
        if not ai_answer:
            try:
                ai_answer = generate_response_from_sources(question, sources, user_language)
            except Exception as e:
                logger.error(f"Fallback failed: {str(e)}")
                ai_answer = "Unable to process at this time."
        
        # Store in memory
        memory.add_message(conversation_id, "user", question, user_language)
        memory.add_message(conversation_id, "assistant", ai_answer, user_language)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': ai_answer,
            'response': ai_answer,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'answer': 'Error processing request'
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"{'='*60}")
    logger.info(f"✓ HARIDWAR UNIVERSITY AI - Starting Application")
    logger.info(f"✓ Port: {port}")
    logger.info(f"✓ Debug Mode: {debug}")
    logger.info(f"✓ Flask/Unified Application Mode")
    logger.info(f"{'='*60}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=False
    )
