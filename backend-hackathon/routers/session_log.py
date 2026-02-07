"""
Conversation logging API endpoints
"""
from fastapi import APIRouter, HTTPException
from models.schemas import ConversationLogRequest, ConversationLogResponse, ErrorResponse
from typing import List
import json
import os
from datetime import datetime
import uuid

router = APIRouter(prefix="/log", tags=["Logging"])

# Simple file-based storage for MVP (replace with database in production)
LOGS_DIR = "conversation_logs"


@router.post(
    "",
    response_model=ConversationLogResponse,
    responses={
        500: {"model": ErrorResponse}
    },
    summary="Log conversation interaction",
    description="Save conversation data for analytics and learning"
)
async def log_conversation(request: ConversationLogRequest):
    """
    Log a conversation interaction
    
    - **sign_input**: Original sign language input (if detected)
    - **translated_text**: Translated/transcribed text
    - **response_speech**: Response from other party
    - **timestamp**: Conversation timestamp
    - **session_id**: Unique session identifier
    
    Returns confirmation of saved log
    """
    try:
        # Create logs directory if it doesn't exist
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Generate unique log ID
        log_id = str(uuid.uuid4())
        
        # Prepare log entry
        log_entry = {
            "log_id": log_id,
            "sign_input": request.sign_input,
            "translated_text": request.translated_text,
            "response_speech": request.response_speech,
            "timestamp": request.timestamp.isoformat(),
            "session_id": request.session_id
        }
        
        # Save to file (in production, use database)
        log_filename = f"{request.session_id}_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        log_path = os.path.join(LOGS_DIR, log_filename)
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return ConversationLogResponse(
            status="saved",
            log_id=log_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log conversation: {str(e)}"
        )


@router.get(
    "/{session_id}",
    summary="Get conversation history",
    description="Retrieve conversation logs for a session"
)
async def get_conversation_history(session_id: str):
    """
    Retrieve conversation history for a session
    
    - **session_id**: Session identifier
    
    Returns list of conversation logs
    """
    try:
        # Find log files for this session
        logs = []
        
        if not os.path.exists(LOGS_DIR):
            return {"session_id": session_id, "logs": []}
        
        for filename in os.listdir(LOGS_DIR):
            if filename.startswith(session_id):
                log_path = os.path.join(LOGS_DIR, filename)
                with open(log_path, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
        
        return {
            "session_id": session_id,
            "logs": logs,
            "count": len(logs)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )
