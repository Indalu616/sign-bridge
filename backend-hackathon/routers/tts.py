"""
Text-to-Speech API endpoints using Coqui TTS
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from models.schemas import TextToSpeechRequest, ErrorResponse
from services.coqui_tts import get_coqui_service

router = APIRouter(prefix="/tts", tags=["Speech Synthesis"])


@router.post(
    "",
    response_class=Response,
    responses={
        200: {
            "content": {"audio/wav": {}},
            "description": "Audio file (WAV format)"
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Convert text to speech",
    description="Send text and receive synthesized audio from local Coqui TTS server"
)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech using Coqui TTS (local server)
    
    - **text**: Text to convert to speech
    - **language**: Language code (e.g., en-US, ar-SA) - currently not used by basic Coqui setup
    
    Returns audio file in WAV format
    """
    try:
        # Get Coqui TTS service
        coqui_service = get_coqui_service()
        
        # Synthesize speech
        audio_content = await coqui_service.synthesize_speech(
            text=request.text
        )
        
        # Return audio as response
        return Response(
            content=audio_content,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f'attachment; filename="speech.wav"'
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to synthesize speech: {str(e)}"
        )
