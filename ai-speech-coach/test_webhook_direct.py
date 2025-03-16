import requests
import json
import time
import logging
import sys

# Configure logging
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

def test_webhook(url="http://localhost:8000/api/transcript/analyze"):
    """Send a test webhook request to the backend"""
    logger.info(f"Sending test webhook request to {url}")
    
    try:
        # Send the request
        response = requests.post(
            url, 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        if response.status_code == 200:
            logger.info("Webhook request successful!")
            
            # Parse and display the response
            result = response.json()
            metrics = result.get("metrics", {})
            suggestions = result.get("suggestions", [])
            
            logger.info("\n--- Speech Analysis Results ---")
            logger.info(f"Session ID: {result.get('session_id')}")
            logger.info(f"User ID: {result.get('user_id')}")
            logger.info(f"Timestamp: {result.get('timestamp')}")
            
            logger.info("\n--- Metrics ---")
            logger.info(f"Filler Word Count: {metrics.get('total_filler_count', 0)}")
            logger.info(f"Filler Words: {json.dumps(metrics.get('filler_words', {}), indent=2)}")
            logger.info(f"Words Per Minute: {metrics.get('words_per_minute', 0)}")
            logger.info(f"Vocabulary Diversity: {metrics.get('vocabulary_diversity', 0)}")
            
            if "confidence_score" in metrics:
                logger.info(f"Confidence Score: {metrics.get('confidence_score')}")
            
            if "clarity_score" in metrics:
                logger.info(f"Clarity Score: {metrics.get('clarity_score')}")
            
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
    
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        return False

if __name__ == "__main__":
    # Wait a moment to make sure the server is running
    logger.info("Waiting for server to be ready...")
    time.sleep(2)
    
    # Check if a custom URL was provided
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/api/transcript/analyze"
    
    # Run the test
    success = test_webhook(url)
    
    if success:
        logger.info("Webhook test completed successfully!")
        sys.exit(0)
    else:
        logger.error("Webhook test failed.")
        sys.exit(1)