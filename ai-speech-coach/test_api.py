import pytest
from fastapi.testclient import TestClient
from main import app
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create test client
client = TestClient(app)

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
        }
    ]
}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Speech Coach"
    assert data["status"] == "online"
    assert "timestamp" in data
    assert "endpoints" in data

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_transcript_analyze():
    """Test the transcript analysis endpoint"""
    response = client.post("/api/transcript/analyze", json=test_data)
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure of response
    assert "metrics" in data
    assert "suggestions" in data
    assert "session_id" in data
    assert "user_id" in data
    assert "timestamp" in data
    
    # Check the metrics
    metrics = data["metrics"]
    assert "filler_words" in metrics
    assert "total_filler_count" in metrics
    assert "words_per_minute" in metrics
    
    # Verify that filler words were detected
    assert metrics["total_filler_count"] > 0
    
    # Print a summary of the results
    logger.info("\n--- API Test Results ---")
    logger.info(f"Transcript Analysis Results:")
    logger.info(f"Filler Word Count: {metrics['total_filler_count']}")
    logger.info(f"Words Per Minute: {metrics['words_per_minute']}")
    if "confidence_score" in metrics:
        logger.info(f"Confidence Score: {metrics['confidence_score']}")
    
    logger.info("\nSuggestions:")
    for i, suggestion in enumerate(data["suggestions"], 1):
        logger.info(f"{i}. [{suggestion['suggestion_type']}] {suggestion['suggestion_text']}")

if __name__ == "__main__":
    logger.info("Running API tests...")
    test_root_endpoint()
    logger.info("✓ Root endpoint test passed")
    
    test_health_check()
    logger.info("✓ Health check test passed")
    
    test_transcript_analyze()
    logger.info("✓ Transcript analysis test passed")
    
    logger.info("All API tests passed!")