"""
HU VOICE AI - Smart Multilingual AI Companion & University Assistant
Advanced conversational voice-based AI agent with natural language processing
"""

import os
import json
import threading
import requests
import re
import html
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from bs4 import BeautifulSoup
import urllib.parse
import logging
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class HUVoiceAgent:
    """Production-Ready Multilingual Conversational AI Agent with OpenRouter"""
    
    MAX_HISTORY = 10  # Keep last 10 messages per user
    
    def __init__(self, api_key, webhook_url=None):
        # FastAPI Backend Configuration
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')  # Still stored for reference
        self.backend_url = os.getenv('HUVOICE_BACKEND_URL', 'http://127.0.0.1:8000')
        self.backend_chat_endpoint = f"{self.backend_url}/chat"
        self.request_timeout = int(os.getenv('OPENROUTER_REQUEST_TIMEOUT', '30'))
        self.retry_attempts = int(os.getenv('OPENROUTER_RETRY_ATTEMPTS', '3'))
        
        # Legacy webhook (optional fallback)
        self.webhook_url = webhook_url or os.getenv('WEBHOOK_URL')
        
        # Audio components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Agent identity
        self.agent_name = os.getenv('AGENT_NAME', 'HU Voice Agent')
        self.agent_description = os.getenv('AGENT_DESCRIPTION', 'Intelligent multilingual AI assistant for students and professionals')
        
        # State management
        self.is_listening = False
        self.conversation_history = []
        self.user_sessions = {}  # Store per-user conversation history
        
        # Logging
        logger.info(f"{'='*60}")
        logger.info(f"✓ {self.agent_name} initialized successfully")
        logger.info(f"✓ Mode: FastAPI Backend Integration")
        logger.info(f"✓ Backend URL: {self.backend_url}")
        logger.info(f"✓ Chat Endpoint: {self.backend_chat_endpoint}")
        logger.info(f"✓ Timeout: {self.request_timeout}s")
        logger.info(f"✓ Retry Attempts: {self.retry_attempts}")
        logger.info(f"{'='*60}")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            logger.info(f"[SPEAKING] {text[:80]}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in speech: {str(e)}")
    
    def detect_language(self, text):
        """Detect language: 'english', 'hindi', or 'hinglish'"""
        try:
            # Common Hindi words (transliterated)
            hindi_keywords = [
                'kaise', 'ho', 'hai', 'hoon', 'kya', 'kyun', 'kaun', 'kahan',
                'kab', 'aap', 'main', 'mera', 'tera', 'uska', 'nahi', 'bilkul',
                'theek', 'badhiya', 'acha', 'shukriya', 'namaste', 'namskar',
                'phir', 'milenge', 'bol', 'batao', 'bhai', 'dost', 'padhna',
                'likhna', 'bolna', 'sochna', 'samajhna', 'banana', 'dikhana',
                'aana', 'jana', 'dena', 'lena', 'dekho', 'suno', 'dekha', 'suna'
            ]
            
            # Hindi script detection (Devanagari)
            hindi_chars = re.findall(r'[\u0900-\u097F]', text)
            english_words = re.findall(r'\b[a-zA-Z]+\b', text)
            
            # Check for transliterated Hindi words
            text_lower = text.lower()
            transliterated_hindi_count = sum(1 for word in english_words if word in hindi_keywords)
            
            # If has actual Hindi characters, it's Hindi or Hinglish
            if len(hindi_chars) > 0:
                if len(hindi_chars) > len(english_words):
                    return 'hindi'
                else:
                    return 'hinglish'
            # If mostly transliterated Hindi words
            elif transliterated_hindi_count >= len(english_words) * 0.6:
                return 'hinglish'
            # Otherwise English
            else:
                return 'english'
        except:
            return 'english'
    
    def add_to_history(self, user_id, role, content):
        """Add message to conversation history (keep last 10)"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        
        self.user_sessions[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        })
        
        # Keep only last 10 messages
        if len(self.user_sessions[user_id]) > self.MAX_HISTORY:
            self.user_sessions[user_id] = self.user_sessions[user_id][-self.MAX_HISTORY:]
    
    def get_history(self, user_id):
        """Get last 10 messages for context"""
        return self.user_sessions.get(user_id, [])
    
    def is_greeting(self, text):
        """Check if text is a greeting"""
        greetings = {
            'english': ['hi', 'hello', 'hey', 'howdy', 'greetings', 'hii', 'hiii'],
            'hindi': ['namaste', 'namskar', 'kaise ho', 'kaisa hai', 'kya hal hai', 'kem cho'],
            'hinglish': ['hi', 'hello', 'hey', 'kaise', 'kaisa', 'kya hal']
        }
        
        lang = self.detect_language(text)
        t_lower = text.lower().strip()
        
        for greeting in greetings.get(lang, []):
            if re.search(r'\b' + greeting + r'\b', t_lower):
                return True
        return False
    
    def is_question(self, text):
        """Check if text is a question"""
        question_markers = ['?', 'what', 'kya', 'how', 'kaise', 'why', 'kyun', 'who', 'kaun', 'when', 'kab', 'where', 'kaha']
        t_lower = text.lower()
        return any(marker in t_lower for marker in question_markers)
    
    def get_context_aware_response(self, text, lang, user_id='default'):
        """Generate context-aware natural responses - act like a human friend"""
        t_lower = text.lower().strip()
        import random
        
        # Get user's first name from history if available
        user_name = "buddy"
        history = self.get_history(user_id)
        for msg in history:
            if msg['role'] == 'assistant' and 'name' in msg['content'].lower():
                # Try to extract name from previous messages
                pass
        
        # Response templates by language - FRIENDLY & CONVERSATIONAL
        responses = {
            'english': {
                'hello': [
                    f"Hey {user_name}! 😊 How's it going?",
                    f"Yo {user_name}! What's up? 🙌",
                    f"Hi there! 😄 What's on your mind?"
                ],
                'hi': [
                    f"Hey! 😊 Kaise ho?",
                    f"What's good {user_name}? 🙌",
                    f"Hey buddy! 😄 How are you?"
                ],
                'how are you': [
                    "I'm doing great, thanks for asking! How about you? How's your day going?",
                    "All good here! What's up with you? Anything interesting happening?",
                    "Feeling awesome! What about you? All good?"
                ],
                'who are you': [
                    "I'm HU Voice AI, your AI buddy! Here for chat, studies, career advice, tech talk, pretty much anything! 😊",
                    "Just your friendly AI companion - HU Voice AI! I'm here to chat, help with studies, career stuff, whatever you need!",
                    "I'm HU Voice AI, like your smart friend who knows about university life, tech, careers, and everything else!"
                ],
                'what is your name': [
                    "I'm HU Voice AI! 🎤 Think of me as your friendly university buddy.",
                    "Call me HU Voice AI - your AI friend and study companion!"
                ],
                'thanks': [
                    "Happy to help! Anything else on your mind?",
                    "Anytime! What else you got for me?",
                    "No problem! Let me know if you need anything else."
                ],
                'bye': [
                    "Catch you later! Don't be a stranger! 👋",
                    "See you soon buddy! All the best! 😊",
                    "Goodbye! Come back whenever you need to chat! 👋"
                ],
                'thank you': [
                    "You're welcome! Happy to help 😊",
                    "Glad I could help! Let me know if you need anything more."
                ]
            },
            'hindi': {
                'namaste': [
                    "Namaste! 😊 Kaise ho? Kya chal raha hai?",
                    "Namaste bhai! 🙏 Kaisa din chal raha hai?",
                    "Arey namaste! Batao, sab badhiya?"
                ],
                'hello': [
                    "Hey! 😊 Kaise ho bhai?",
                    "Arre hello! 🙌 Kya haal hai?",
                    "Arey wassup! 😄 Batao!"
                ],
                'kaise ho': [
                    "Main bilkul badhiya! 😊 Tum batao, kaisa chal raha hai?",
                    "Sab kuch theek hai mere saath! 😄 Tum kaise ho?",
                    "Main fit hoon! Aur tum? Sab badhiya?"
                ],
                'tum kaun ho': [
                    "Main HU Voice AI hoon, tera AI dost! 😊 Studies, career, tech, ya sirf bakchodi—sab mein madad kar sakta hoon!",
                    "Ek AI buddy jo university ke students ke liye bana hai! Padhai, admissions, placements, sab kuch handle kar sakta hoon.",
                    "Main tera smart friend HU Voice AI hoon! 🎤 Har cheez ke baare mein baat kar sakte hain—padhai, career, life advice, sab kuch!"
                ],
                'mera naam': [
                    "Nice to meet you! Glad to know your name bhai! 😊",
                    "Awesome! 🙌 Now we can have proper conversations!",
                    "Great! Let's be friends then! 😄"
                ],
                'shukriya': [
                    "Bilkul! Kuch aur chahiye to batana! 😊",
                    "Anytime! Aur kya help chahiye?",
                    "Khushee ki baat! Baki sab kuch pooch!"
                ],
                'phir milenge': [
                    "Phir milenge! Jaldi waapas aa jana! 👋",
                    "Bilkul! Take care bhai! 😊",
                    "See you soon! Bye! 👋"
                ],
                'mood off': [
                    "Arrey kya hua bhai? Batao na! Maybe main help kar sakun. 😊",
                    "Kya dikkat hai? Sab theek? Talk to me!",
                    "Tension mat le! Sab kuch theek ho jayega. Bol, kya problem hai?"
                ]
            },
            'hinglish': {
                'kaise ho': [
                    "Main theek hoon! 😊 Aap batao, kaisa hal hai?",
                    "Sab chill hai! 😄 Aap kaise ho?",
                    "Bilkul badhiya! Tum bolo, sab theek?"
                ],
                'hello': [
                    "Hey! 😊 Kya haal hai?",
                    "Yo! 🙌 What's up?",
                    "Arey! Kaise ho?"
                ],
                'kaun ho': [
                    "Main HU Voice AI hoon, tera AI buddy! 😊 Studies, career, tech, ya just chill and chat—sab ho sakta hai!",
                    "Ek AI friend jo help kar sakta hai har cheez mein—padhai se lekar life advice tak!",
                    "Just your AI companion bhai! HU Voice AI! 🎤"
                ],
                'thanks': [
                    "Anytime bhai! Aur kya chahiye?",
                    "Bilkul! Help karna mera kaam hai! 😊",
                    "No problem! Aur pooch!"
                ],
                'bye': [
                    "Cya! Jaldi milte hain! 👋",
                    "Take care buddy! 😊",
                    "Bye! Come back soon! 👋"
                ]
            }
        }
        
        # Find matching response
        for keyword, response_list in responses.get(lang, {}).items():
            if keyword in t_lower:
                return random.choice(response_list)
        
        return None
    
    def clean_html(self, text):
        """Clean HTML tags and entities"""
        try:
            if not text:
                return text
            
            text = re.sub(r'<[^>]*>*', '', text)
            text = re.sub(r'</?\w+[^>]*', '', text)
            text = html.unescape(text)
            text = re.sub(r'&[a-z]+;', '', text)
            text = re.sub(r'[\r\n]+', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            return text
        except Exception as e:
            logger.error(f"Error cleaning HTML: {str(e)}")
            return text
    
    def call_hu_api(self, message, conversation_id):
        """
        Call HU Voice AI FastAPI backend with proper error handling and timeout
        
        Args:
            message (str): User message
            conversation_id (str): Unique conversation ID for context
        
        Returns:
            str: Response from backend or None if failed
        """
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"[BACKEND] Attempt {attempt + 1}/{self.retry_attempts}")
                logger.info(f"[BACKEND] Request URL: {self.backend_chat_endpoint}")
                logger.info(f"[BACKEND] Message: {message[:80]}...")
                logger.info(f"[BACKEND] Conversation ID: {conversation_id}")
                
                # Prepare request payload
                payload = {
                    "message": message,
                    "conversation_id": conversation_id
                }
                logger.debug(f"[BACKEND] Request payload: {payload}")
                
                # Make request to FastAPI backend
                response = requests.post(
                    self.backend_chat_endpoint,
                    json=payload,
                    timeout=self.request_timeout,
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
                
                logger.info(f"[BACKEND] Response status code: {response.status_code}")
                logger.debug(f"[BACKEND] Raw response text: {response.text[:500]}")
                
                # Handle successful response
                if response.status_code == 200:
                    try:
                        data = response.json()
                        logger.debug(f"[BACKEND] Parsed JSON: {data}")
                        logger.info(f"[BACKEND] Response received successfully")
                        
                        success_flag = data.get('success')
                        has_answer = 'answer' in data
                        logger.debug(f"[BACKEND] success={success_flag}, has_answer={has_answer}")
                        
                        if success_flag and has_answer:
                            answer = data.get('answer', '').strip()
                            
                            if answer:
                                logger.info(f"[BACKEND] ✓ SUCCESS - Returning answer: {answer[:100]}...")
                                return answer
                            else:
                                logger.error(f"[BACKEND] ✗ FAILED - Reason: Empty answer field")
                                logger.error(f"[BACKEND] Response data: {data}")
                        else:
                            if not success_flag:
                                logger.error(f"[BACKEND] ✗ FAILED - Reason: success=false")
                            if not has_answer:
                                logger.error(f"[BACKEND] ✗ FAILED - Reason: Missing answer field")
                            logger.error(f"[BACKEND] Response data: {data}")
                            
                    except json.JSONDecodeError as je:
                        logger.error(f"[BACKEND] ✗ FAILED - Reason: Invalid JSON")
                        logger.error(f"[BACKEND] JSON decode error: {str(je)}")
                        logger.error(f"[BACKEND] Raw response text: {response.text[:500]}")
                        
                elif response.status_code == 422:
                    logger.error(f"[BACKEND] ✗ FAILED - HTTP 422 Validation error")
                    logger.error(f"[BACKEND] Response text: {response.text[:200]}")
                    return None
                    
                elif response.status_code == 500:
                    logger.error(f"[BACKEND] ✗ FAILED - HTTP 500 Server error (Attempt {attempt + 1}/{self.retry_attempts})")
                    logger.error(f"[BACKEND] Response text: {response.text[:200]}")
                    if attempt < self.retry_attempts - 1:
                        import time
                        logger.info(f"[BACKEND] Retrying in 2 seconds...")
                        time.sleep(2)
                        continue
                    
                else:
                    logger.error(f"[BACKEND] ✗ FAILED - HTTP {response.status_code}")
                    logger.error(f"[BACKEND] Response text: {response.text[:200]}")
                    
            except requests.exceptions.Timeout:
                logger.error(f"[BACKEND] ✗ FAILED - Reason: Timeout")
                logger.error(f"[BACKEND] Request timeout after {self.request_timeout}s (Attempt {attempt + 1}/{self.retry_attempts})")
                if attempt < self.retry_attempts - 1:
                    import time
                    logger.info(f"[BACKEND] Retrying in 1 second...")
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.ConnectionError as ce:
                logger.error(f"[BACKEND] ✗ FAILED - Reason: ConnectionError")
                logger.error(f"[BACKEND] Connection error (Attempt {attempt + 1}/{self.retry_attempts})")
                logger.error(f"[BACKEND] Error details: {str(ce)}")
                logger.error(f"[BACKEND] Make sure FastAPI backend is running at {self.backend_chat_endpoint}")
                if attempt < self.retry_attempts - 1:
                    import time
                    logger.info(f"[BACKEND] Retrying in 1 second...")
                    time.sleep(1)
                    continue
                    
            except Exception as e:
                logger.error(f"[BACKEND] ✗ FAILED - Reason: Unexpected exception")
                logger.error(f"[BACKEND] Exception: {str(e)}")
                import traceback
                logger.error(f"[BACKEND] Traceback: {traceback.format_exc()}")
        
        logger.error(f"[BACKEND] ✗✗✗ All {self.retry_attempts} attempts failed - returning None")
        return None
    
    def get_ai_response(self, question, user_id, lang):
        """Get response from FastAPI backend via call_hu_api function"""
        try:
            logger.info(f"[AI] Processing question: {question[:80]}...")
            logger.info(f"[AI] User ID: {user_id}")
            logger.info(f"[AI] Detected Language: {lang}")
            
            # Call FastAPI backend
            answer = self.call_hu_api(question, user_id)
            
            if answer:
                logger.info(f"[AI] ✓ Got response from backend")
                return answer
            else:
                logger.error(f"[AI] Backend returned None")
                return None
                
        except Exception as e:
            logger.error(f"[AI] Exception: {str(e)}")
            import traceback
            logger.error(f"[AI] Traceback: {traceback.format_exc()}")
            return None
    
    def search_local_knowledge(self, query, lang):
        """Search for answer in local knowledge base - return conversational result"""
        try:
            logger.warning(f"[FALLBACK SEARCH ACTIVATED]")
            logger.info(f"[SEARCH] Searching local knowledge for: {query}")
            
            headers = {'User-Agent': 'HaridwarAI/1.0'}
            
            # Try DuckDuckGo API first
            ddg_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_redirect': 1,
                'no_html': 1
            }
            
            response = requests.get(ddg_url, params=params, headers=headers, timeout=8)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            if data.get('Answer'):
                results.append(self.clean_html(data['Answer'][:500]))
            
            if data.get('AbstractText'):
                results.append(self.clean_html(data['AbstractText'][:500]))
            
            if data.get('RelatedTopics'):
                for topic in data['RelatedTopics'][:2]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        text = self.clean_html(topic['Text'])
                        if len(text) > 40:
                            results.append(text[:500])
            
            if results:
                logger.info(f"[SEARCH] Found {len(results)} results from DuckDuckGo")
                # Return conversational result, not dictionary definition
                result = results[0] if results else None
                logger.debug(f"[SEARCH] First result: {result[:100] if result else 'None'}")
                if result and len(result) < 150:
                    # For short results, make it more conversational
                    return result
                return result
            
            logger.warning(f"[SEARCH] No results found from DuckDuckGo")
            return None
            
        except Exception as e:
            logger.debug(f"Search error: {str(e)}")
            return None
    
    def get_meaningful_error(self, lang):
        """Get meaningful error message based on language"""
        errors = {
            'english': [
                "I'm having trouble connecting to my backend right now. Could you try again in a moment?",
                "My systems are a bit slow at the moment. Try asking in a different way?",
                "Something's not working right. Make sure the FastAPI backend is running!",
                "I'm unable to reach my resources. Could you rephrase your question?"
            ],
            'hindi': [
                "Mujhe apna backend reach karne mein dikkat ho rahi hai. Thode der baad try karna?",
                "Mera system thoda slow chal raha hai. Kya aap question dobara poocha sakte ho?",
                "Kuch problem aaya. FastAPI backend chal raha hai ke check karo!",
                "Mujhe issue aaya hai. Question dobara try kar de?"
            ],
            'hinglish': [
                "Backend se connect nahi ho raha. Thode der baad try kar?",
                "Mera system slow hai. Question dobara pooch sakta hai?",
                "Backend start nahi hai! Check kar de!",
                "System issue hai. Thode der baad retry kar."
            ]
        }
        
        import random
        return random.choice(errors.get(lang, errors['english']))
    
    def get_friend_like_ai_prompt(self, question, lang):
        """Create a prompt that makes AI behave like a friendly human, not a dictionary"""
        prompts = {
            'english': f"""You are HU Voice AI, a friendly, intelligent AI companion and university assistant. 

