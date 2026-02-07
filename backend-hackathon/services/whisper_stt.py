"""
OpenAI Whisper Speech-to-Text service integration
"""
from openai import OpenAI
from typing import Optional, Tuple
import os
import io


class WhisperSTTService:
    """Service for OpenAI Whisper Speech-to-Text API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI Whisper client
        
        Args:
            api_key: OpenAI API key (from environment if not provided)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
    
    async def transcribe_audio(
        self,
        audio_content: bytes,
        filename: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Tuple[str, Optional[str]]:
        """
        Transcribe audio to text using OpenAI Whisper API
        
        Args:
            audio_content: Audio file content as bytes
            filename: Original filename (used to determine format)
            language: Optional language code (e.g., 'en', 'ar')
            prompt: Optional prompt to guide transcription
            
        Returns:
            Tuple of (transcript, detected_language)
            
        Raises:
            Exception: If transcription fails
        """
        try:
            # Create a file-like object from bytes
            audio_file = io.BytesIO(audio_content)
            audio_file.name = filename  # Whisper uses filename to detect format
            
            # Prepare transcription parameters
            transcribe_params = {
                "file": audio_file,
                "model": "whisper-1",
                "response_format": "verbose_json"  # Get detailed response with language
            }
            
            if language:
                transcribe_params["language"] = language
            
            if prompt:
                transcribe_params["prompt"] = prompt
            
            # Perform transcription
            response = self.client.audio.transcriptions.create(**transcribe_params)
            
            # Extract transcript and language
            transcript = response.text
            detected_language = getattr(response, 'language', None)
            
            return transcript, detected_language
        
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")
    
    async def translate_to_english(
        self,
        audio_content: bytes,
        filename: str
    ) -> str:
        """
        Translate audio to English text (Whisper's translation feature)
        
        Args:
            audio_content: Audio file content as bytes
            filename: Original filename
            
        Returns:
            English translation of the audio
            
        Raises:
            Exception: If translation fails
        """
        try:
            # Create a file-like object from bytes
            audio_file = io.BytesIO(audio_content)
            audio_file.name = filename
            
            # Use Whisper's translation endpoint
            response = self.client.audio.translations.create(
                file=audio_file,
                model="whisper-1"
            )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Whisper translation failed: {str(e)}")


# Singleton instance
_whisper_service: Optional[WhisperSTTService] = None


def get_whisper_service() -> WhisperSTTService:
    """
    Get or create WhisperSTTService singleton instance
    
    Returns:
        WhisperSTTService instance
    """
    global _whisper_service
    if _whisper_service is None:
        _whisper_service = WhisperSTTService()
    return _whisper_service
