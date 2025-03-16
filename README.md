# AI-Speech-Coach

An AI-powered tool providing personalized feedback and guidance to improve articulation and speaking skills. It analyzes speech patterns from OMI device conversations, providing end-of-day reports with specific improvement suggestions.

## Sparking the Idea: Video Inspiration

[![YouTube](http://i.ytimg.com/vi/2FTx7DV7sv8/hqdefault.jpg)](https://www.youtube.com/watch?v=2FTx7DV7sv8)

![AI_Speech_Coach](assets/speech_coach.jpg)

## Features

- **Filler Word Detection**: Identifies and counts filler words like "um," "uh," "like," etc.
- **Speech Pace Analysis**: Measures words per minute and speaking rhythm
- **Vocabulary Assessment**: Evaluates word variety and suggests improvements
- **Confidence Scoring**: Analyzes speaking confidence based on multiple metrics
- **Personalized Suggestions**: Provides actionable recommendations for improvement
- **Progress Tracking**: Monitors improvement over time with historical data
- **End-of-Day Analysis**: Scheduled job at 7 PM to process the day's conversations
- **MCP Integration**: Speech analysis tools accessible through Model Context Protocol

## Architecture

- **Backend**: FastAPI with async PostgreSQL database
- **Frontend**: Next.js with shadcn/ui components and responsive design
- **Analysis Engine**: Speech analysis components for filler words, pace, and vocabulary
- **MCP Server**: Provides speech analysis tools via Model Context Protocol
- **OMI Integration**: Real-time transcript and audio processing

## Setup & Installation

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-Speech-Coach-OMI-MCP.git
   cd AI-Speech-Coach-OMI-MCP
   ```

2. Use the start script to launch the application:
   ```bash
   chmod +x start.sh
   ./start.sh prod
   ```

3. Access the application:
   - Backend API: http://localhost:8000
   - Frontend Dashboard: http://localhost:3000

4. To stop the application:
   ```bash
   ./start.sh stop
   ```

### Manual Setup

#### Backend

1. Create a virtual environment and install dependencies:
   ```bash
   cd ai-speech-coach
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/speech_coach
   PORT=8000
   HOST=0.0.0.0
   DEBUG=True
   MCP_TRANSPORT=stdio
   ```

3. Initialize the database and start the server:
   ```bash
   python setup_database.py
   python main.py
   ```

#### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Create `.env.local` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Key Components

### Backend API Endpoints

- `POST /api/transcript/analyze`: Analyze transcript segments for speech patterns
- `GET /api/transcript/history/{user_id}`: Get historical analysis for a user
- `GET /api/transcript/statistics/{user_id}`: Get aggregated statistics for a user
- `POST /api/audio/upload`: Upload audio for analysis
- `POST /trigger-analysis`: Manually trigger end-of-day analysis

### MCP Tools

- `analyze_text`: Comprehensive speech analysis
- `detect_filler_words`: Identify and count filler words
- `generate_improvement_suggestions`: Get personalized improvement suggestions

### Dashboard Features

- Speech metrics visualization with charts and cards
- Historical progress tracking
- Personalized improvement suggestions panel
- Audio upload for analysis

## Project Structure

- `/ai-speech-coach`: Backend FastAPI application
  - `/analyzer`: Speech analysis algorithms
  - `/api`: API routes and services
  - `/mcp`: MCP server implementation
  - `/models`: Database models and schemas
- `/frontend`: Next.js dashboard application
  - `/src/components`: React components
  - `/src/lib`: Utilities and API service
  - `/src/app`: Page components and routing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

**Built for the MCP Hackathon at AGI House.**
