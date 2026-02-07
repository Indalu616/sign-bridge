"""
Configuration endpoint for server-side settings
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
import os

router = APIRouter(prefix="/config", tags=["Configuration"])


class ConfigResponse(BaseModel):
    """Response model for configuration"""
    whisper_model: str = Field(..., description="Whisper model being used")
    coqui_server_url: str = Field(..., description="Coqui TTS server URL")
    tts_model: str = Field(..., description="TTS model name")
    api_version: str = Field(..., description="API version")
    features: dict = Field(..., description="Enabled features")
    
    class Config:
        json_schema_extra = {
            "example": {
                "whisper_model": "whisper-1",
                "coqui_server_url": "http://localhost:5002",
                "tts_model": "tts_models/en/ljspeech/tacotron2-DDC",
                "api_version": "1.0.0",
                "features": {
                    "speech_to_text": True,
                    "text_to_speech": True,
                    "sign_language": True,
                    "conversation_logging": True
                }
            }
        }


@router.get(
    "",
    response_model=ConfigResponse,
    summary="Get server configuration",
    description="Returns server-side configuration including models and enabled features"
)
async def get_config():
    """
    Get server configuration
    
    Returns information about:
    - Whisper model version
    - Coqui TTS server URL
    - TTS model name
    - API version
    - Enabled features
    """
    return ConfigResponse(
        whisper_model="whisper-1",
        coqui_server_url=os.getenv("COQUI_SERVER_URL", "http://localhost:5002"),
        tts_model="tts_models/en/ljspeech/tacotron2-DDC",  # Default model
        api_version="1.0.0",
        features={
            "speech_to_text": True,
            "text_to_speech": True,
            "sign_language": True,
            "conversation_logging": True,
            "dialogue_orchestration": True
        }
    )
