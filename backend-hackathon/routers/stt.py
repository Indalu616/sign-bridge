"""
Speech-to-Text API endpoints using OpenAI Whisper
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from models.schemas import SpeechToTextResponse, ErrorResponse
from services.whisper_stt import get_whisper_service
from utils.audio_utils import validate_audio_file

router = APIRouter(prefix="/stt", tags=["Speech Recognition"])


@router.post(
    "",
    response_model=SpeechToTextResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Convert speech to text",
    description="Upload an audio file and receive the transcribed text"
)
async def speech_to_text(
    audio_file: UploadFile = File(..., description="Audio file (.wav, .mp3, .m4a, .ogg, .flac)"),
    language: str = Query(None, description="Optional language code (e.g., 'en', 'ar'). Auto-detected if not provided.")
):
    """
    Convert speech audio to text using OpenAI Whisper API
    
    - **audio_file**: Audio file to transcribe
    - **language**: Optional language code (auto-detected if not provided)
    
    Returns the transcribed text and detected language
    """
    try:
        # Validate audio file
        audio_content = await validate_audio_file(audio_file)
        
        # Get Whisper service
        whisper_service = get_whisper_service()
        
        # Transcribe audio (Whisper auto-detects format from filename)
        transcript, detected_language = await whisper_service.transcribe_audio(
            audio_content=audio_content,
            filename=audio_file.filename,
            language=language
        )
        
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in audio file"
            )
        
        return SpeechToTextResponse(
            transcript=transcript,
            confidence=None  # Whisper doesn't provide confidence scores
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to transcribe audio: {str(e)}"
        )