CRITICAL RULES - YOU MUST FOLLOW:
1. Act like a real human friend, NOT a dictionary or search engine
2. Never start responses with definitions or dictionary-style explanations
3. Be conversational, warm, and natural in your responses
4. Use casual language and emojis when appropriate
5. Remember the conversation context and respond accordingly

Topics you can discuss:
- General conversation and friendship
- Student life, admissions, courses
- University info: fees, hostel, placements, scholarships
- Career advice and guidance
- Technology, programming, AI
- Current affairs and politics (neutral, factual)
- Business and startups
- Motivation and life advice

RESPONSE STYLE:
- If asked "What is Python?" - Don't define it like Wikipedia. Instead: "Python is awesome for building stuff quickly! You can do web development, AI, automation... What interests you most?"
- If user is sad - Be a real friend: "Kya hua? Batao, maybe I can help"
- If user introduces themselves - Be warm: "Nice to meet you! Welcome aboard! 😊"

Current question: {question}

Respond naturally like a real friend would. Be helpful, intelligent, but NEVER act like a dictionary or encyclopedia.""",
            'hindi': f"""Tum HU Voice AI ho, ek friendly aur intelligent AI companion jo university ke students ke liye bana hai.

ZAROORI RULES - INHE ZAROOR FOLLOW KARNA:
1. Ek real human friend ki tarah behave karna, dictionary ki tarah nahi
2. Kabhi dictionary definition se start mat karna
3. Natural, warm, conversational language use karna
4. Casual tone aur emojis add karna jab appropriate ho
5. Conversation ka context yaad rakhna

