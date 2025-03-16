import unittest
from analyzer.filler_words import FillerWordAnalyzer

class TestFillerWordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FillerWordAnalyzer()
        self.sample_text = """
        Hello, um, this is a test recording for the, uh, speech coach.
        I want to improve my speaking skills and like reduce filler words.
        Sometimes I speak too quickly and people have trouble following what I'm saying.
        I also need to work on my vocabulary and you know use more varied words in my speech.
        """
    
    def test_analyze_text(self):
        filler_words, total_fillers = self.analyzer.analyze_text(self.sample_text)
        
        # Check if we detected filler words
        self.assertIsInstance(filler_words, dict)
        self.assertGreater(len(filler_words), 0)
        self.assertGreater(total_fillers, 0)
        
        # Check specific filler words
        self.assertTrue("um" in filler_words)
        self.assertTrue("uh" in filler_words)
        self.assertTrue("like" in filler_words)
        self.assertTrue("you know" in filler_words)
    
    def test_get_filler_percentage(self):
        filler_words, total_fillers = self.analyzer.analyze_text(self.sample_text)
        total_words = len(self.sample_text.split())
        
        percentage = self.analyzer.get_filler_percentage(total_fillers, total_words)
        
        # Check percentage calculation
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 0.0)
        self.assertLessEqual(percentage, 100.0)
        
        # Check edge cases
        self.assertEqual(self.analyzer.get_filler_percentage(5, 0), 0.0)
        self.assertEqual(self.analyzer.get_filler_percentage(0, 100), 0.0)
    
    def test_generate_improvement_suggestions(self):
        filler_words, total_fillers = self.analyzer.analyze_text(self.sample_text)
        
        suggestions = self.analyzer.generate_improvement_suggestions(filler_words, total_fillers, self.sample_text)
        
        # Check suggestions
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        
        # Check suggestion format
        for suggestion in suggestions:
            self.assertIn("suggestion_type", suggestion)
            self.assertIn("suggestion_text", suggestion)
            self.assertIn("priority_level", suggestion)

if __name__ == "__main__":
    unittest.main()