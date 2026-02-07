"""
SignAll SDK integration for sign language output
"""
import httpx
from typing import Optional, Dict
import os


class SignAllService:
    """Service for SignAll SDK integration"""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize SignAll service
        
        Args:
            api_key: SignAll API key (from environment if not provided)
            api_url: SignAll API URL (from environment if not provided)
        """
        self.api_key = api_key or os.getenv("SIGNALL_API_KEY")
        self.api_url = api_url or os.getenv("SIGNALL_API_URL", "https://api.signall.us")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def text_to_sign(
        self,
        text: str,
        language: str = "ASL"
    ) -> Dict[str, str]:
        """
        Convert text to sign language video/animation
        
        Args:
            text: Text to convert to sign language
            language: Sign language type (ASL, Arabic Sign Language, etc.)
            
        Returns:
            Dictionary with video_url and metadata
            
        Raises:
            Exception: If conversion fails
        """
        if not self.api_key:
            # Fallback: Return pre-recorded sign videos (for MVP)
            return await self._get_prerecorded_sign(text, language)
        
        # Make API request to SignAll
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "language": language,
            "format": "mp4"
        }
        
        try:
            response = await self.client.post(
                f"{self.api_url}/v1/text-to-sign",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "video_url": data.get("video_url"),
                "text": text,
                "language": language
            }
        
        except httpx.HTTPError as e:
            print(f"SignAll API error: {e}")
            # Fallback to pre-recorded signs
            return await self._get_prerecorded_sign(text, language)
    
    async def _get_prerecorded_sign(self, text: str, language: str) -> Dict[str, str]:
        """
        Fallback: Map text to pre-recorded sign videos
        
        Args:
            text: Text to map
            language: Sign language type
            
        Returns:
            Dictionary with video_url
        """
        # Simple mapping for common phrases (for MVP/demo)
        # In production, this would be a database lookup
        sign_library = {
            "hello": "https://cdn.example.com/signs/hello.mp4",
            "help": "https://cdn.example.com/signs/help.mp4",
            "water": "https://cdn.example.com/signs/water.mp4",
            "thank you": "https://cdn.example.com/signs/thank_you.mp4",
            "yes": "https://cdn.example.com/signs/yes.mp4",
            "no": "https://cdn.example.com/signs/no.mp4",
            "where is the hospital": "https://cdn.example.com/signs/where_hospital.mp4",
            "i need help": "https://cdn.example.com/signs/need_help.mp4",
        }
        
        # Normalize text for lookup
        normalized_text = text.lower().strip()
        video_url = sign_library.get(normalized_text, "https://cdn.example.com/signs/default.mp4")
        
        return {
            "video_url": video_url,
            "text": text,
            "language": language,
            "source": "prerecorded"
        }
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_signall_service: Optional[SignAllService] = None


def get_signall_service() -> SignAllService:
    """
    Get or create SignAllService singleton instance
    
    Returns:
        SignAllService instance
    """
    global _signall_service
    if _signall_service is None:
        _signall_service = SignAllService()
    return _signall_service
