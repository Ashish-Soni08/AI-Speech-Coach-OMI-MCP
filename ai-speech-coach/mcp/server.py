import mcp
from mcp import FastMCP, Context
import logging
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime, date
import os

# Import analyzer components
from analyzer.filler_words import FillerWordAnalyzer
from analyzer.pace import PaceAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

# Create MCP server
mcp_server = FastMCP(
    name="speech-coach-server",
    instructions="""
    This server provides tools for analyzing speech patterns and providing coaching.
    You can analyze text for filler words, speaking pace, and other speech metrics.
    The server also provides historical analysis data and improvement suggestions.
    """
)


@mcp_server.tool()
async def analyze_text(text: str, ctx: Context) -> Dict[str, Any]:
    """
    Analyze a text for speech patterns and provide coaching feedback.
    
    This tool analyzes provided text for:
    - Filler words (um, uh, like, etc.)
    - Speaking pace metrics
    - Vocabulary diversity
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing analysis results and improvement suggestions
    """
    await ctx.info(f"Analyzing text of length {len(text)}")
    
    try:
        # Initialize analyzers
        filler_word_analyzer = FillerWordAnalyzer()
        
        # Analyze filler words
        filler_words, total_fillers = filler_word_analyzer.analyze_text(text)
        total_words = len(text.split())
        filler_percentage = filler_word_analyzer.get_filler_percentage(
            total_fillers, total_words)
        
        # Generate suggestions
        suggestions = filler_word_analyzer.generate_improvement_suggestions(
            filler_words, total_fillers, text)
        
        # Calculate metrics
        vocabulary_diversity = len(set(text.lower().split())) / total_words if total_words > 0 else 0
        
        # Prepare response
        result = {
            "metrics": {
                "filler_words": filler_words,
                "total_filler_count": total_fillers,
                "filler_percentage": filler_percentage,
                "total_words": total_words,
                "vocabulary_diversity": vocabulary_diversity
            },
            "suggestions": suggestions
        }
        
        return result
    
    except Exception as e:
        await ctx.error(f"Error analyzing text: {str(e)}")
        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": f"Error analyzing text: {str(e)}"
                }
            ]
        }


@mcp_server.tool()
async def detect_filler_words(text: str, ctx: Context) -> Dict[str, Any]:
    """
    Detect and count filler words in a text.
    
    This tool identifies common filler words like "um", "uh", "like", etc.,
    and provides counts and percentages.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing filler word counts and metrics
    """
    await ctx.info(f"Detecting filler words in text of length {len(text)}")
    
    try:
        # Initialize analyzer
        filler_word_analyzer = FillerWordAnalyzer()
        
        # Analyze filler words
        filler_words, total_fillers = filler_word_analyzer.analyze_text(text)
        total_words = len(text.split())
        filler_percentage = filler_word_analyzer.get_filler_percentage(
            total_fillers, total_words)
        
        # Prepare response
        result = {
            "filler_words": filler_words,
            "total_filler_count": total_fillers,
            "filler_percentage": filler_percentage,
            "total_words": total_words
        }
        
        return result
    
    except Exception as e:
        await ctx.error(f"Error detecting filler words: {str(e)}")
        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": f"Error detecting filler words: {str(e)}"
                }
            ]
        }


