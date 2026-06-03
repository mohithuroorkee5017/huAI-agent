"""
OpenRouter AI Integration Service
Handles communication with OpenRouter API for AI responses with automatic fallback models
"""

import requests
import logging
from typing import List, Dict, Optional, Tuple
from config import settings
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detect user language (Hindi, English, Hinglish)"""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language of input text
        
        Args:
            text: Input text to analyze
        
        Returns:
            Language code: 'hi' (Hindi), 'en' (English), or 'hinglish'
        """
        try:
            if not text or len(text) < 2:
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
        
        except LangDetectException:
            return "en"
        except Exception as e:
            logger.warning(f"Language detection error: {str(e)}")
            return "en"


class OpenRouterService:
    """Handle AI responses via OpenRouter API with automatic fallback"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.primary_model = settings.OPENROUTER_MODEL
        self.fallback_models = settings.OPENROUTER_FALLBACK_MODELS
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = 30
        self.current_model_index = 0
        
        # Log initialization
        logger.info(f"Initializing OpenRouter Service")
        logger.info(f"  API Key Configured: {'✓ YES' if self.api_key else '✗ NO'}")
        if self.api_key:
            logger.info(f"  API Key Preview: {self.api_key[:20]}...{self.api_key[-4:]}")
        logger.info(f"  Primary Model: {self.primary_model}")
        logger.info(f"  Fallback Models: {len(self.fallback_models)}")
    
    def _get_next_model(self) -> str:
        """Get next model to try (including primary and fallbacks)"""
        all_models = [self.primary_model] + [m for m in self.fallback_models if m != self.primary_model]
        if self.current_model_index >= len(all_models):
            self.current_model_index = 0
        
        model = all_models[self.current_model_index]
        self.current_model_index += 1
        return model
    
    def _reset_model_index(self) -> None:
        """Reset model index for next request"""
        self.current_model_index = 0
    
    @staticmethod
    def generate_system_prompt(user_language: str) -> str:
        """
        Generate context-aware system prompt based on user language
        
        Args:
            user_language: Detected user language
        
        Returns:
            System prompt string
        """
        base_prompt = """You are HU Voice AI.

Behavior Rules:
* Reply in the same language as the user.
* Hindi -> Hindi response.
* Hinglish -> Hinglish response.
* English -> English response.
* Never behave like a dictionary.
* Never explain simple greetings.
* Talk naturally like a real friend.
* Keep conversation context.
* Do not repeat the same sentence.
* Give direct and useful answers.
* Support IT, Non-IT, education, coding, politics, current affairs, career guidance and general conversation.
* If user says "hi", "hello", "kaise ho", respond naturally instead of giving definitions.
* Be warm, friendly and conversational.

Examples:
User: hi
Assistant: Kya haal bhai 😄

User: hello
Assistant: Hello bhai! Kaise ho?

User: kaise ho
Assistant: Badhiya bhai 😄 Tu suna kya chal raha hai?

