import asyncio
import sys
import logging
import json
from datetime import datetime

# Add current directory to sys.path
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import MCP server
from mcp.server import mcp_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Mock context class for testing
class MockContext:
    async def info(self, message):
        logger.info(f"[MCP Context] {message}")
    
    async def error(self, message):
        logger.error(f"[MCP Context] {message}")
    
    async def report_progress(self, current, total):
        logger.info(f"[MCP Context] Progress: {current}/{total}")

# Sample text for testing
SAMPLE_TEXT = """
Hello, um, this is a test recording for the, uh, speech coach.
I want to improve my speaking skills and like reduce filler words.
Sometimes I speak too quickly and people have trouble following what I'm saying.
I also need to work on my vocabulary and you know use more varied words in my speech.
"""

async def test_analyze_text():
    """Test the analyze_text MCP tool"""
    logger.info("\n==== Testing analyze_text tool ====")
    
    try:
        # Get the tool function
        analyze_text_tool = mcp_server._tools.get("analyze_text")
        if not analyze_text_tool:
            logger.error("analyze_text tool not found in MCP server!")
            return False
        
        # Call the tool
        mock_ctx = MockContext()
        result = await analyze_text_tool.func(SAMPLE_TEXT, mock_ctx)
        
        # Check the result
        if result and isinstance(result, dict) and "metrics" in result:
            logger.info("analyze_text tool executed successfully!")
            logger.info(f"Result metrics: {json.dumps(result['metrics'], indent=2)}")
            logger.info(f"Suggestions count: {len(result.get('suggestions', []))}")
            return True
        else:
            logger.error(f"Unexpected result from analyze_text: {result}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing analyze_text: {str(e)}")
        return False

async def test_detect_filler_words():
    """Test the detect_filler_words MCP tool"""
    logger.info("\n==== Testing detect_filler_words tool ====")
    
    try:
        # Get the tool function
        detect_filler_words_tool = mcp_server._tools.get("detect_filler_words")
        if not detect_filler_words_tool:
            logger.error("detect_filler_words tool not found in MCP server!")
            return False
        
        # Call the tool
        mock_ctx = MockContext()
        result = await detect_filler_words_tool.func(SAMPLE_TEXT, mock_ctx)
        
        # Check the result
        if result and isinstance(result, dict) and "filler_words" in result:
            logger.info("detect_filler_words tool executed successfully!")
            logger.info(f"Filler words detected: {json.dumps(result['filler_words'], indent=2)}")
            logger.info(f"Total filler count: {result.get('total_filler_count', 0)}")
            logger.info(f"Filler percentage: {result.get('filler_percentage', 0):.2f}%")
            return True
        else:
            logger.error(f"Unexpected result from detect_filler_words: {result}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing detect_filler_words: {str(e)}")
        return False

async def test_generate_improvement_suggestions():
    """Test the generate_improvement_suggestions MCP tool"""
    logger.info("\n==== Testing generate_improvement_suggestions tool ====")
    
    try:
        # Get the tool function
        generate_suggestions_tool = mcp_server._tools.get("generate_improvement_suggestions")
        if not generate_suggestions_tool:
            logger.error("generate_improvement_suggestions tool not found in MCP server!")
            return False
        
        # Call the tool
        mock_ctx = MockContext()
        result = await generate_suggestions_tool.func(SAMPLE_TEXT, mock_ctx)
        
        # Check the result
        if result and isinstance(result, list) and len(result) > 0:
            logger.info("generate_improvement_suggestions tool executed successfully!")
            logger.info(f"Number of suggestions: {len(result)}")
            
            for i, suggestion in enumerate(result, 1):
                logger.info(f"Suggestion {i}: [{suggestion.get('suggestion_type')}] {suggestion.get('suggestion_text')}")
            
            return True
        else:
            logger.error(f"Unexpected result from generate_improvement_suggestions: {result}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing generate_improvement_suggestions: {str(e)}")
        return False

async def test_example_transcript_resource():
    """Test the example transcript resource"""
    logger.info("\n==== Testing example transcript resource ====")
    
    try:
        # Get the resource function
        resource_func = mcp_server._resources.get("resource://speech-coach/example/transcript")
        if not resource_func:
            logger.error("Example transcript resource not found in MCP server!")
            return False
        
        # Call the resource function
        result = resource_func.func()
        
        # Check the result
        if result and isinstance(result, dict) and "segments" in result:
            logger.info("Example transcript resource retrieved successfully!")
            logger.info(f"Number of segments: {len(result['segments'])}")
            return True
        else:
            logger.error(f"Unexpected result from example transcript resource: {result}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing example transcript resource: {str(e)}")
        return False

async def run_all_tests():
    """Run all MCP tool tests"""
    logger.info(f"Starting MCP tools tests at {datetime.now().isoformat()}")
    
    # Run all test functions
    test_results = await asyncio.gather(
        test_analyze_text(),
        test_detect_filler_words(),
        test_generate_improvement_suggestions(),
        test_example_transcript_resource()
    )
    
    # Check if all tests passed
    all_passed = all(test_results)
    
    # Report overall result
    if all_passed:
        logger.info("\n✓ All MCP tool tests PASSED!")
    else:
        logger.error("\n✗ Some MCP tool tests FAILED!")
        
        # Report which tests failed
        test_names = ["analyze_text", "detect_filler_words", "generate_improvement_suggestions", "example_transcript_resource"]
        for i, result in enumerate(test_results):
            status = "✓ PASSED" if result else "✗ FAILED"
            logger.info(f"{status}: {test_names[i]}")
    
    return all_passed

# Run all tests when this script is executed directly
if __name__ == "__main__":
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("Tests interrupted by user.")
        sys.exit(130)