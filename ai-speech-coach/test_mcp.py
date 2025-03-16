import asyncio
import sys
import os

# Add the current directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import mcp_server

async def main():
    """Test the MCP server tools"""
    print("Testing MCP server tools...")
    
    # Test the analyze_text tool
    text = """Hello, um, this is a test recording for the, uh, speech coach.
    I want to improve my speaking skills and like reduce filler words.
    Sometimes I speak too quickly and people have trouble following what I'm saying.
    I also need to work on my vocabulary and you know use more varied words in my speech."""
    
    # Set up context mock
    class MockContext:
        async def info(self, message):
            print(f"INFO: {message}")
        
        async def error(self, message):
            print(f"ERROR: {message}")
    
    # Test analyze_text
    print("\n=== Testing analyze_text ===")
    result = await mcp_server._tools["analyze_text"].func(text, MockContext())
    print(f"Analysis metrics: {result['metrics']}")
    print(f"Suggestions count: {len(result['suggestions'])}")
    for i, suggestion in enumerate(result['suggestions'], 1):
        print(f"Suggestion {i}: {suggestion['suggestion_text']}")
    
    # Test detect_filler_words
    print("\n=== Testing detect_filler_words ===")
    filler_result = await mcp_server._tools["detect_filler_words"].func(text, MockContext())
    print(f"Filler words: {filler_result['filler_words']}")
    print(f"Total filler count: {filler_result['total_filler_count']}")
    print(f"Filler percentage: {filler_result['filler_percentage']:.2f}%")
    
    # Test generate_improvement_suggestions
    print("\n=== Testing generate_improvement_suggestions ===")
    suggestion_result = await mcp_server._tools["generate_improvement_suggestions"].func(text, MockContext())
    for i, suggestion in enumerate(suggestion_result, 1):
        print(f"Suggestion {i}: {suggestion['suggestion_text']}")
    
    # Test the example transcript resource
    print("\n=== Testing example transcript resource ===")
    transcript = mcp_server._resources["resource://speech-coach/example/transcript"].func()
    print(f"Example transcript segments: {len(transcript['segments'])}")
    
    print("\nAll MCP server tests completed!")

if __name__ == "__main__":
    asyncio.run(main())