User: MCA ke baad job ka scope hai?
Assistant: Haan bhai, MCA ke baad Software Developer, Backend Developer, Data Analyst aur bahut roles mil sakte hain."""
        
        language_instructions = {
            "hi": "\n\nIMPORTANT: The user is speaking Hindi. Reply in Hindi only.",
            "en": "\n\nIMPORTANT: The user is speaking English. Reply in English only.",
            "hinglish": "\n\nIMPORTANT: The user is speaking Hinglish (mixed Hindi-English). Reply in Hinglish using the same mix."
        }
        
        return base_prompt + language_instructions.get(user_language, "")
    
    
    def get_ai_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        user_language: str = "en",
        sources: List[Dict] = None
    ) -> Tuple[Optional[str], bool]:
        """
        Get AI response from OpenRouter API with automatic fallback
        
        Args:
            user_message: Current user message
            conversation_history: List of previous messages
            user_language: Detected user language
            sources: Optional knowledge sources to include
        
        Returns:
            Tuple of (response_text, success_flag)
        """
        if not self.api_key:
            logger.error("CRITICAL: OpenRouter API key not configured")
            logger.error("  → Set OPENROUTER_API_KEY environment variable")
            logger.error("  → Or add it to .env file in the api/ directory")
            return None, False
        
        logger.info(f"Processing AI request for language: {user_language}")
        logger.debug(f"  Message length: {len(user_message)} chars")
        logger.debug(f"  History messages: {len(conversation_history)}")
        logger.debug(f"  Sources: {len(sources) if sources else 0}")
        
        self._reset_model_index()
        max_retries = len(self.fallback_models) + 1
        last_error = None
        
        for attempt in range(max_retries):
            current_model = self._get_next_model()
            
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries}: Trying model: {current_model}")
                
                # Build messages with conversation history
                messages = []
                
                # Add system prompt to guide conversation behavior
                system_prompt = self.generate_system_prompt(user_language)
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
                
                # Add recent conversation context (last 10 messages)
                if conversation_history:
                    for msg in conversation_history[-10:]:
                        messages.append({
                            "role": msg.get("role", "user"),
                            "content": msg.get("content", "")
                        })
                
                # Add current message
                messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Add sources context if available
                if sources:
                    source_info = self._format_sources(sources)
                    messages[-1]["content"] += f"\n\n{source_info}"
                
                # Prepare request headers
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://huvoiceai.example.com",
                    "X-Title": "HU Voice AI"
                }
                
                # Validate headers
                if not headers.get("Authorization"):
                    logger.error(f"CRITICAL: Authorization header is empty!")
                    logger.error(f"  API Key: {self.api_key}")
                    logger.error(f"  Header formed: {headers['Authorization']}")
                    last_error = "Authorization header is empty"
                    continue
                
                logger.debug(f"Authorization header formed: {headers['Authorization'][:30]}...")
                
                # Prepare request payload
                payload = {
                    "model": current_model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1024,
                    "top_p": 0.9
                }
                
                # Log request details
                logger.debug(f"OpenRouter API Request:")
                logger.debug(f"  URL: {self.base_url}/chat/completions")
                logger.debug(f"  Model: {current_model}")
                logger.debug(f"  Messages: {len(messages)}")
                logger.debug(f"  Headers: {headers}")
                
                # Make API call
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Log response details
                logger.debug(f"OpenRouter API Response Status: {response.status_code}")
                logger.debug(f"OpenRouter API Response Body: {response.text[:500]}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "choices" not in data or len(data["choices"]) == 0:
                        logger.error(f"Invalid response structure from OpenRouter: {data}")
                        last_error = "Invalid response structure"
                        continue
                    
                    response_text = data["choices"][0]["message"]["content"]
                    logger.info(f"Successfully got AI response from model: {current_model}")
                    self._reset_model_index()
                    return response_text, True
                
                else:
                    # Log error and try next model
                    error_msg = f"OpenRouter API error: {response.status_code}"
                    error_details = ""
                    
                    try:
                        error_data = response.json()
                        if "error" in error_data:
                            error_details = error_data['error'].get('message', str(error_data['error']))
                            error_msg += f" - {error_details}"
                    except:
                        error_details = response.text[:200]
                        error_msg += f" - {error_details}"
                    
                    # Special handling for 401 (authentication error)
                    if response.status_code == 401:
                        logger.error("="*70)
                        logger.error("🔴 AUTHENTICATION ERROR (401) - OpenRouter API")
                        logger.error("="*70)
                        logger.error(f"Error Details: {error_details}")
                        logger.error(f"API Key Status: {('✓ LOADED' if self.api_key else '✗ MISSING')}")
                        if self.api_key:
                            logger.error(f"API Key Format: {self.api_key[:20]}...{self.api_key[-4:]}")
                        logger.error(f"Authorization Header: {headers.get('Authorization', 'NOT SET')[:30]}...")
                        logger.error("POSSIBLE CAUSES:")
                        logger.error("  1. API key is invalid or expired")
                        logger.error("  2. API key not set in .env file or environment")
                        logger.error("  3. Headers not being transmitted correctly")
                        logger.error("NEXT STEPS:")
                        logger.error("  1. Check .env file has OPENROUTER_API_KEY")
                        logger.error("  2. Verify API key is valid at https://openrouter.ai")
                        logger.error("  3. Try /diagnose endpoint for detailed diagnostics")
                        logger.error("="*70)
                        last_error = error_msg
                        return None, False  # Don't retry on auth error
                    
                    # Regular logging for other errors
                    logger.warning(f"{error_msg} (Model: {current_model})")
                    last_error = error_msg
                    
                    # Don't retry on 429 (rate limit) as it will fail repeatedly
                    if response.status_code == 429:
                        logger.error(f"Rate limited by OpenRouter, stopping retries")
                        break
                    
                    # Continue to next model for other errors
                    continue
            
            except requests.exceptions.Timeout:
                error_msg = f"OpenRouter API request timeout (Model: {current_model})"
                logger.warning(error_msg)
                last_error = error_msg
                continue
            
            except requests.exceptions.ConnectionError:
                error_msg = f"Connection error with OpenRouter API (Model: {current_model})"
                logger.warning(error_msg)
                last_error = error_msg
                continue
            
            except Exception as e:
                error_msg = f"Error with model {current_model}: {str(e)}"
                logger.warning(error_msg)
                last_error = error_msg
                continue
        
        # All models exhausted
        logger.error(f"All OpenRouter models failed. Last error: {last_error}")
        self._reset_model_index()
        return None, False
    
    
    @staticmethod
    def _format_sources(sources: List[Dict]) -> str:
        """Format sources for inclusion in AI prompt"""
        if not sources:
            return ""
        
        formatted = "Additional context from sources:\n"
        for source in sources:
            if source.get("source") == "University Knowledge":
                formatted += f"- {source.get('category', '')}: {source.get('content', '')}\n"
            else:
                formatted += f"- {source.get('title', '')}: {source.get('summary', '')}\n"
        
        return formatted


# Global instance
openrouter_service = OpenRouterService()
language_detector = LanguageDetector()
