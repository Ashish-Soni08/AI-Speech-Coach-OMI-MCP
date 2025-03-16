from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get database connection string from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/speech_coach")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Create declarative base
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    device_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSONB)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    speech_segments = relationship("SpeechSegment", back_populates="user")
    analysis_results = relationship("AnalysisResult", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    start_timestamp = Column(DateTime, nullable=False)
    end_timestamp = Column(DateTime, nullable=False)
    conversation_context = Column(String(100))
    participants_count = Column(Integer)
    total_duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    speech_segments = relationship("SpeechSegment", back_populates="conversation")


class SpeechSegment(Base):
    __tablename__ = "speech_segments"
    
    segment_id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.conversation_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    text_content = Column(Text, nullable=False)
    is_user_speaking = Column(Boolean, nullable=False)
    speaker_identification = Column(String(50))
    duration_seconds = Column(Integer)
    word_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="speech_segments")
    user = relationship("User", back_populates="speech_segments")
    improvement_suggestions = relationship("ImprovementSuggestion", back_populates="speech_segment")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    analysis_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date, nullable=False)
    total_speaking_time_seconds = Column(Integer)
    total_conversations = Column(Integer)
    filler_word_count = Column(Integer)
    filler_word_percentage = Column(Numeric(5, 2))
    avg_words_per_minute = Column(Integer)
    pace_variability = Column(Numeric(5, 2))
    vocabulary_diversity_score = Column(Numeric(5, 2))
    clarity_score = Column(Numeric(5, 2))
    confidence_score = Column(Numeric(5, 2))
    overall_rating = Column(Numeric(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analysis_results")
    improvement_suggestions = relationship("ImprovementSuggestion", back_populates="analysis_result")


class ImprovementSuggestion(Base):
    __tablename__ = "improvement_suggestions"
    
    suggestion_id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.analysis_id"))
    segment_id = Column(Integer, ForeignKey("speech_segments.segment_id"), nullable=True)
    suggestion_type = Column(String(50), nullable=False)
    suggestion_text = Column(Text, nullable=False)
    priority_level = Column(Integer)
    example_text = Column(Text)
    improved_example = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    analysis_result = relationship("AnalysisResult", back_populates="improvement_suggestions")
    speech_segment = relationship("SpeechSegment", back_populates="improvement_suggestions")


async def init_db():
    """Initialize the database by creating all tables"""
    async with engine.begin() as conn:
        try:
            # Create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise


# Function to get a database session
async def get_db():
    """Dependency for getting an async database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()