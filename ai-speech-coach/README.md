# AI Speech Coach

An intelligent speech coach that analyzes conversations and provides personalized feedback to help users become more articulate speakers.

## Features

- **Filler Word Detection**: Identifies and counts filler words like "um," "uh," "like," etc.
- **Speech Pace Analysis**: Measures words per minute and speaking rhythm
- **Vocabulary Assessment**: Evaluates word variety and suggests improvements
- **Confidence Scoring**: Analyzes speaking confidence based on multiple metrics
- **Personalized Suggestions**: Provides actionable recommendations for improvement
- **Progress Tracking**: Monitors improvement over time with historical data

## Architecture

This application consists of several components:

- **FastAPI Backend**: Handles API requests and serves the dashboard
- **PostgreSQL Database**: Stores conversation data, analysis results, and user information
- **Analysis Engine**: Processes speech transcripts to identify patterns and generate insights
- **MCP Server**: Provides tools for speech analysis through the Model Context Protocol
- **OMI Integration**: Connects with OMI devices for real-time transcript processing

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- Node.js (for dashboard frontend)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-speech-coach.git
   cd ai-speech-coach
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```
   python -m scripts.initialize_db
   ```

### Running the Application

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

2. Access the API at `http://localhost:8000`
3. Access the dashboard at `http://localhost:8000/dashboard`

### Running the MCP Server

The MCP server can be run separately for integration with MCP clients:

```
python -m mcp.server
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /api/transcript/analyze`: Analyze transcript segments for speech patterns
- `GET /api/transcript/history/{user_id}`: Get historical analysis for a user
- `POST /api/audio/upload`: Upload audio for analysis
- `POST /api/audio/stream`: Process streaming audio from devices

## MCP Tools

The following tools are available through the MCP server:

- `analyze_text`: Analyze text for speech patterns
- `detect_filler_words`: Detect and count filler words in text
- `generate_improvement_suggestions`: Generate improvement suggestions for speech

## MCP Resources

The server provides these resources:

- `resource://speech-coach/example/transcript`: Example speech transcript for testing

## MCP Prompts

The server provides these prompt templates:

- `analyze_speech_prompt`: Prompt for analyzing speech patterns
- `practice_exercise_prompt`: Prompt for generating speech practice exercises

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by research on effective communication techniques
- Built with FastAPI, SQLAlchemy, and FastMCP
- Thanks to the OMI team for device integration support