Tum in topics par discuss kar sakte ho:
- Casual baat-cheet aur dosti
- Student life, admissions, courses
- University: fees, hostel, placements, scholarships
- Career guidance
- Technology, programming, AI
- Current affairs aur politics (neutral)
- Business aur startups
- Motivation aur life advice

RESPONSE STYLE:
- "Python kya hai?" par - Definition mat do. Instead: "Python bahut badhiya hai! Web, AI, automation—sab kuch kar sakte ho! Tume kya interest hai?"
- Agar user sad ho - Real friend ki tarah: "Kya hua? Batao, maybe main help kar sakun"
- Name introduce kare - Warm reply: "Nice to meet you! Welcome! 😊"

Question: {question}

Natural tarike se reply de, ek real friend ki tarah. KABHI dictionary ki tarah mat act karna.""",
            'hinglish': f"""Tum HU Voice AI ho, ek friendly aur intelligent AI buddy jo students ke liye designed ho.

IMPORTANT RULES:
1. Real friend ki tarah behave karna, dictionary nahi
2. Kabhi dictionary definitions start mat kar
3. Conversational aur natural rehna
4. Casual language use karna with emojis
5. Context remember rakhna

Topics:
- Casual chat and friendship
- Student life, admissions, courses
- University: fees, hostel, placements, scholarships
- Career guidance
- Tech, programming, AI
- Current affairs
- Business
- Motivation and life advice

