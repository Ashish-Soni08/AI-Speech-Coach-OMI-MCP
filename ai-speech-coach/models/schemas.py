from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date


class UserBase(BaseModel):
    username: str
    email: str
    device_id: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    created_at: datetime
    settings: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


class SpeechSegmentBase(BaseModel):
    text_content: str
    start_time: datetime
    end_time: datetime
    is_user_speaking: bool
    speaker_identification: Optional[str] = None


class SpeechSegmentCreate(SpeechSegmentBase):
    conversation_id: int
    user_id: int


class SpeechSegment(SpeechSegmentBase):
    segment_id: int
    conversation_id: int
    user_id: int
    duration_seconds: Optional[int] = None
    word_count: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    start_timestamp: datetime
    end_timestamp: datetime
    conversation_context: Optional[str] = None
    participants_count: Optional[int] = None
    total_duration_seconds: Optional[int] = None


class ConversationCreate(ConversationBase):
    user_id: int


class Conversation(ConversationBase):
    conversation_id: int
    user_id: int
    created_at: datetime
    speech_segments: List[SpeechSegment] = []

    class Config:
        orm_mode = True


class AnalysisResultBase(BaseModel):
    date: date
    total_speaking_time_seconds: Optional[int] = None
    total_conversations: Optional[int] = None
    filler_word_count: Optional[int] = None
    filler_word_percentage: Optional[float] = None
    avg_words_per_minute: Optional[int] = None
    pace_variability: Optional[float] = None
    vocabulary_diversity_score: Optional[float] = None
    clarity_score: Optional[float] = None
    confidence_score: Optional[float] = None
    overall_rating: Optional[float] = None


class AnalysisResultCreate(AnalysisResultBase):
    user_id: int


class AnalysisResult(AnalysisResultBase):
    analysis_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ImprovementSuggestionBase(BaseModel):
    suggestion_type: str
    suggestion_text: str
    priority_level: Optional[int] = None
    example_text: Optional[str] = None
    improved_example: Optional[str] = None


class ImprovementSuggestionCreate(ImprovementSuggestionBase):
    analysis_id: int
    segment_id: Optional[int] = None


class ImprovementSuggestion(ImprovementSuggestionBase):
    suggestion_id: int
    analysis_id: int
    segment_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for transcript processing endpoint
class TranscriptSegment(BaseModel):
    text: str
    speaker: str
    speakerId: int
    is_user: bool
    start: float
    end: float


class TranscriptRequest(BaseModel):
    segments: List[TranscriptSegment]
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")


# Schema for analysis response
class AnalysisMetrics(BaseModel):
    filler_words: Dict[str, int] = Field(default_factory=dict)
    total_filler_count: int = 0
    words_per_minute: float = 0
    total_words: int = 0
    speaking_time_seconds: float = 0
    vocabulary_diversity: float = 0
    confidence_score: float = 0
    clarity_score: float = 0


class SpeechAnalysisResponse(BaseModel):
    analysis_id: Optional[int] = None
    session_id: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metrics: AnalysisMetrics
    suggestions: List[ImprovementSuggestion] = []