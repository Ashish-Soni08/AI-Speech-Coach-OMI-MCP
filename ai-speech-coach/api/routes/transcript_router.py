from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import os

from models.database import get_db
from models.schemas import TranscriptRequest, SpeechAnalysisResponse
from analyzer.analyzer_service import SpeechAnalyzerService
from api.services.database_service import DatabaseService

# Initialize router
router = APIRouter()

# Initialize services
analyzer_service = SpeechAnalyzerService()
db_service = DatabaseService()

# Configure logging
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=SpeechAnalysisResponse)
async def analyze_transcript(
    request: TranscriptRequest,
    session: AsyncSession = Depends(get_db),
    store_results: bool = Query(True, description="Whether to store analysis results in the database"),
    omi_api_key: str = Header(None, alias="X-OMI-API-Key")
):
    """
    Analyze transcript segments and provide coaching feedback.
    
    This endpoint receives transcript segments from OMI devices,
    analyzes them, and returns coaching feedback.
    
    - Detects filler words
    - Measures speaking pace
    - Analyzes vocabulary diversity
    - Provides personalized improvement suggestions
    """
    # Validate OMI API key if in production
    if os.getenv("ENVIRONMENT") == "production":
        expected_api_key = os.getenv("OMI_API_KEY")
        if not expected_api_key or omi_api_key != expected_api_key:
            raise HTTPException(status_code=403, detail="Invalid or missing API key")
            
    logger.info(f"Received transcript analysis request for session {request.session_id}")
    
    try:
        # Convert transcript request to internal format
        segments = []
        for segment in request.segments:
            segments.append({
                "text_content": segment.text,
                "speaker_identification": segment.speaker,
                "is_user_speaking": segment.is_user,
                "start_time": segment.start,
                "end_time": segment.end
            })
        
        # Get analysis from the analyzer service
        analysis_result = await analyzer_service.analyze_transcript(segments)
        
        # If storing is enabled, save results to database
        if store_results:
            try:
                # Store user if they don't exist
                user = await db_service.get_or_create_user(
                    session,
                    user_id=request.user_id,
                    username=f"User-{request.user_id[:8]}",  # Generate temporary username
                    device_id=f"OMI-{request.user_id[:8]}"   # Generate temporary device ID
                )
                
                # Store conversation and segments
                conversation = await db_service.store_conversation(
                    session,
                    user_id=user.user_id,
                    session_id=request.session_id,
                    segments=segments
                )
                
                # Store analysis results
                stored_analysis = await db_service.store_analysis_results(
                    session,
                    user_id=user.user_id,
                    metrics=analysis_result["metrics"],
                    suggestions=analysis_result["suggestions"]
                )
                
                analysis_id = stored_analysis.analysis_id
                logger.info(f"Stored analysis results with ID {analysis_id}")
            
            except Exception as e:
                logger.error(f"Error storing analysis results: {str(e)}")
                # Continue even if storage fails
        else:
            analysis_id = None
        
        # Prepare response
        response = SpeechAnalysisResponse(
            analysis_id=analysis_id,
            session_id=request.session_id,
            user_id=request.user_id,
            timestamp=datetime.utcnow(),
            metrics=analysis_result["metrics"],
            suggestions=analysis_result["suggestions"]
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error analyzing transcript: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing transcript: {str(e)}")


@router.get("/history/{user_id}", response_model=List[Dict[str, Any]])
async def get_user_history(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db)
):
    """
    Get historical speech analysis results for a user.
    
    Returns the most recent analysis results for the specified user,
    including metrics and suggestions for improvement.
    """
    logger.info(f"Retrieving speech history for user {user_id}")
    
    try:
        history = await db_service.get_user_analysis_history(
            session,
            user_id=user_id,
            limit=limit
        )
        
        return history
    
    except Exception as e:
        logger.error(f"Error retrieving user history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user history: {str(e)}")


@router.get("/statistics/{user_id}", response_model=Dict[str, Any])
async def get_user_statistics(
    user_id: str,
    days: int = Query(30, ge=1, le=365),
    session: AsyncSession = Depends(get_db)
):
    """
    Get aggregated speech statistics for a user over a time period.
    
    Returns metrics such as average filler word usage, speaking pace,
    vocabulary diversity, and overall progress over time.
    """
    logger.info(f"Retrieving speech statistics for user {user_id} over {days} days")
    
    try:
        statistics = await db_service.get_user_statistics(
            session,
            user_id=user_id,
            days=days
        )
        
        return statistics
    
    except Exception as e:
        logger.error(f"Error retrieving user statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user statistics: {str(e)}")