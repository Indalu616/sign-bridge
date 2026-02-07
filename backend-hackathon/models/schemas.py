"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech conversion"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    language: str = Field(default="en-US", description="Language code (e.g., en-US, ar-SA)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Thank you for helping me.",
                "language": "en-US"
            }
        }


class SpeechToTextResponse(BaseModel):
    """Response model for speech-to-text conversion"""
    transcript: str = Field(..., description="Transcribed text from audio")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "Hello, how can I help you?",
                "confidence": 0.95
            }
        }


class TextToSignRequest(BaseModel):
    """Request model for text-to-sign conversion"""
    text: str = Field(..., min_length=1, max_length=500, description="Text to convert to sign language")
    language: str = Field(default="ASL", description="Sign language type (ASL, Arabic Sign Language)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Where is the hospital?",
                "language": "ASL"
            }
        }


class TextToSignResponse(BaseModel):
    """Response model for text-to-sign conversion"""
    video_url: str = Field(..., description="URL to sign language video/animation")
    text: str = Field(..., description="Original text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_url": "https://cdn.example.com/signs/where_is_the_hospital.mp4",
                "text": "Where is the hospital?"
            }
        }


class ConversationLogRequest(BaseModel):
    """Request model for logging conversations"""
    sign_input: Optional[str] = Field(None, description="Original sign language input (if detected)")
    translated_text: str = Field(..., description="Translated/transcribed text")
    response_speech: Optional[str] = Field(None, description="Response from other party")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Conversation timestamp")
    session_id: str = Field(..., description="Unique session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sign_input": "I need water",
                "translated_text": "I need water",
                "response_speech": "Coming right up!",
                "timestamp": "2024-02-07T16:22:10Z",
                "session_id": "abc123"
            }
        }


class ConversationLogResponse(BaseModel):
    """Response model for conversation logging"""
    status: str = Field(..., description="Status of the operation")
    log_id: Optional[str] = Field(None, description="ID of the saved log entry")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "saved",
                "log_id": "log_12345"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Server status")
    uptime: Optional[str] = Field(None, description="Server uptime")
    version: str = Field(default="1.0.0", description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "uptime": "20h",
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid audio format",
                "detail": "Only .wav and .mp3 files are supported"
            }
        }
