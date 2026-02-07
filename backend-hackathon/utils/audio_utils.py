"""
Utility functions for audio processing
"""
import os
from typing import Optional
from fastapi import UploadFile, HTTPException


ALLOWED_AUDIO_FORMATS = {".wav", ".mp3", ".m4a", ".ogg", ".flac"}
MAX_AUDIO_SIZE_MB = 10


async def validate_audio_file(file: UploadFile) -> bytes:
    """
    Validate and read uploaded audio file
    
    Args:
        file: Uploaded audio file
        
    Returns:
        Audio file content as bytes
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio format. Allowed formats: {', '.join(ALLOWED_AUDIO_FORMATS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    file_size_mb = len(content) / (1024 * 1024)
    if file_size_mb > MAX_AUDIO_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_AUDIO_SIZE_MB}MB"
        )
    
    # Reset file pointer for potential re-reading
    await file.seek(0)
    
    return content


def get_audio_format(filename: str) -> str:
    """
    Get audio format from filename
    
    Args:
        filename: Name of the audio file
        
    Returns:
        Audio format (e.g., 'wav', 'mp3')
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext.lstrip('.')


def convert_to_linear16(audio_content: bytes, source_format: str) -> Optional[bytes]:
    """
    Convert audio to LINEAR16 format for Google Speech API
    (Placeholder - implement with pydub if needed)
    
    Args:
        audio_content: Raw audio bytes
        source_format: Source audio format
        
    Returns:
        Converted audio bytes or None if conversion not needed
    """
    # For now, return as-is. Implement conversion with pydub if needed:
    # from pydub import AudioSegment
    # audio = AudioSegment.from_file(io.BytesIO(audio_content), format=source_format)
    # audio = audio.set_frame_rate(16000).set_channels(1)
    # return audio.raw_data
    
    return None


async def save_temp_audio(content: bytes, filename: str, temp_dir: str = "temp") -> str:
    """
    Save audio content to temporary file
    
    Args:
        content: Audio file content
        filename: Original filename
        temp_dir: Temporary directory path
        
    Returns:
        Path to saved temporary file
    """
    import aiofiles
    
    # Create temp directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate unique filename
    import uuid
    unique_filename = f"{uuid.uuid4()}_{filename}"
    temp_path = os.path.join(temp_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(temp_path, 'wb') as f:
        await f.write(content)
    
    return temp_path


def cleanup_temp_file(file_path: str) -> None:
    """
    Remove temporary file
    
    Args:
        file_path: Path to temporary file
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Failed to cleanup temp file {file_path}: {e}")
