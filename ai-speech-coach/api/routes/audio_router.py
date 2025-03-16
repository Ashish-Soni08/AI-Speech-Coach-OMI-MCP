from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
import logging
import aiofiles
import os
from datetime import datetime
import uuid

from models.database import get_db
from api.services.database_service import DatabaseService
from api.services.transcription_service import TranscriptionService

# Initialize router
router = APIRouter()

# Initialize services
db_service = DatabaseService()
transcription_service = TranscriptionService()

# Configure logging
logger = logging.getLogger(__name__)

# Storage directory for audio files
AUDIO_STORAGE_DIR = os.environ.get("AUDIO_STORAGE_DIR", "/tmp/speech_coach/audio")
os.makedirs(AUDIO_STORAGE_DIR, exist_ok=True)


@router.post("/stream", response_model=Dict[str, Any])
async def process_audio_stream(
    audio_data: bytes = File(...),
    user_id: str = Form(...),
    session_id: Optional[str] = Form(None),
    sample_rate: int = Form(16000),
    session: AsyncSession = Depends(get_db)
):
    """
    Process streaming audio from an OMI device.
    
    This endpoint receives audio data chunks from OMI devices,
    transcribes them, and queues them for later analysis.
    
    The audio is temporarily stored and processed at the end of the day
    for comprehensive speech analysis.
    """
    logger.info(f"Received audio stream from user {user_id}")
    
    # Generate session ID if not provided
    if not session_id:
        session_id = f"audio-{uuid.uuid4()}"
    
    try:
        # Save audio chunk to temporary storage
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{session_id}_{timestamp}.wav"
        file_path = os.path.join(AUDIO_STORAGE_DIR, filename)
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(audio_data)
        
        logger.info(f"Saved audio chunk to {file_path}")
        
        # Record audio chunk in database for later processing
        await db_service.record_audio_chunk(
            session,
            user_id=user_id,
            session_id=session_id,
            file_path=file_path,
            sample_rate=sample_rate,
            duration=len(audio_data) / (sample_rate * 2)  # Approximate duration in seconds
        )
        
        return {
            "status": "success",
            "message": "Audio chunk received and queued for processing",
            "session_id": session_id
        }
    
    except Exception as e:
        logger.error(f"Error processing audio stream: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio stream: {str(e)}")


@router.post("/upload", response_model=Dict[str, Any])
async def upload_audio_file(
    audio_file: UploadFile = File(...),
    user_id: str = Form(...),
    analyze_immediately: bool = Form(False),
    session: AsyncSession = Depends(get_db)
):
    """
    Upload an audio recording for analysis.
    
    This endpoint allows uploading complete audio files for speech analysis.
    The file is stored and can be analyzed immediately or queued for
    end-of-day processing.
    """
    logger.info(f"Received audio file upload from user {user_id}")
    
    try:
        # Generate a unique session ID for this upload
        session_id = f"upload-{uuid.uuid4()}"
        
        # Save audio file
        file_extension = os.path.splitext(audio_file.filename)[1]
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{session_id}_{timestamp}{file_extension}"
        file_path = os.path.join(AUDIO_STORAGE_DIR, filename)
        
        # Read and write the file
        content = await audio_file.read()
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        
        logger.info(f"Saved audio file to {file_path}")
        
        # Record in database
        await db_service.record_audio_upload(
            session,
            user_id=user_id,
            session_id=session_id,
            file_path=file_path,
            filename=audio_file.filename
        )
        
        # If immediate analysis is requested
        analysis_result = None
        if analyze_immediately:
            # Transcribe the audio
            transcription = await transcription_service.transcribe_audio(file_path)
            
            # Convert transcription to segments format
            segments = [
                {
                    "text_content": segment["text"],
                    "speaker_identification": "USER",
                    "is_user_speaking": True,
                    "start_time": segment["start"],
                    "end_time": segment["end"]
                }
                for segment in transcription["segments"]
            ]
            
            # Store the transcription
            await db_service.store_transcription(
                session,
                user_id=user_id,
                session_id=session_id,
                segments=segments
            )
            
            # Trigger analysis (simplified for now)
            logger.info("Immediate analysis not yet implemented")
            analysis_result = {
                "status": "pending",
                "message": "Analysis is being processed"
            }
        
        return {
            "status": "success",
            "message": "Audio file uploaded successfully",
            "session_id": session_id,
            "file_path": file_path,
            "analysis": analysis_result
        }
    
    except Exception as e:
        logger.error(f"Error uploading audio file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading audio file: {str(e)}")


@router.get("/status/{session_id}", response_model=Dict[str, Any])
async def get_audio_processing_status(
    session_id: str,
    session: AsyncSession = Depends(get_db)
):
    """
    Check the status of audio processing for a session.
    
    Returns the current status of audio processing, transcription,
    and analysis for the specified session.
    """
    logger.info(f"Checking audio processing status for session {session_id}")
    
    try:
        status = await db_service.get_audio_processing_status(
            session,
            session_id=session_id
        )
        
        return status
    
    except Exception as e:
        logger.error(f"Error retrieving audio processing status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving audio processing status: {str(e)}")