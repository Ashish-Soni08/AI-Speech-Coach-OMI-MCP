import requests
import json
import asyncio
import logging
from datetime import datetime
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Test data simulating an OMI device webhook call
test_data = {
    "session_id": "test-session-123",
    "user_id": "test-user-456",
    "segments": [
        {
            "text": "Hello, um, this is a test recording for the, uh, speech coach.",
            "speaker": "SPEAKER_00",
            "speakerId": 0,
            "is_user": True,
            "start": 0.0,
            "end": 5.0
        },
        {
            "text": "I want to improve my speaking skills and like reduce filler words.",
            "speaker": "SPEAKER_00",
            "speakerId": 0,
            "is_user": True,
            "start": 5.5,
            "end": 12.0
        },
        {
            "text": "Sometimes I speak too quickly and people have trouble following what I'm saying.",
            "speaker": "SPEAKER_00",
            "speakerId": 0,
            "is_user": True,
            "start": 12.5,
            "end": 18.0
        }
    ]
}

async def test_webhook():
    """Test the transcript analysis webhook endpoint."""
    try:
        logger.info("Sending test request to webhook endpoint...")
        
        # The webhook URL (local development)
        webhook_url = "http://localhost:8000/api/transcript/analyze"
        
        # Send the request
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Check the response
        if response.status_code == 200:
            logger.info("Webhook request successful!")
            logger.info(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Extract and display the analysis metrics
            metrics = response.json().get("metrics", {})
            suggestions = response.json().get("suggestions", [])
            
            logger.info("\n--- Speech Analysis Results ---")
            logger.info(f"Filler Word Count: {metrics.get('total_filler_count', 0)}")
            logger.info(f"Words Per Minute: {metrics.get('words_per_minute', 0)}")
            logger.info(f"Confidence Score: {metrics.get('confidence_score', 0)}")
            logger.info(f"Vocabulary Diversity: {metrics.get('vocabulary_diversity', 0)}")
            
            logger.info("\n--- Improvement Suggestions ---")
            for i, suggestion in enumerate(suggestions, 1):
                logger.info(f"{i}. [{suggestion.get('suggestion_type')}] {suggestion.get('suggestion_text')}")
                if suggestion.get('example_text'):
                    logger.info(f"   Example: {suggestion.get('example_text')}")
                    logger.info(f"   Improved: {suggestion.get('improved_example')}")
            
            return True
        else:
            logger.error(f"Webhook request failed with status code {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error testing webhook: {str(e)}")
        return False

# Execute the test
if __name__ == "__main__":
    try:
        result = asyncio.run(test_webhook())
        if result:
            logger.info("Webhook test completed successfully!")
            sys.exit(0)
        else:
            logger.error("Webhook test failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Test interrupted by user.")
        sys.exit(130)