import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from models.database import Base, User, Conversation, SpeechSegment, AnalysisResult, ImprovementSuggestion
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/speech_coach")

async def create_tables():
    """Create all tables in the database"""
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return False

async def create_demo_data():
    """Create demo data for testing"""
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    try:
        # Create tables if they don't exist
        async with engine.begin() as conn:
            # Create user
            await conn.execute(
                text("""
                INSERT INTO users (username, email, device_id, created_at, settings)
                VALUES ('demo_user', 'demo@example.com', 'OMI-12345', :now, '{}')
                """),
                {"now": datetime.utcnow()}
            )
            
            # Get user ID
            result = await conn.execute(text("SELECT user_id FROM users WHERE username = 'demo_user'"))
            user_id = result.scalar()
            
            # Create conversation
            now = datetime.utcnow()
            await conn.execute(
                text("""
                INSERT INTO conversations 
                (user_id, start_timestamp, end_timestamp, conversation_context, participants_count, total_duration_seconds, created_at)
                VALUES (:user_id, :start, :end, 'Demo Conversation', 2, 300, :now)
                """),
                {
                    "user_id": user_id,
                    "start": now - timedelta(minutes=5),
                    "end": now,
                    "now": now
                }
            )
            
            # Get conversation ID
            result = await conn.execute(text("SELECT conversation_id FROM conversations WHERE user_id = :user_id"), {"user_id": user_id})
            conversation_id = result.scalar()
            
            # Create speech segments
            segment_texts = [
                "Hello, um, this is a test recording for the, uh, speech coach.",
                "I want to improve my speaking skills and like reduce filler words.",
                "Sometimes I speak too quickly and people have trouble following what I'm saying.",
                "I also need to work on my vocabulary and you know use more varied words in my speech."
            ]
            
            start_time = now - timedelta(minutes=5)
            for i, text in enumerate(segment_texts):
                segment_start = start_time + timedelta(seconds=i * 60)
                segment_end = segment_start + timedelta(seconds=50)
                
                await conn.execute(
                    text("""
                    INSERT INTO speech_segments
                    (conversation_id, user_id, start_time, end_time, text_content, is_user_speaking, 
                    speaker_identification, duration_seconds, word_count, created_at)
                    VALUES (:conversation_id, :user_id, :start, :end, :text, TRUE, 'USER', :duration, :word_count, :now)
                    """),
                    {
                        "conversation_id": conversation_id,
                        "user_id": user_id,
                        "start": segment_start,
                        "end": segment_end,
                        "text": text,
                        "duration": 50,
                        "word_count": len(text.split()),
                        "now": now
                    }
                )
            
            # Create analysis result
            await conn.execute(
                text("""
                INSERT INTO analysis_results
                (user_id, date, total_speaking_time_seconds, total_conversations, filler_word_count,
                filler_word_percentage, avg_words_per_minute, pace_variability, vocabulary_diversity_score,
                clarity_score, confidence_score, overall_rating, created_at)
                VALUES (:user_id, :date, 300, 1, 7, 5.2, 160, 15.3, 0.72, 78.5, 72.3, 75.4, :now)
                """),
                {
                    "user_id": user_id,
                    "date": now.date(),
                    "now": now
                }
            )
            
            # Get analysis ID
            result = await conn.execute(text("SELECT analysis_id FROM analysis_results WHERE user_id = :user_id"), {"user_id": user_id})
            analysis_id = result.scalar()
            
            # Create improvement suggestions
            suggestions = [
                ("filler_words", "Replace 'um' with strategic pauses to sound more confident.", 5),
                ("pace", "Your speaking pace varies significantly. Work on maintaining a more consistent pace for clarity.", 3),
                ("vocabulary", "Expand your vocabulary by incorporating more precise terms when describing concepts.", 2)
            ]
            
            for suggestion_type, suggestion_text, priority in suggestions:
                await conn.execute(
                    text("""
                    INSERT INTO improvement_suggestions
                    (analysis_id, suggestion_type, suggestion_text, priority_level, created_at)
                    VALUES (:analysis_id, :type, :text, :priority, :now)
                    """),
                    {
                        "analysis_id": analysis_id,
                        "type": suggestion_type,
                        "text": suggestion_text,
                        "priority": priority,
                        "now": now
                    }
                )
            
        logger.info("Demo data created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating demo data: {str(e)}")
        return False

async def main():
    """Main function to set up the database"""
    logger.info("Setting up database...")
    
    # Create tables
    success = await create_tables()
    if not success:
        return
    
    # Create demo data
    success = await create_demo_data()
    if not success:
        return
    
    logger.info("Database setup completed successfully")

if __name__ == "__main__":
    asyncio.run(main())