@mcp_server.tool()
async def generate_improvement_suggestions(text: str, ctx: Context) -> List[Dict]:
    """
    Generate improvement suggestions for speech based on text analysis.
    
    This tool analyzes the provided text and generates coaching suggestions
    for improving speaking style, reducing filler words, and enhancing clarity.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of improvement suggestions
    """
    await ctx.info(f"Generating improvement suggestions for text of length {len(text)}")
    
    try:
        # Initialize analyzers
        filler_word_analyzer = FillerWordAnalyzer()
        
        # Analyze filler words
        filler_words, total_fillers = filler_word_analyzer.analyze_text(text)
        
        # Generate suggestions
        suggestions = filler_word_analyzer.generate_improvement_suggestions(
            filler_words, total_fillers, text)
        
        # Add general suggestions
        if len(suggestions) < 3:
            suggestions.append({
                "suggestion_type": "vocabulary",
                "suggestion_text": "Expand your vocabulary by reading widely and learning new words. This will make your speech more engaging and precise.",
                "priority_level": 2,
                "example_text": None,
                "improved_example": None
            })
            
            suggestions.append({
                "suggestion_type": "structure",
                "suggestion_text": "Practice using clear structure in your speech: introduction, main points, and conclusion. This helps listeners follow your thoughts.",
                "priority_level": 2,
                "example_text": None,
                "improved_example": None
            })
        
        return suggestions
    
    except Exception as e:
        await ctx.error(f"Error generating improvement suggestions: {str(e)}")
        return [{
            "suggestion_type": "error",
            "suggestion_text": f"Error generating improvement suggestions: {str(e)}",
            "priority_level": 1,
            "example_text": None,
            "improved_example": None
        }]


@mcp_server.resource("resource://speech-coach/example/transcript")
def get_example_transcript() -> Dict[str, Any]:
    """
    Get an example speech transcript for testing.
    
    Returns:
        Example transcript data
    """
    return {
        "segments": [
            {
                "text": "Hello, um, this is a test recording for the, uh, speech coach.",
                "speaker": "USER",
                "speakerId": 0,
                "is_user": True,
                "start": 0.0,
                "end": 5.0
            },
            {
                "text": "I want to improve my speaking skills and like reduce filler words.",
                "speaker": "USER",
                "speakerId": 0,
                "is_user": True,
                "start": 5.5,
                "end": 12.0
            },
            {
                "text": "Sometimes I speak too quickly and people have trouble following what I'm saying.",
                "speaker": "USER",
                "speakerId": 0,
                "is_user": True,
                "start": 12.5,
                "end": 18.0
            },
            {
                "text": "I also need to work on my vocabulary and you know use more varied words in my speech.",
                "speaker": "USER",
                "speakerId": 0,
                "is_user": True,
                "start": 18.5,
                "end": 24.0
            }
        ]
    }


@mcp_server.prompt()
def analyze_speech_prompt() -> List[Dict[str, Any]]:
    """
    Prompt for analyzing speech patterns and providing coaching.
    
    This prompt guides the analysis of speech transcripts to identify
    patterns, issues, and opportunities for improvement.
    """
    return [
        {
            "role": "user",
            "content": """
            Analyze my speech patterns from the provided transcript or audio.
            
            Please identify:
            1. Filler words I commonly use
            2. My speaking pace (words per minute)
            3. Any issues with clarity or structure
            4. Vocabulary diversity and suggestions
            
            Then provide specific, actionable suggestions for improvement.
            """
        }
    ]


@mcp_server.prompt()
def practice_exercise_prompt() -> List[Dict[str, Any]]:
    """
    Prompt for generating speech practice exercises.
    
    This prompt creates personalized practice exercises based on
    identified speech patterns and areas for improvement.
    """
    return [
        {
            "role": "user",
            "content": """
            Create speech practice exercises tailored to my needs.
            
            Based on my speech analysis, please create:
            1. A short tongue twister targeting my specific pronunciation challenges
            2. A structured speaking exercise (1-2 minutes) that helps me reduce filler words
            3. A pacing exercise to help me maintain optimal speaking speed
            4. A vocabulary expansion exercise related to my field
            
            Make these exercises practical and tailored to my specific needs.
            """
        }
    ]


def setup_mcp_server():
    """
    Set up and configure the MCP server.
    """
    logger.info("Setting up MCP server")
    return mcp_server

# Export the server instance - makes it accessible via import
__all__ = ["mcp_server", "setup_mcp_server"]


if __name__ == "__main__":
    # Run the MCP server directly if this file is executed
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting MCP server directly")
    mcp_server.run(transport="stdio")