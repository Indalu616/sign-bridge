"""
Dialogue orchestration endpoint for end-to-end interactions
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from models.schemas import ErrorResponse
from services.whisper_stt import get_whisper_service
from services.coqui_tts import get_coqui_service
from fastapi.responses import Response
import io

router = APIRouter(prefix="/dialogue", tags=["Dialogue"])


class DialogueRequest(BaseModel):
    """Request model for dialogue interaction"""
    user_input: str = Field(..., description="User input text or audio reference")
    mode: Literal["speech", "text"] = Field(..., description="Input mode: 'speech' or 'text'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_input": "Can I pay my bill?",
                "mode": "speech"
            }
        }


class DialogueResponse(BaseModel):
    """Response model for dialogue interaction"""
    reply_text: str = Field(..., description="Text response")
    reply_audio_base64: Optional[str] = Field(None, description="Base64 encoded audio response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reply_text": "Yes, please provide your account number.",
                "reply_audio_base64": "UklGRiQAAABXQVZFZm10..."
            }
        }


@router.post(
    "",
    response_model=DialogueResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Orchestrate end-to-end dialogue",
    description="Handle complete user interaction with speech/text input and audio/text output"
)
async def dialogue_interaction(request: DialogueRequest):
    """
    Orchestrate a complete dialogue interaction
    
    - **user_input**: User's input (text or reference to audio)
    - **mode**: Input mode ('speech' or 'text')
    
    Returns text response and optional audio
    """
    try:
        # For now, this is a simple echo/response system
        # In production, this would integrate with a conversational AI
        
        # Generate a simple response based on input
        reply_text = f"I understand you said: '{request.user_input}'. How can I assist you further?"
        
        # Generate audio response using Coqui TTS
        coqui_service = get_coqui_service()
        audio_content = await coqui_service.synthesize_speech(text=reply_text)
        
        # Convert audio to base64 for JSON response
        import base64
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')
        
        return DialogueResponse(
            reply_text=reply_text,
            reply_audio_base64=audio_base64
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dialogue processing failed: {str(e)}"
        )