RESPONSE STYLE:
- "What is Python?" - Don't define. Say: "Python is awesome! Web, AI, automation sab kar sakte ho! What interests you?"
- If sad - Be a real friend: "Kya hua? Batao!"
- Introduction - Be warm: "Nice to meet you! 😊"

Question: {question}

Respond naturally like a real friend. Never act like a dictionary."""
        }
        
        return prompts.get(lang, prompts['english'])

    def process_user_input(self, user_input, user_id='default'):
        """Process user input and generate response via FastAPI backend"""
        try:
            logger.info(f"[PROCESS] Input: {user_input}")
            logger.info(f"[PROCESS] User ID: {user_id}")
            
            # Detect language
            lang = self.detect_language(user_input)
            logger.info(f"[LANG] Detected: {lang}")
            
            # Store user message
            self.add_to_history(user_id, 'user', user_input)
            
            # MAIN PATH: Send EVERY message to FastAPI backend
            logger.info(f"[PROCESS] Calling FastAPI backend...")
            ai_response = self.get_ai_response(user_input, user_id, lang)
            
            if ai_response:
                logger.info(f"[PROCESS] Backend returned valid answer: {ai_response[:100]}...")
                self.add_to_history(user_id, 'assistant', ai_response)
                return ai_response
            
            # FALLBACK 1: Only if FastAPI backend fails - try search
            logger.warning(f"[PROCESS] Backend returned None")
            logger.warning(f"[PROCESS] Executing search fallback...")
            search_result = self.search_local_knowledge(user_input, lang)
            if search_result:
                logger.info(f"[PROCESS] Search fallback returned result: {search_result[:100]}...")
                self.add_to_history(user_id, 'assistant', search_result)
                return search_result
            
            # FALLBACK 2: Only if both fail - error message
            logger.error(f"[PROCESS] Both backend and search failed, returning error")
            error_msg = self.get_meaningful_error(lang)
            self.add_to_history(user_id, 'assistant', error_msg)
            return error_msg
            
        except Exception as e:
            logger.error(f"[PROCESS] Exception: {str(e)}")
            import traceback
            logger.error(f"[PROCESS] Traceback: {traceback.format_exc()}")
            lang = self.detect_language(user_input)
            error_msg = self.get_meaningful_error(lang)
            self.add_to_history(user_id, 'assistant', error_msg)
            return error_msg
    
    def listen(self):
        """Listen for voice input"""
        try:
            self.is_listening = True
            logger.info("[LISTENING] Waiting for voice input...")
            
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"[HEARD] {text}")
            self.is_listening = False
            return text
            
        except sr.UnknownValueError:
            response = "Sorry, I didn't catch that. Could you say it again?"
            self.speak(response)
            self.is_listening = False
            return None
        except sr.RequestError as e:
            logger.error(f"Speech API error: {str(e)}")
            self.speak("There's an issue with the speech service")
            self.is_listening = False
            return None
        except Exception as e:
            logger.error(f"Listening error: {str(e)}")
            self.is_listening = False
            return None
    
    def voice_interaction(self):
        """Voice-based interaction loop"""
        try:
            greeting = f"Hi! I'm {self.agent_name}, your {self.agent_description}. What would you like to know?"
            self.speak(greeting)
            
            while True:
                user_input = self.listen()
                
                if user_input is None:
                    continue
                
                if any(word in user_input.lower() for word in ['exit', 'quit', 'bye', 'goodbye', 'phir milenge']):
                    self.speak("Thanks for chatting! Catch you later! 👋")
                    break
                
                answer = self.process_user_input(user_input)
                self.speak(answer)
                
        except KeyboardInterrupt:
            logger.info("Voice interaction interrupted")
            self.speak("Goodbye!")
        except Exception as e:
            logger.error(f"Voice interaction error: {str(e)}")
    
    def get_user_history(self, user_id):
        """Get user's conversation history"""
        return self.get_history(user_id)
    
    def clear_user_history(self, user_id):
        """Clear user's conversation history"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        logger.info(f"History cleared for user: {user_id}")


# Flask Web Interface
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'haridwar-secret-key-2024-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
agent = None

USERS_DB = 'users.json'

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

def initialize_agent(api_key, webhook_url=None):
    """Initialize agent"""
    global agent
    agent = HUVoiceAgent(api_key, webhook_url)
    return agent

@app.route('/')
def index():
    """Main page"""
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
    """Login"""
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
    """Signup"""
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
    """Logout"""
    try:
        if 'user' in session:
            user_email = session['user'].get('email')
            session.pop('user', None)
            logger.info(f"[LOGOUT] User: {user_email}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/api/ask', methods=['POST'])
@login_required
def ask_question():
    """Ask question API"""
    try:
        if not agent:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question required'}), 400
        
        user_email = session['user']['email']
        answer = agent.process_user_input(question, user_email)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Ask error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    """Get conversation history"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    user_email = session['user']['email']
    history = agent.get_user_history(user_email)
    
    return jsonify({'history': history})

