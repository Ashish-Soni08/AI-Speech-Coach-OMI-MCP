import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class FillerWordAnalyzer:
    """
    Analyzer component for detecting and analyzing filler words in speech.
    """
    
    # Common filler words to detect
    COMMON_FILLER_WORDS = {
        'um': True,
        'uh': True,
        'like': True,
        'you know': True,
        'sort of': True,
        'kind of': True,
        'basically': True,
        'actually': True,
        'literally': True,
        'i mean': True,
        'right': True,
        'okay': True,
        'so': True,
        'well': True,
        'just': True
    }
    
    def __init__(self, custom_fillers: Dict[str, bool] = None):
        """
        Initialize the filler word analyzer with optional custom filler words.
        
        Args:
            custom_fillers: Optional dictionary of custom filler words to detect
        """
        self.filler_words = self.COMMON_FILLER_WORDS.copy()
        
        if custom_fillers:
            self.filler_words.update(custom_fillers)
        
        # Prepare regex pattern for detecting filler words
        filler_list = "|".join(r"\b" + re.escape(word) + r"\b" for word in self.filler_words.keys())
        self.filler_pattern = re.compile(filler_list, re.IGNORECASE)
        
        logger.info(f"FillerWordAnalyzer initialized with {len(self.filler_words)} filler words")
    
    def analyze_text(self, text: str) -> Tuple[Dict[str, int], int]:
        """
        Analyze text content for filler words.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Tuple containing:
                - Dictionary of filler words and their counts
                - Total count of filler words
        """
        if not text:
            return {}, 0
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Find all filler word matches
        matches = self.filler_pattern.findall(text_lower)
        
        # Count occurrences of each filler word
        filler_count = {}
        for match in matches:
            match = match.lower()
            filler_count[match] = filler_count.get(match, 0) + 1
        
        total_fillers = sum(filler_count.values())
        
        logger.debug(f"Found {total_fillers} filler words in text")
        return filler_count, total_fillers
    
    def get_filler_percentage(self, filler_count: int, total_words: int) -> float:
        """
        Calculate the percentage of filler words in the text.
        
        Args:
            filler_count: Number of filler words
            total_words: Total number of words in the text
            
        Returns:
            Percentage of filler words (0-100)
        """
        if total_words == 0:
            return 0.0
        
        return (filler_count / total_words) * 100
    
    def generate_improvement_suggestions(self, filler_analysis: Dict[str, int], 
                                         total_fillers: int, 
                                         text: str = None) -> List[Dict]:
        """
        Generate improvement suggestions based on filler word analysis.
        
        Args:
            filler_analysis: Dictionary of filler words and their counts
            total_fillers: Total count of filler words
            text: Optional original text for contextual examples
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Sort filler words by frequency (most frequent first)
        sorted_fillers = sorted(filler_analysis.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_fillers:
            return suggestions
        
        # Generate suggestion for most common filler word
        most_common_filler, count = sorted_fillers[0]
        
        suggestion = {
            "suggestion_type": "filler_words",
            "suggestion_text": f"Replace '{most_common_filler}' with strategic pauses to sound more confident.",
            "priority_level": min(5, max(1, count // 3)),  # Priority 1-5 based on frequency
            "example_text": None,
            "improved_example": None
        }
        
        # If we have the original text, try to find an example
        if text:
            # Use regex to find the most common filler word in context
            pattern = re.compile(r"[^.!?]*\b" + re.escape(most_common_filler) + r"\b[^.!?]*[.!?]", 
                                 re.IGNORECASE)
            examples = pattern.findall(text)
            
            if examples:
                # Use the first example
                example = examples[0].strip()
                suggestion["example_text"] = example
                
                # Create improved example by replacing with a pause
                improved = re.sub(r"\b" + re.escape(most_common_filler) + r"\b", 
                                  "[pause]", 
                                  example, 
                                  flags=re.IGNORECASE)
                suggestion["improved_example"] = improved
        
        suggestions.append(suggestion)
        
        # General suggestion if multiple filler words are used
        if len(sorted_fillers) > 1:
            filler_list = ", ".join([f"'{word}'" for word, _ in sorted_fillers[:3]])
            
            suggestion = {
                "suggestion_type": "filler_words",
                "suggestion_text": f"Practice reducing filler words like {filler_list} by speaking more slowly and deliberately.",
                "priority_level": min(4, max(1, total_fillers // 5)),
                "example_text": None,
                "improved_example": None
            }
            
            suggestions.append(suggestion)
        
        return suggestions


# Helper function to count total words in text
def count_words(text: str) -> int:
    """Count the total number of words in a text."""
    if not text:
        return 0
    
    # Split by whitespace and count non-empty words
    words = [word for word in text.split() if word.strip()]
    return len(words)