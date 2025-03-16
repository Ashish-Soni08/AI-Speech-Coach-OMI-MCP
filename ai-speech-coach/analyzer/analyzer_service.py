from typing import List, Dict, Any
import logging
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
import asyncio

# Import analyzer components
from analyzer.filler_words import FillerWordAnalyzer, count_words
from analyzer.pace import PaceAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

# Download NLTK data (uncomment when first running)
# nltk.download('punkt')


class SpeechAnalyzerService:
    """
    Service for analyzing speech transcripts and providing feedback.
    """
    
    def __init__(self):
        """Initialize the speech analyzer service with all component analyzers."""
        self.filler_word_analyzer = FillerWordAnalyzer()
        self.pace_analyzer = PaceAnalyzer()
        logger.info("SpeechAnalyzerService initialized with all analyzer components")
    
    async def analyze_transcript(self, transcript_segments: List[Dict]) -> Dict:
        """
        Analyze transcript segments and provide comprehensive feedback.
        
        Args:
            transcript_segments: List of transcript segments to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        if not transcript_segments:
            logger.warning("No transcript segments provided for analysis")
            return {
                "metrics": {
                    "filler_words": {},
                    "total_filler_count": 0,
                    "words_per_minute": 0,
                    "total_words": 0,
                    "speaking_time_seconds": 0,
                    "vocabulary_diversity": 0,
                    "confidence_score": 0,
                    "clarity_score": 0
                },
                "suggestions": []
            }
        
        logger.info(f"Analyzing {len(transcript_segments)} transcript segments")
        
        # Extract user segments (where is_user_speaking is True)
        user_segments = [s for s in transcript_segments if s.get("is_user_speaking", False)]
        
        if not user_segments:
            logger.warning("No user speech segments found in transcript")
            return {
                "metrics": {
                    "filler_words": {},
                    "total_filler_count": 0,
                    "words_per_minute": 0,
                    "total_words": 0,
                    "speaking_time_seconds": 0,
                    "vocabulary_diversity": 0,
                    "confidence_score": 0,
                    "clarity_score": 0
                },
                "suggestions": []
            }
        
        # Combine all user speech for aggregate analysis
        combined_text = " ".join([s.get("text_content", "") for s in user_segments])
        
        # Count total words
        total_words = count_words(combined_text)
        
        # Calculate total speaking time
        total_speaking_time = 0.0
        for segment in user_segments:
            start_time = segment.get("start_time")
            end_time = segment.get("end_time")
            
            if isinstance(start_time, datetime) and isinstance(end_time, datetime):
                duration = (end_time - start_time).total_seconds()
            else:
                # Handle case where start/end might be float values
                duration = float(end_time) - float(start_time)
            
            total_speaking_time += duration
        
        # Run analyses in parallel using asyncio tasks
        analyses = await asyncio.gather(
            self._analyze_filler_words(combined_text),
            self._analyze_pace(user_segments),
            self._analyze_vocabulary_diversity(combined_text)
        )
        
        filler_analysis, pace_analysis, vocabulary_analysis = analyses
        
        # Generate all improvement suggestions
        suggestions = []
        suggestions.extend(filler_analysis.get("suggestions", []))
        suggestions.extend(pace_analysis.get("suggestions", []))
        
        # Combine metrics
        metrics = {
            "filler_words": filler_analysis.get("filler_words", {}),
            "total_filler_count": filler_analysis.get("total_filler_count", 0),
            "words_per_minute": pace_analysis.get("avg_wpm", 0),
            "pace_variability": pace_analysis.get("pace_variability", 0),
            "total_words": total_words,
            "speaking_time_seconds": total_speaking_time,
            "vocabulary_diversity": vocabulary_analysis.get("diversity_score", 0),
            "confidence_score": self._calculate_confidence_score(filler_analysis, pace_analysis),
            "clarity_score": self._calculate_clarity_score(pace_analysis)
        }
        
        return {
            "metrics": metrics,
            "suggestions": suggestions
        }
    
    async def _analyze_filler_words(self, text: str) -> Dict:
        """Analyze filler words in the text."""
        filler_words, total_fillers = self.filler_word_analyzer.analyze_text(text)
        total_words = count_words(text)
        
        # Calculate percentage
        filler_percentage = self.filler_word_analyzer.get_filler_percentage(
            total_fillers, total_words)
        
        # Generate suggestions
        suggestions = self.filler_word_analyzer.generate_improvement_suggestions(
            filler_words, total_fillers, text)
        
        return {
            "filler_words": filler_words,
            "total_filler_count": total_fillers,
            "filler_percentage": filler_percentage,
            "suggestions": suggestions
        }
    
    async def _analyze_pace(self, segments: List[Dict]) -> Dict:
        """Analyze speaking pace from segments."""
        pace_analysis = self.pace_analyzer.analyze_segments(segments)
        
        # Generate suggestions
        suggestions = self.pace_analyzer.generate_improvement_suggestions(pace_analysis)
        
        return {
            **pace_analysis,
            "suggestions": suggestions
        }
    
    async def _analyze_vocabulary_diversity(self, text: str) -> Dict:
        """Analyze vocabulary diversity."""
        if not text:
            return {"diversity_score": 0.0}
        
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Filter out punctuation
        words = [word for word in tokens if word.isalnum()]
        
        if not words:
            return {"diversity_score": 0.0}
        
        # Calculate type-token ratio (unique words / total words)
        unique_words = set(words)
        diversity_score = len(unique_words) / len(words)
        
        return {
            "diversity_score": diversity_score,
            "unique_word_count": len(unique_words),
            "total_word_count": len(words)
        }
    
    def _calculate_confidence_score(self, filler_analysis: Dict, pace_analysis: Dict) -> float:
        """Calculate a confidence score based on various metrics."""
        filler_percentage = filler_analysis.get("filler_percentage", 0)
        pace_category = pace_analysis.get("pace_category", "optimal")
        
        # Base score
        score = 100
        
        # Reduce score based on filler words
        # Higher percentage of filler words reduces confidence score
        if filler_percentage > 0:
            score -= min(30, filler_percentage * 3)
        
        # Adjust based on pace
        if pace_category == "too_slow":
            score -= 15
        elif pace_category == "slow":
            score -= 5
        elif pace_category == "fast":
            score -= 5
        elif pace_category == "too_fast":
            score -= 15
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return score
    
    def _calculate_clarity_score(self, pace_analysis: Dict) -> float:
        """Calculate a clarity score based on various metrics."""
        pace_category = pace_analysis.get("pace_category", "optimal")
        pace_variability = pace_analysis.get("pace_variability", 0)
        
        # Base score
        score = 100
        
        # Adjust based on pace
        if pace_category == "too_slow":
            score -= 10
        elif pace_category == "slow":
            score -= 5
        elif pace_category == "fast":
            score -= 10
        elif pace_category == "too_fast":
            score -= 20
        
        # Adjust based on pace variability
        if pace_variability > 30:
            score -= 15
        elif pace_variability > 20:
            score -= 10
        elif pace_variability < 5:
            score -= 5  # Too monotone
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return score