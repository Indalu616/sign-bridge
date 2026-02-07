"""
Text-to-Sign API endpoints
"""
from fastapi import APIRouter, HTTPException
from models.schemas import TextToSignRequest, TextToSignResponse, ErrorResponse
from services.signall_sdk import get_signall_service

router = APIRouter(prefix="/translate-sign", tags=["Sign Language Output"])


@router.post(
    "",
    response_model=TextToSignResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Convert text to sign language",
    description="Send text and receive sign language video/animation URL"
)
async def text_to_sign(request: TextToSignRequest):
    """
    Convert text to sign language video/animation
    
    - **text**: Text to convert to sign language
    - **language**: Sign language type (ASL, Arabic Sign Language)
    
    Returns URL to sign language video or animation
    """
    try:
        # Get SignAll service
        signall_service = get_signall_service()
        
        # Convert text to sign
        result = await signall_service.text_to_sign(
            text=request.text,
            language=request.language
        )
        
        return TextToSignResponse(
            video_url=result["video_url"],
            text=request.text
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate sign language output: {str(e)}"
        )
