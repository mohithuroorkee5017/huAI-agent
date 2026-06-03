"""
Configuration module for HU Voice AI API
Handles all environment variables and application settings
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the directory where config.py is located
CONFIG_DIR = Path(__file__).parent
ENV_FILE = CONFIG_DIR / ".env"

logger.info(f"Configuration file location: {CONFIG_DIR}")
logger.info(f".env file path: {ENV_FILE}")
logger.info(f".env file exists: {ENV_FILE.exists()}")


class Settings(BaseSettings):
    """Application Settings"""
    
    model_config = ConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )
    
    # Application
    APP_NAME: str = "HU Voice AI API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # API Keys
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_FALLBACK_MODELS: List[str] = [
        "openai/gpt-4o-mini",
        "google/gemini-2.5-flash",
        "deepseek/deepseek-r1",
        "openai/gpt-3.5-turbo"
    ]
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY: int = 20
    CONVERSATION_TIMEOUT: int = 3600  # 1 hour in seconds
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Redis Settings (Optional)
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    # Search Settings
    WIKIPEDIA_TIMEOUT: int = 5
    DUCKDUCKGO_TIMEOUT: int = 5
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]


def _load_settings():
    """Load settings and verify critical configuration"""
    settings = Settings()
    
    # Log configuration loading (excluding sensitive data)
    print("\n" + "="*70)
    print("🔧 HU VOICE AI - CONFIGURATION DIAGNOSTIC")
    print("="*70)
    print(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    print(f"Rate Limiting: {'✓ Enabled' if settings.RATE_LIMIT_ENABLED else '✗ Disabled'}")
    print(f"Config Directory: {CONFIG_DIR}")
    print(f".env File: {ENV_FILE}")
    print(f".env Exists: {'✓ YES' if ENV_FILE.exists() else '✗ NO'}")
    
    # Check OpenRouter configuration
    print("\n" + "-"*70)
    print("🔐 OPENROUTER API STATUS:")
    if settings.OPENROUTER_API_KEY:
        # Check if it's the placeholder value
        if settings.OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
            print(f"  API Key Status: ✗ PLACEHOLDER - Not actually configured")
            print(f"    → Set actual API key in {ENV_FILE}")
        elif settings.OPENROUTER_API_KEY.startswith("sk-or-v1-"):
            # Show masked API key for debugging (first 20 and last 4 chars)
            masked_key = settings.OPENROUTER_API_KEY[:20] + "..." + settings.OPENROUTER_API_KEY[-4:]
            print(f"  API Key Status: ✓ LOADED ({masked_key})")
        else:
            print(f"  API Key Status: ⚠ INVALID FORMAT - Unexpected key format")
            print(f"    → Expected format: sk-or-v1-XXXXXXXXXXXXX")
            print(f"    → Actual: {settings.OPENROUTER_API_KEY[:30]}...")
    else:
        print(f"  API Key Status: ✗ MISSING - Check OPENROUTER_API_KEY environment variable")
        print(f"    → Set via: .env file, OS environment, or Docker env")
    
    print(f"  Primary Model: {settings.OPENROUTER_MODEL}")
    print(f"  Fallback Models: {len(settings.OPENROUTER_FALLBACK_MODELS)} configured")
    print("-"*70 + "\n")
    
    return settings


# Initialize settings with diagnostics
settings = _load_settings()
