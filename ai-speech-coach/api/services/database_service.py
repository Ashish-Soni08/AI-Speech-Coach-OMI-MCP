from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, desc
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, date, timedelta
import json

from models.database import User, Conversation, SpeechSegment, AnalysisResult, ImprovementSuggestion

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service for database operations related to speech analysis.
    """
    
    async def get_or_create_user(
        self, 
        session: AsyncSession, 
        user_id: str, 
        username: str, 
        device_id: str
    ) -> User:
        """
        Get a user by ID or create if not exists.
        
        Args:
            session: Database session
            user_id: User ID (could be from OMI device)
            username: Username
            device_id: Device ID
            
        Returns:
            User object
        """
        # Try to find existing user
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalars().first()
        
        if not user:
            # Create new user
            user = User(
                username=username,
                email=f"{username}@example.com",  # Placeholder email
                device_id=device_id,
                settings={}
            )
            session.add(user)
            await session.commit()
            logger.info(f"Created new user: {username}")
        
        return user
    
    async def store_conversation(
        self, 
        session: AsyncSession, 
        user_id: int, 
        session_id: str, 
        segments: List[Dict]
    ) -> Conversation:
        """
        Store a conversation with speech segments.
        
        Args:
            session: Database session
            user_id: User ID
            session_id: Session ID
            segments: List of speech segments
            
        Returns:
            Conversation object
        """
        # Calculate conversation timestamps
        if segments:
            start_times = [s.get("start_time") for s in segments if s.get("start_time")]
            end_times = [s.get("end_time") for s in segments if s.get("end_time")]
            
            if start_times and end_times:
                start_timestamp = min(start_times)
                end_timestamp = max(end_times)
                
                if isinstance(start_timestamp, float):
                    # Convert to datetime if timestamps are floats
                    now = datetime.utcnow()
                    base_time = datetime(now.year, now.month, now.day)
                    start_timestamp = base_time + timedelta(seconds=start_timestamp)
                    end_timestamp = base_time + timedelta(seconds=end_timestamp)
            else:
                start_timestamp = datetime.utcnow()
                end_timestamp = datetime.utcnow()
        else:
            start_timestamp = datetime.utcnow()
            end_timestamp = datetime.utcnow()
        
        # Create conversation record
        conversation = Conversation(
            user_id=user_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            conversation_context=f"Session: {session_id}",
            participants_count=len(set([s.get("speaker_identification") for s in segments if s.get("speaker_identification")])),
            total_duration_seconds=(end_timestamp - start_timestamp).total_seconds()
        )
        session.add(conversation)
        await session.flush()  # Flush to get the ID
        
        # Store speech segments
        for segment in segments:
            # Extract segment data
            text_content = segment.get("text_content", "")
            speaker = segment.get("speaker_identification", "UNKNOWN")
            is_user = segment.get("is_user_speaking", False)
            
            # Handle timestamps
            start_time = segment.get("start_time")
            end_time = segment.get("end_time")
            
            if isinstance(start_time, float) and isinstance(end_time, float):
                # Convert to datetime if timestamps are floats
                now = datetime.utcnow()
                base_time = datetime(now.year, now.month, now.day)
                start_time = base_time + timedelta(seconds=start_time)
                end_time = base_time + timedelta(seconds=end_time)
            
            # Calculate duration and word count
            duration = (end_time - start_time).total_seconds()
            word_count = len(text_content.split())
            
            # Create segment record
            speech_segment = SpeechSegment(
                conversation_id=conversation.conversation_id,
                user_id=user_id,
                start_time=start_time,
                end_time=end_time,
                text_content=text_content,
                is_user_speaking=is_user,
                speaker_identification=speaker,
                duration_seconds=duration,
                word_count=word_count
            )
            session.add(speech_segment)
        
        await session.commit()
        logger.info(f"Stored conversation with {len(segments)} segments for user {user_id}")
        
        return conversation
    
    async def store_analysis_results(
        self, 
        session: AsyncSession, 
        user_id: int, 
        metrics: Dict, 
        suggestions: List[Dict]
    ) -> AnalysisResult:
        """
        Store speech analysis results.
        
        Args:
            session: Database session
            user_id: User ID
            metrics: Analysis metrics
            suggestions: Improvement suggestions
            
        Returns:
            AnalysisResult object
        """
        # Create analysis result record
        analysis_result = AnalysisResult(
            user_id=user_id,
            date=date.today(),
            total_speaking_time_seconds=metrics.get("speaking_time_seconds", 0),
            total_conversations=1,  # For now, just count this as one conversation
            filler_word_count=metrics.get("total_filler_count", 0),
            filler_word_percentage=metrics.get("filler_percentage", 0),
            avg_words_per_minute=metrics.get("words_per_minute", 0),
            pace_variability=metrics.get("pace_variability", 0),
            vocabulary_diversity_score=metrics.get("vocabulary_diversity", 0),
            clarity_score=metrics.get("clarity_score", 0),
            confidence_score=metrics.get("confidence_score", 0),
            overall_rating=metrics.get("confidence_score", 0) * 0.5 + metrics.get("clarity_score", 0) * 0.5
        )
        session.add(analysis_result)
        await session.flush()  # Flush to get the ID
        
        # Store improvement suggestions
        for suggestion in suggestions:
            suggestion_record = ImprovementSuggestion(
                analysis_id=analysis_result.analysis_id,
                segment_id=None,  # For now, we don't link to specific segments
                suggestion_type=suggestion.get("suggestion_type", "general"),
                suggestion_text=suggestion.get("suggestion_text", ""),
                priority_level=suggestion.get("priority_level", 3),
                example_text=suggestion.get("example_text"),
                improved_example=suggestion.get("improved_example")
            )
            session.add(suggestion_record)
        
        await session.commit()
        logger.info(f"Stored analysis results with {len(suggestions)} suggestions for user {user_id}")
        
        return analysis_result
    
    async def get_user_analysis_history(
        self, 
        session: AsyncSession, 
        user_id: str, 
        limit: int = 10
    ) -> List[Dict]:
        """
        Get historical analysis results for a user.
        
        Args:
            session: Database session
            user_id: User ID
            limit: Maximum number of results to return
            
        Returns:
            List of analysis results with suggestions
        """
        # Find user record
        user_query = select(User).where(User.username.like(f"%{user_id}%"))
        user_result = await session.execute(user_query)
        user = user_result.scalars().first()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            return []
        
        # Query analysis results
        query = (
            select(AnalysisResult)
            .where(AnalysisResult.user_id == user.user_id)
            .order_by(desc(AnalysisResult.date))
            .limit(limit)
        )
        result = await session.execute(query)
        analyses = result.scalars().all()
        
        # Build response
        history = []
        for analysis in analyses:
            # Get suggestions for this analysis
            suggestion_query = select(ImprovementSuggestion).where(
                ImprovementSuggestion.analysis_id == analysis.analysis_id
            )
            suggestion_result = await session.execute(suggestion_query)
            suggestions = suggestion_result.scalars().all()
            
            # Format suggestions
            formatted_suggestions = [
                {
                    "suggestion_id": s.suggestion_id,
                    "suggestion_type": s.suggestion_type,
                    "suggestion_text": s.suggestion_text,
                    "priority_level": s.priority_level,
                    "example_text": s.example_text,
                    "improved_example": s.improved_example
                }
                for s in suggestions
            ]
            
            # Add to history
            history.append({
                "analysis_id": analysis.analysis_id,
                "date": analysis.date.isoformat(),
                "metrics": {
                    "total_speaking_time_seconds": analysis.total_speaking_time_seconds,
                    "total_conversations": analysis.total_conversations,
                    "filler_word_count": analysis.filler_word_count,
                    "filler_word_percentage": float(analysis.filler_word_percentage) if analysis.filler_word_percentage else 0,
                    "avg_words_per_minute": analysis.avg_words_per_minute,
                    "vocabulary_diversity_score": float(analysis.vocabulary_diversity_score) if analysis.vocabulary_diversity_score else 0,
                    "clarity_score": float(analysis.clarity_score) if analysis.clarity_score else 0,
                    "confidence_score": float(analysis.confidence_score) if analysis.confidence_score else 0,
                    "overall_rating": float(analysis.overall_rating) if analysis.overall_rating else 0
                },
                "suggestions": formatted_suggestions
            })
        
        return history
    
    async def get_user_statistics(
        self, 
        session: AsyncSession, 
        user_id: str, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get aggregated statistics for a user over a time period.
        
        Args:
            session: Database session
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary of statistics
        """
        # Find user record
        user_query = select(User).where(User.username.like(f"%{user_id}%"))
        user_result = await session.execute(user_query)
        user = user_result.scalars().first()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            return {
                "user_id": user_id,
                "days_analyzed": days,
                "total_speaking_time": 0,
                "total_conversations": 0,
                "average_metrics": {},
                "trend_data": {}
            }
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Query analysis results within date range
        query = (
            select(AnalysisResult)
            .where(and_(
                AnalysisResult.user_id == user.user_id,
                AnalysisResult.date >= start_date,
                AnalysisResult.date <= end_date
            ))
            .order_by(AnalysisResult.date)
        )
        result = await session.execute(query)
        analyses = result.scalars().all()
        
        if not analyses:
            logger.warning(f"No analysis results found for user {user_id} in the past {days} days")
            return {
                "user_id": user_id,
                "days_analyzed": days,
                "total_speaking_time": 0,
                "total_conversations": 0,
                "average_metrics": {},
                "trend_data": {}
            }
        
        # Calculate total speaking time and conversations
        total_speaking_time = sum(a.total_speaking_time_seconds for a in analyses if a.total_speaking_time_seconds)
        total_conversations = sum(a.total_conversations for a in analyses if a.total_conversations)
        
        # Calculate averages
        avg_filler_percentage = sum(float(a.filler_word_percentage) for a in analyses if a.filler_word_percentage) / len(analyses)
        avg_wpm = sum(a.avg_words_per_minute for a in analyses if a.avg_words_per_minute) / len(analyses)
        avg_diversity = sum(float(a.vocabulary_diversity_score) for a in analyses if a.vocabulary_diversity_score) / len(analyses)
        avg_clarity = sum(float(a.clarity_score) for a in analyses if a.clarity_score) / len(analyses)
        avg_confidence = sum(float(a.confidence_score) for a in analyses if a.confidence_score) / len(analyses)
        
        # Prepare trend data (daily values)
        trend_dates = [a.date.isoformat() for a in analyses]
        trend_filler = [float(a.filler_word_percentage) if a.filler_word_percentage else 0 for a in analyses]
        trend_wpm = [a.avg_words_per_minute if a.avg_words_per_minute else 0 for a in analyses]
        trend_confidence = [float(a.confidence_score) if a.confidence_score else 0 for a in analyses]
        trend_clarity = [float(a.clarity_score) if a.clarity_score else 0 for a in analyses]
        
        return {
            "user_id": user_id,
            "days_analyzed": days,
            "total_speaking_time": total_speaking_time,
            "total_conversations": total_conversations,
            "average_metrics": {
                "avg_filler_percentage": avg_filler_percentage,
                "avg_words_per_minute": avg_wpm,
                "avg_vocabulary_diversity": avg_diversity,
                "avg_clarity_score": avg_clarity,
                "avg_confidence_score": avg_confidence
            },
            "trend_data": {
                "dates": trend_dates,
                "filler_percentage": trend_filler,
                "words_per_minute": trend_wpm,
                "confidence_score": trend_confidence,
                "clarity_score": trend_clarity
            }
        }
    
    async def record_audio_chunk(
        self, 
        session: AsyncSession, 
        user_id: str, 
        session_id: str, 
        file_path: str, 
        sample_rate: int, 
        duration: float
    ) -> None:
        """
        Record an audio chunk for later processing.
        
        For now, this is a stub - we'll implement proper audio tracking later.
        
        Args:
            session: Database session
            user_id: User ID
            session_id: Session ID
            file_path: Path to saved audio file
            sample_rate: Audio sample rate
            duration: Audio duration in seconds
        """
        # Placeholder for now
        logger.info(f"Recorded audio chunk of {duration:.2f}s for user {user_id}, session {session_id}")
    
    async def record_audio_upload(
        self, 
        session: AsyncSession, 
        user_id: str, 
        session_id: str, 
        file_path: str, 
        filename: str
    ) -> None:
        """
        Record an audio file upload.
        
        For now, this is a stub - we'll implement proper audio tracking later.
        
        Args:
            session: Database session
            user_id: User ID
            session_id: Session ID
            file_path: Path to saved audio file
            filename: Original filename
        """
        # Placeholder for now
        logger.info(f"Recorded audio upload {filename} for user {user_id}, session {session_id}")
    
    async def store_transcription(
        self, 
        session: AsyncSession, 
        user_id: str, 
        session_id: str, 
        segments: List[Dict]
    ) -> None:
        """
        Store a transcription from audio.
        
        Args:
            session: Database session
            user_id: User ID
            session_id: Session ID
            segments: Transcription segments
        """
        # Find user record
        user_query = select(User).where(User.username.like(f"%{user_id}%"))
        user_result = await session.execute(user_query)
        user = user_result.scalars().first()
        
        if not user:
            # Create a placeholder user
            user = await self.get_or_create_user(
                session, 
                user_id=user_id, 
                username=f"User-{user_id[:8]}", 
                device_id=f"OMI-{user_id[:8]}"
            )
        
        # Store the conversation and segments
        await self.store_conversation(session, user.user_id, session_id, segments)
        logger.info(f"Stored transcription with {len(segments)} segments for user {user_id}")
    
    async def get_audio_processing_status(
        self, 
        session: AsyncSession, 
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get status of audio processing for a session.
        
        Args:
            session: Database session
            session_id: Session ID
            
        Returns:
            Dictionary with status information
        """
        # Placeholder for now
        return {
            "session_id": session_id,
            "status": "pending",
            "message": "Audio processing status tracking not yet implemented",
            "progress": 0,
            "estimated_completion": None
        }