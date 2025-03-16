import sys
import os
import logging
from analyzer.filler_words import FillerWordAnalyzer
from analyzer.pace import PaceAnalyzer
from analyzer.vocabulary import VocabularyAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Sample text for testing
SAMPLE_TEXT = """
Hello, um, this is a test recording for the, uh, speech coach.
I want to improve my speaking skills and like reduce filler words.
Sometimes I speak too quickly and people have trouble following what I'm saying.
I also need to work on my vocabulary and you know use more varied words in my speech.
"""

def test_filler_word_analyzer():
    """Test the filler word analyzer"""
    logger.info("\n==== Testing FillerWordAnalyzer ====")
    
    # Initialize analyzer
    analyzer = FillerWordAnalyzer()
    
    # Analyze the sample text
    filler_words, total_fillers = analyzer.analyze_text(SAMPLE_TEXT)
    
    # Calculate percentage
    total_words = len(SAMPLE_TEXT.split())
    percentage = analyzer.get_filler_percentage(total_fillers, total_words)
    
    # Generate suggestions
    suggestions = analyzer.generate_improvement_suggestions(filler_words, total_fillers, SAMPLE_TEXT)
    
    # Log results
    logger.info(f"Filler words detected: {filler_words}")
    logger.info(f"Total fillers: {total_fillers}")
    logger.info(f"Filler percentage: {percentage:.2f}%")
    logger.info(f"Number of suggestions: {len(suggestions)}")
    
    for i, suggestion in enumerate(suggestions, 1):
        logger.info(f"Suggestion {i}: {suggestion['suggestion_text']}")
        if suggestion.get('example_text'):
            logger.info(f"Example: {suggestion['example_text']}")
            logger.info(f"Improved: {suggestion['improved_example']}")
    
    # Run assertions
    assert isinstance(filler_words, dict), "filler_words should be a dictionary"
    assert total_fillers > 0, "Should detect some filler words"
    assert len(suggestions) > 0, "Should generate suggestions"
    
    return True

def test_pace_analyzer():
    """Test the pace analyzer"""
    logger.info("\n==== Testing PaceAnalyzer ====")
    
    # Initialize analyzer
    analyzer = PaceAnalyzer()
    
    # Create sample segments
    segments = [
        {
            "text_content": "Hello, this is a test recording for the speech coach.",
            "start_time": 0.0,
            "end_time": 5.0,
            "duration_seconds": 5.0
        },
        {
            "text_content": "I want to improve my speaking skills and reduce filler words.",
            "start_time": 5.5,
            "end_time": 12.0,
            "duration_seconds": 6.5
        },
        {
            "text_content": "Sometimes I speak too quickly and people have trouble following what I'm saying.",
            "start_time": 12.5,
            "end_time": 18.0,
            "duration_seconds": 5.5
        }
    ]
    
    # Analyze pace
    pace_analysis = analyzer.analyze_segments(segments)
    
    # Generate suggestions
    suggestions = analyzer.generate_improvement_suggestions(pace_analysis)
    
    # Log results
    logger.info(f"Average WPM: {pace_analysis.get('avg_wpm', 0)}")
    logger.info(f"Pace category: {pace_analysis.get('pace_category', '')}")
    logger.info(f"Pace variability: {pace_analysis.get('pace_variability', 0)}")
    logger.info(f"Number of suggestions: {len(suggestions)}")
    
    for i, suggestion in enumerate(suggestions, 1):
        logger.info(f"Suggestion {i}: {suggestion['suggestion_text']}")
    
    # Run assertions
    assert "avg_wpm" in pace_analysis, "Should calculate average WPM"
    assert "pace_category" in pace_analysis, "Should determine pace category"
    assert "pace_variability" in pace_analysis, "Should calculate pace variability"
    
    return True

def test_vocabulary_analyzer():
    """Test the vocabulary analyzer"""
    logger.info("\n==== Testing VocabularyAnalyzer ====")
    
    # Initialize analyzer
    analyzer = VocabularyAnalyzer()
    
    # Analyze vocabulary
    analysis = analyzer.analyze_text(SAMPLE_TEXT)
    
    # Generate suggestions
    suggestions = analyzer.generate_improvement_suggestions(analysis, SAMPLE_TEXT)
    
    # Log results
    logger.info(f"Diversity score: {analysis.get('diversity_score', 0):.2f}")
    logger.info(f"Unique words: {analysis.get('unique_word_count', 0)}")
    logger.info(f"Total words: {analysis.get('total_word_count', 0)}")
    logger.info(f"Top words: {analysis.get('top_words', [])[:3]}")
    logger.info(f"Number of suggestions: {len(suggestions)}")
    
    for i, suggestion in enumerate(suggestions, 1):
        logger.info(f"Suggestion {i}: {suggestion['suggestion_text']}")
        if suggestion.get('example_text'):
            logger.info(f"Example: {suggestion['example_text']}")
            logger.info(f"Improved: {suggestion['improved_example']}")
    
    # Run assertions
    assert "diversity_score" in analysis, "Should calculate diversity score"
    assert "unique_word_count" in analysis, "Should count unique words"
    assert "total_word_count" in analysis, "Should count total words"
    assert "top_words" in analysis, "Should identify top words"
    
    return True

if __name__ == "__main__":
    logger.info("Running analyzer tests...")
    
    # Run all tests
    filler_result = test_filler_word_analyzer()
    pace_result = test_pace_analyzer()
    vocab_result = test_vocabulary_analyzer()
    
    # Check overall results
    all_passed = filler_result and pace_result and vocab_result
    
    if all_passed:
        logger.info("\n✓ All analyzer tests passed!")
        sys.exit(0)
    else:
        logger.error("\n✗ Some analyzer tests failed!")
        sys.exit(1)