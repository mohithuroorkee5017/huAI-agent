"""
Vision API Integration Service
Handles image analysis using OpenRouter vision models (GPT-4 Vision)
Supports: Image description, OCR, object detection, document reading
"""

import requests
import logging
import base64
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


class VisionService:
    """Handle image analysis via OpenRouter Vision API"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.vision_model = "openai/gpt-4o-mini"  # Vision-capable model
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = 60  # Vision tasks may take longer
        self.max_image_size = 20 * 1024 * 1024  # 20MB max
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    
    def validate_image_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate image file exists and is supported format
        
        Args:
            file_path: Path to image file
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            # Check file size
            file_size = path.stat().st_size
            if file_size > self.max_image_size:
                return False, f"File too large. Max size: {self.max_image_size // (1024*1024)}MB"
            
            # Check file extension
            if path.suffix.lower() not in self.supported_formats:
                return False, f"Unsupported format. Supported: {', '.join(self.supported_formats)}"
            
            return True, ""
        
        except Exception as e:
            logger.error(f"[VISION] File validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def encode_image_to_base64(self, file_path: str) -> Optional[str]:
        """
        Encode image file to base64 for API transmission
        
        Args:
            file_path: Path to image file
        
        Returns:
            Base64 encoded string or None if error
        """
        try:
            logger.info(f"[IMAGE] Encoding image: {file_path}")
            
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            logger.info(f"[IMAGE] ✓ Image encoded successfully ({len(base64_image)} chars)")
            return base64_image
        
        except Exception as e:
            logger.error(f"[IMAGE] Encoding error: {str(e)}")
            return None
    
    def get_image_media_type(self, file_path: str) -> str:
        """
        Get MIME type for image file
        
        Args:
            file_path: Path to image file
        
        Returns:
            MIME type string
        """
        extension = Path(file_path).suffix.lower()
        
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp'
        }
        
        return mime_types.get(extension, 'image/jpeg')
    
    def analyze_image(
        self,
        image_path: str,
        user_prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[List[str]], bool]:
        """
        Analyze image using vision model
        
        Args:
            image_path: Path to image file
            user_prompt: Optional custom prompt for analysis
        
        Returns:
            Tuple of (analysis_text, objects_list, success_flag)
        """
        try:
            # Validate image file
            is_valid, error_msg = self.validate_image_file(image_path)
            if not is_valid:
                logger.error(f"[VISION] Validation failed: {error_msg}")
                return None, [], False
            
            # Encode image to base64
            base64_image = self.encode_image_to_base64(image_path)
            if not base64_image:
                logger.error("[VISION] Failed to encode image")
                return None, [], False
            
            # Determine media type
            media_type = self.get_image_media_type(image_path)
            logger.info(f"[IMAGE] Media type: {media_type}")
            
            # Prepare default prompt if not provided
            if not user_prompt:
                user_prompt = """Analyze this image and provide:
1. **Description**: What is shown in the image?
2. **Objects**: List main objects/elements detected
3. **Text**: Any visible text (OCR)
4. **Type**: Image type (screenshot, photo, document, chart, etc.)
5. **Analysis**: Key observations and insights

Format response clearly with these sections."""
            
            # Build request payload
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.vision_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image
                                }
                            },
                            {
                                "type": "text",
                                "text": user_prompt
                            }
                        ]
                    }
                ],
                "max_tokens": 1500,
                "temperature": 0.7
            }
            
            logger.info(f"[VISION] Sending request to {self.vision_model}")
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            logger.info(f"[VISION] Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"[VISION] API error: {response.text}")
                return None, [], False
            
            # Parse response
            data = response.json()
            
            if 'choices' not in data or len(data['choices']) == 0:
                logger.error("[VISION] No response from API")
                return None, [], False
            
            analysis_text = data['choices'][0]['message']['content'].strip()
            logger.info(f"[VISION] ✓ Analysis received ({len(analysis_text)} chars)")
            
            # Extract objects from analysis (simple keyword extraction)
            objects = extract_objects(analysis_text)
            
            return analysis_text, objects, True
        
        except requests.exceptions.Timeout:
            logger.error(f"[VISION] Request timeout ({self.timeout}s)")
            return None, [], False
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[VISION] Connection error: {str(e)}")
            return None, [], False
        
        except Exception as e:
            logger.error(f"[VISION] Unexpected error: {str(e)}")
            import traceback
            logger.error(f"[VISION] Traceback: {traceback.format_exc()}")
            return None, [], False


def extract_objects(analysis_text: str) -> List[str]:
    """
    Extract detected objects from analysis text
    
    Args:
        analysis_text: Analysis response from vision model
    
    Returns:
        List of detected objects
    """
    try:
        objects = []
        
        # Common indicators of object lists
        keywords = ['objects', 'detected', 'elements', 'items', 'contains', 'shows']
        
        for line in analysis_text.split('\n'):
            # Look for bullet points or numbered lists
            if any(line.strip().startswith(prefix) for prefix in ['•', '-', '*', '1', '2', '3']):
                # Clean up the line
                cleaned = line.strip().lstrip('•-*0123456789. )').strip()
                if cleaned and len(cleaned) > 2:
                    objects.append(cleaned)
        
        logger.info(f"[OCR] Extracted {len(objects)} objects from analysis")
        return objects[:20]  # Limit to 20 objects
    
    except Exception as e:
        logger.warning(f"[OCR] Object extraction error: {str(e)}")
        return []


# Create service instance
vision_service = VisionService()

__all__ = ["vision_service", "VisionService"]
