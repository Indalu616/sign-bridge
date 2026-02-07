"""
Coqui TTS service integration (local self-hosted server)
"""
import httpx
from typing import Optional
import os


class CoquiTTSService:
    """Service for Coqui TTS local server integration"""
    
    def __init__(self, server_url: Optional[str] = None):
        """
        Initialize Coqui TTS client
        
        Args:
            server_url: Coqui TTS server URL (from environment if not provided)
        """
        self.server_url = server_url or os.getenv("COQUI_SERVER_URL", "http://localhost:5002")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def synthesize_speech(
        self,
        text: str,
        speaker_id: Optional[str] = None,
        language_id: Optional[str] = None,
        style_wav: Optional[str] = None
    ) -> bytes:
        """
        Convert text to speech using Coqui TTS server
        
        Args:
            text: Text to convert to speech
            speaker_id: Optional speaker ID for multi-speaker models
            language_id: Optional language ID for multi-lingual models
            style_wav: Optional path to reference audio for style transfer
            
        Returns:
            Audio content as bytes (WAV format)
            
        Raises:
            Exception: If synthesis fails or server is unreachable
        """
        try:
            # Prepare request payload
            payload = {
                "text": text
            }
            
            if speaker_id:
                payload["speaker_id"] = speaker_id
            
            if language_id:
                payload["language_id"] = language_id
            
            if style_wav:
                payload["style_wav"] = style_wav
            
            # Make request to Coqui TTS server
            response = await self.client.post(
                f"{self.server_url}/api/tts",
                json=payload
            )
            
            response.raise_for_status()
            
            # Return audio bytes
            return response.content
        
        except httpx.ConnectError:
            raise Exception(
                f"Cannot connect to Coqui TTS server at {self.server_url}. "
                "Make sure the server is running."
            )
        except httpx.HTTPStatusError as e:
            raise Exception(f"Coqui TTS server error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Coqui TTS synthesis failed: {str(e)}")
    
    async def get_server_info(self) -> dict:
        """
        Get information about the Coqui TTS server
        
        Returns:
            Server information including available models and speakers
            
        Raises:
            Exception: If server is unreachable
        """
        try:
            response = await self.client.get(f"{self.server_url}/api/tts/info")
            response.raise_for_status()
            return response.json()
        
        except httpx.ConnectError:
            raise Exception(
                f"Cannot connect to Coqui TTS server at {self.server_url}. "
                "Make sure the server is running."
            )
        except Exception as e:
            raise Exception(f"Failed to get server info: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check if Coqui TTS server is healthy
        
        Returns:
            True if server is reachable and healthy, False otherwise
        """
        try:
            response = await self.client.get(f"{self.server_url}/health", timeout=5.0)
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_coqui_service: Optional[CoquiTTSService] = None


def get_coqui_service() -> CoquiTTSService:
    """
    Get or create CoquiTTSService singleton instance
    
    Returns:
        CoquiTTSService instance
    """
    global _coqui_service
    if _coqui_service is None:
        _coqui_service = CoquiTTSService()
    return _coqui_service