@app.route('/api/clear-history', methods=['POST'])
@login_required
def clear_history_api():
    """Clear history"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    user_email = session['user']['email']
    agent.clear_user_history(user_email)
    
    return jsonify({'success': True})

@app.route('/api/status', methods=['GET'])
@login_required
def get_status():
    """Get status"""
    if not agent:
        return jsonify({'status': 'not_initialized'})
    
    user_email = session['user']['email']
    history = agent.get_user_history(user_email)
    
    return jsonify({
        'status': 'active',
        'agent_name': agent.agent_name,
        'agent_description': agent.agent_description,
        'listening': agent.is_listening,
        'message_count': len(history)
    })

@app.route('/api/image', methods=['POST'])
@login_required
def upload_image():
    """Upload and analyze image"""
    try:
        if not agent:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get optional prompt
        prompt = request.form.get('prompt', None)
        
        logger.info(f"[IMAGE] Received file: {file.filename}")
        
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            file.save(tmp.name)
            temp_path = tmp.name
        
        try:
            # Call FastAPI image analysis endpoint
            import requests
            api_url = 'http://127.0.0.1:8000/analyze-image'
            
            with open(temp_path, 'rb') as img_file:
                files = {'file': img_file}
                data = {'prompt': prompt} if prompt else {}
                
                response = requests.post(
                    api_url,
                    files=files,
                    data=data,
                    timeout=90
                )
            
            if response.status_code == 200:
                result = response.json()
                user_email = session['user']['email']
                
                return jsonify({
                    'success': result.get('success', True),
                    'answer': result.get('answer', ''),
                    'objects': result.get('objects', []),
                    'filename': file.filename,
                    'timestamp': result.get('timestamp', datetime.now().isoformat()),
                    'user': user_email
                })
            else:
                logger.error(f"[IMAGE] FastAPI error: {response.status_code} - {response.text}")
                return jsonify({
                    'success': False,
                    'error': f'Vision API error: {response.status_code}'
                }), 500
        
        finally:
            # Cleanup temp file
            if Path(temp_path).exists():
                Path(temp_path).unlink()
                logger.info(f"[IMAGE] Cleaned up temp file")
    
    except Exception as e:
        logger.error(f"[IMAGE] Upload error: {str(e)}")
        import traceback
        logger.error(f"[IMAGE] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-input', methods=['POST'])
@login_required
def voice_input():
    """Voice input API"""
    try:
        if not agent:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        text = agent.listen()
        
        if text is None:
            return jsonify({'success': False, 'text': None})
        
        user_email = session['user']['email']
        answer = agent.process_user_input(text, user_email)
        
        return jsonify({
            'success': True,
            'heard': text,
            'answer': answer
        })
        
    except Exception as e:
        logger.error(f"Voice error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/<path:webhook_id>', methods=['POST', 'GET'])
def webhook_handler(webhook_id):
    """Webhook handler"""
    try:
        if request.method == 'POST':
            data = request.json or {}
        else:
            data = request.args.to_dict()
        
        question = data.get('question') or data.get('q') or data.get('message')
        
        if not question:
            return jsonify({'error': 'Question required'}), 400
        
        if not agent:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        # Use webhook_id as user_id for context
        answer = agent.process_user_input(question, webhook_id)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'agent': agent.agent_name,
            'webhook_id': webhook_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY', 'sk-or-v1-YOUR_KEY_HERE')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://huassist2010.app.n8n.cloud/webhook/38f72ae7-8140-4887-b3b5-ce7e118f7c13')
    
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║     HU VOICE AI - Smart Multilingual Companion        ║
    ║  Advanced Conversational Voice-Based AI Assistant     ║
    ║     University Assistant & Educational Chatbot        ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    initialize_agent(API_KEY, WEBHOOK_URL)
    
    print("\n[INFO] Starting Flask server...")
    print("[INFO] Web Interface: http://localhost:5000")
    print("[INFO] API Base: http://localhost:5000/api")
    if WEBHOOK_URL:
        print(f"[INFO] Webhook: {WEBHOOK_URL[:60]}...")
    print("\n[READY] HU Voice AI is ready to assist!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
