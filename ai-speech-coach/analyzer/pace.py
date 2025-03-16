from typing import List, Dict, Tuple
import logging
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

class PaceAnalyzer:
    """
    Analyzer component for measuring and analyzing speech pace.
    """
    
    # Speech pace guidelines (words per minute)
    PACE_RANGES = {
        "too_slow": (0, 120),
        "slow": (120, 150),
        "optimal": (150, 180),
        "fast": (180, 210),
        "too_fast": (210, float('inf'))
    }
    
    def __init__(self, custom_pace_ranges: Dict[str, Tuple[float, float]] = None):
        """
        Initialize the pace analyzer with optional custom pace ranges.
        
        Args:
            custom_pace_ranges: Optional dictionary of custom pace ranges
        """
        self.pace_ranges = self.PACE_RANGES.copy()
        
        if custom_pace_ranges:
            self.pace_ranges.update(custom_pace_ranges)
        
        logger.info("PaceAnalyzer initialized with pace ranges")
    
    def calculate_words_per_minute(self, word_count: int, duration_seconds: float) -> float:
        """
        Calculate words per minute from word count and duration.
        
        Args:
            word_count: Number of words spoken
            duration_seconds: Duration in seconds
            
        Returns:
            Words per minute rate
        """
        if duration_seconds <= 0:
            return 0.0
        
        # Convert seconds to minutes and calculate WPM
        minutes = duration_seconds / 60.0
        wpm = word_count / minutes
        
        return round(wpm, 1)
    
    def analyze_segments(self, segments: List[Dict]) -> Dict:
        """
        Analyze speech pace across multiple segments.
        
        Args:
            segments: List of speech segments with text, start_time, and end_time
            
        Returns:
            Dictionary containing pace metrics
        """
        if not segments:
            return {
                "avg_wpm": 0.0,
                "pace_variability": 0.0,
                "pace_category": "no_data",
                "segment_paces": []
            }
        
        total_words = 0
        total_seconds = 0.0
        segment_paces = []
        
        # Calculate pace for each segment
        for segment in segments:
            text = segment.get("text_content", "")
            
            # Calculate word count for this segment
            words = len(text.split())
            total_words += words
            
            # Calculate duration in seconds
            start_time = segment.get("start_time")
            end_time = segment.get("end_time")
            
            if isinstance(start_time, datetime) and isinstance(end_time, datetime):
                duration = (end_time - start_time).total_seconds()
            else:
                # Handle case where start/end might be float values
                duration = float(end_time) - float(start_time)
            
            total_seconds += duration
            
            # Calculate WPM for this segment
            if duration > 0:
                wpm = self.calculate_words_per_minute(words, duration)
                segment_paces.append({
                    "segment_id": segment.get("segment_id", None),
                    "wpm": wpm,
                    "duration_seconds": duration,
                    "word_count": words
                })
        
        # Calculate overall WPM
        avg_wpm = self.calculate_words_per_minute(total_words, total_seconds)
        
        # Calculate pace variability (standard deviation of segment WPMs)
        if len(segment_paces) > 1:
            pace_values = [s["wpm"] for s in segment_paces]
            pace_variability = float(np.std(pace_values))
        else:
            pace_variability = 0.0
        
        # Determine pace category
        pace_category = "optimal"
        for category, (min_pace, max_pace) in self.pace_ranges.items():
            if min_pace <= avg_wpm < max_pace:
                pace_category = category
                break
        
        return {
            "avg_wpm": avg_wpm,
            "pace_variability": pace_variability,
            "pace_category": pace_category,
            "segment_paces": segment_paces
        }
    
    def generate_improvement_suggestions(self, pace_analysis: Dict) -> List[Dict]:
        """
        Generate improvement suggestions based on pace analysis.
        
        Args:
            pace_analysis: Dictionary containing pace metrics
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        avg_wpm = pace_analysis.get("avg_wpm", 0)
        pace_category = pace_analysis.get("pace_category", "no_data")
        pace_variability = pace_analysis.get("pace_variability", 0)
        
        # No suggestions if we don't have data
        if pace_category == "no_data":
            return suggestions
        
        # Suggestion based on overall pace
        if pace_category == "too_slow":
            suggestion = {
                "suggestion_type": "pace",
                "suggestion_text": f"Your pace of {avg_wpm} words per minute is too slow, which may cause listeners to lose interest. Aim to increase your speaking pace slightly.",
                "priority_level": 4,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        
        elif pace_category == "slow":
            suggestion = {
                "suggestion_type": "pace",
                "suggestion_text": f"Your pace of {avg_wpm} words per minute is on the slower side. For most contexts, you could speak a bit faster to maintain engagement.",
                "priority_level": 3,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        
        elif pace_category == "fast":
            suggestion = {
                "suggestion_type": "pace",
                "suggestion_text": f"Your pace of {avg_wpm} words per minute is slightly fast. Consider slowing down a bit to ensure clarity.",
                "priority_level": 3,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        
        elif pace_category == "too_fast":
            suggestion = {
                "suggestion_type": "pace",
                "suggestion_text": f"Your pace of {avg_wpm} words per minute is too fast, making it difficult for listeners to follow. Try to slow down and include more pauses.",
                "priority_level": 5,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        
        # Suggestion based on pace variability
        if pace_variability > 30:
            suggestion = {
                "suggestion_type": "pace_consistency",
                "suggestion_text": f"Your speaking pace varies significantly (±{pace_variability:.1f} WPM). Work on maintaining a more consistent pace for clarity.",
                "priority_level": 3,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        elif pace_variability < 10 and avg_wpm > 100:
            suggestion = {
                "suggestion_type": "pace_dynamics",
                "suggestion_text": "Your speaking pace is very uniform. Using some pace variation can make your speech more engaging.",
                "priority_level": 2,
                "example_text": None,
                "improved_example": None
            }
            suggestions.append(suggestion)
        
        return suggestions