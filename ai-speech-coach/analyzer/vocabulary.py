import re
from typing import Dict, List, Tuple, Any
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

logger = logging.getLogger(__name__)

class VocabularyAnalyzer:
    """
    Analyzer component for evaluating vocabulary diversity and usage in speech.
    """
    
    # Download required NLTK datasets (uncomment when first running)
    # nltk.download('punkt')
    # nltk.download('stopwords')
    
    def __init__(self):
        """Initialize the vocabulary analyzer."""
        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            # If stopwords aren't available, use a basic set
            self.stopwords = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
                'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
                'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
                'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
                'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 
                't', 'can', 'will', 'just', 'don', 'should', 'now'
            }
        
        logger.info("VocabularyAnalyzer initialized")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text content for vocabulary metrics.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dictionary of vocabulary metrics
        """
        if not text:
            return {
                "diversity_score": 0.0,
                "unique_word_count": 0,
                "total_word_count": 0,
                "top_words": [],
                "rare_words": []
            }
        
        # Simple tokenization for testing
        try:
            # Try to use NLTK's word_tokenize
            tokens = word_tokenize(text.lower())
        except:
            # Fall back to simple splitting if NLTK isn't available
            tokens = text.lower().split()
        
        # Filter out punctuation and stopwords
        words = [word for word in tokens if word.isalnum() and word not in self.stopwords]
        
        if not words:
            return {
                "diversity_score": 0.0,
                "unique_word_count": 0,
                "total_word_count": 0,
                "top_words": [],
                "rare_words": []
            }
        
        # Calculate metrics
        word_freq = Counter(words)
        unique_words = set(words)
        
        # Type-token ratio (unique words / total words)
        diversity_score = len(unique_words) / len(words)
        
        # Get most common words
        top_words = word_freq.most_common(5)
        
        # Get least common words (excludes words that appear only once)
        rare_words = [(word, count) for word, count in word_freq.items() 
                     if count > 1 and count < 3][:5]
        
        return {
            "diversity_score": diversity_score,
            "unique_word_count": len(unique_words),
            "total_word_count": len(words),
            "top_words": top_words,
            "rare_words": rare_words
        }
    
    def generate_improvement_suggestions(self, analysis: Dict[str, Any], text: str = None) -> List[Dict]:
        """
        Generate improvement suggestions based on vocabulary analysis.
        
        Args:
            analysis: Dictionary containing vocabulary analysis
            text: Optional original text for contextual examples
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check diversity score
        diversity_score = analysis.get("diversity_score", 0.0)
        
        if diversity_score < 0.4:
            suggestions.append({
                "suggestion_type": "vocabulary",
                "suggestion_text": "Your vocabulary diversity is low. Try to use a wider range of words to express yourself and avoid repeating the same terms.",
                "priority_level": 4,
                "example_text": None,
                "improved_example": None
            })
        elif diversity_score < 0.6:
            suggestions.append({
                "suggestion_type": "vocabulary",
                "suggestion_text": "Your vocabulary diversity is moderate. Consider expanding your vocabulary by reading widely and learning new words related to your field.",
                "priority_level": 3,
                "example_text": None,
                "improved_example": None
            })
        
        # Check for overused words
        top_words = analysis.get("top_words", [])
        if top_words and len(top_words) > 0:
            overused_word, count = top_words[0]
            total_words = analysis.get("total_word_count", 100)
            
            # If the most common word appears more than 5% of the time
            if count / total_words > 0.05 and overused_word not in self.stopwords:
                # Get synonyms (placeholder for now)
                synonyms = self.get_synonyms(overused_word)
                
                suggestion = {
                    "suggestion_type": "overused_words",
                    "suggestion_text": f"You frequently use the word '{overused_word}'. Try using alternatives like: {', '.join(synonyms[:3])}.",
                    "priority_level": 3,
                    "example_text": None,
                    "improved_example": None
                }
                
                # If we have the original text, try to find an example
                if text:
                    # Use regex to find the overused word in context
                    pattern = re.compile(r"[^.!?]*\b" + re.escape(overused_word) + r"\b[^.!?]*[.!?]", 
                                        re.IGNORECASE)
                    examples = pattern.findall(text)
                    
                    if examples:
                        # Use the first example
                        example = examples[0].strip()
                        suggestion["example_text"] = example
                        
                        # Create improved example by replacing with a synonym
                        if synonyms:
                            improved = re.sub(r"\b" + re.escape(overused_word) + r"\b", 
                                            synonyms[0], 
                                            example, 
                                            flags=re.IGNORECASE, 
                                            count=1)
                            suggestion["improved_example"] = improved
                
                suggestions.append(suggestion)
        
        return suggestions
    
    def get_synonyms(self, word: str) -> List[str]:
        """
        Get synonyms for a word.
        
        This is a simple placeholder function. In a real implementation,
        you would use a thesaurus API or WordNet.
        
        Args:
            word: The word to find synonyms for
            
        Returns:
            List of synonyms
        """
        # Simple placeholder synonyms for common words
        synonyms_dict = {
            "good": ["excellent", "great", "fine", "superior"],
            "bad": ["poor", "inferior", "substandard", "inadequate"],
            "big": ["large", "huge", "substantial", "enormous"],
            "small": ["tiny", "little", "miniature", "compact"],
            "happy": ["joyful", "pleased", "delighted", "content"],
            "sad": ["unhappy", "sorrowful", "downcast", "melancholy"],
            "important": ["significant", "crucial", "vital", "essential"],
            "problem": ["issue", "challenge", "difficulty", "obstacle"],
            "idea": ["concept", "notion", "thought", "plan"],
            "think": ["believe", "consider", "contemplate", "reflect"],
            "say": ["state", "mention", "express", "declare"],
            "get": ["obtain", "acquire", "receive", "procure"],
            "make": ["create", "produce", "construct", "form"],
            "look": ["appear", "seem", "glance", "view"],
            "want": ["desire", "wish", "long for", "crave"]
        }
        
        return synonyms_dict.get(word.lower(), ["other words", "alternatives", "different terms"])