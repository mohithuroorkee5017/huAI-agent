"""
Conversation Memory Management Service
Maintains conversation history for context-aware responses
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import OrderedDict
from config import settings
import logging

logger = logging.getLogger(__name__)


class Message:
    """Represents a single message in conversation"""
    
    def __init__(self, role: str, content: str, language: str = "en"):
        self.role = role  # "user" or "assistant"
        self.content = content
        self.language = language
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            "role": self.role,
            "content": self.content,
            "language": self.language,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationMemory:
    """Manages conversation history with memory limits"""
    
    def __init__(self):
        self.conversations: Dict[str, List[Message]] = OrderedDict()
        self.max_history = settings.MAX_CONVERSATION_HISTORY
        self.timeout = settings.CONVERSATION_TIMEOUT
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        language: str = "en"
    ) -> None:
        """Add a message to conversation history"""
        try:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            message = Message(role=role, content=content, language=language)
            self.conversations[conversation_id].append(message)
            
            # Keep only last N messages
            if len(self.conversations[conversation_id]) > self.max_history:
                self.conversations[conversation_id] = \
                    self.conversations[conversation_id][-self.max_history:]
            
            logger.info(
                f"Message added to conversation {conversation_id} by {role}"
            )
        except Exception as e:
            logger.error(f"Error adding message to memory: {str(e)}")
    
    def get_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history for OpenRouter format"""
        if conversation_id not in self.conversations:
            return []
        
        messages = self.conversations[conversation_id]
        return [msg.to_dict() for msg in messages]
    
    def get_recent_context(
        self,
        conversation_id: str,
        limit: int = 5
    ) -> str:
        """Get recent conversation context as string"""
        if conversation_id not in self.conversations:
            return ""
        
        messages = self.conversations[conversation_id][-limit:]
        context = "\n".join(
            [f"{msg.role.upper()}: {msg.content}" for msg in messages]
        )
        return context
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Conversation {conversation_id} cleared")
    
    def get_all_conversations(self) -> Dict[str, List[Dict]]:
        """Get all conversations (for debugging)"""
        return {
            conv_id: [msg.to_dict() for msg in messages]
            for conv_id, messages in self.conversations.items()
        }
    
    def cleanup_old_conversations(self) -> None:
        """Remove conversations that have exceeded timeout"""
        try:
            now = datetime.now()
            timeout_delta = timedelta(seconds=self.timeout)
            
            expired_ids = []
            for conv_id, messages in self.conversations.items():
                if messages:
                    last_message_time = messages[-1].timestamp
                    if now - last_message_time > timeout_delta:
                        expired_ids.append(conv_id)
            
            for conv_id in expired_ids:
                del self.conversations[conv_id]
                logger.info(f"Expired conversation {conv_id} removed")
        except Exception as e:
            logger.error(f"Error during conversation cleanup: {str(e)}")


# Global memory instance
memory = ConversationMemory()
