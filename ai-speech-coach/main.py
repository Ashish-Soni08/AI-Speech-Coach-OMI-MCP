from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import List, Optional
import logging
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

# Import our modules
from api.routes import transcript_router, audio_router
from mcp.server import setup_mcp_server
from models.database import init_db, get_db
from api.services.database_service import DatabaseService
from analyzer.analyzer_service import SpeechAnalyzerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize services
analyzer_service = SpeechAnalyzerService()
db_service = DatabaseService()

# Initialize scheduler
scheduler = AsyncIOScheduler()

# Initialize FastAPI app
app = FastAPI(
    title="AI Speech Coach",
    description="An OMI integration for analyzing speech patterns and providing coaching",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcript_router.router, prefix="/api/transcript", tags=["transcript"])
app.include_router(audio_router.router, prefix="/api/audio", tags=["audio"])

# End-of-day analysis job (7 PM)
async def run_end_of_day_analysis():
    """Run end-of-day analysis for all users"""
    logger.info("Running scheduled end-of-day speech analysis")
    
    try:
        async for session in get_db():
            # Get all active users
            users = await db_service.get_all_users(session)
            
            # For each user, run daily analysis
            for user in users:
                try:
                    # Get today's conversations
                    today_convos = await db_service.get_user_daily_conversations(
                        session, 
                        user_id=user.user_id,
                        date=datetime.now().date()
                    )
                    
                    if not today_convos:
                        logger.info(f"No conversations found today for user {user.user_id}")
                        continue
                    
                    # Get speech segments
                    segments = []
                    for convo in today_convos:
                        convo_segments = await db_service.get_conversation_segments(
                            session, 
                            conversation_id=convo.conversation_id
                        )
                        segments.extend(convo_segments)
                    
                    if not segments:
                        logger.info(f"No speech segments found for user {user.user_id}")
                        continue
                    
                    # Run analysis
                    analysis_result = await analyzer_service.analyze_transcript(segments)
                    
                    # Store results
                    await db_service.store_analysis_results(
                        session,
                        user_id=user.user_id,
                        metrics=analysis_result["metrics"],
                        suggestions=analysis_result["suggestions"]
                    )
                    
                    logger.info(f"Completed end-of-day analysis for user {user.user_id}")
                
                except Exception as e:
                    logger.error(f"Error analyzing data for user {user.user_id}: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error in end-of-day analysis job: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting AI Speech Coach application")
    
    # Initialize database
    await init_db()
    
    # Set up MCP server
    setup_mcp_server()
    
    # Schedule end-of-day analysis at 7 PM
    scheduler.add_job(
        run_end_of_day_analysis,
        CronTrigger(hour=19, minute=0),  # 7:00 PM
        id="end_of_day_analysis",
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduled end-of-day analysis job for 7:00 PM")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down AI Speech Coach application")
    
    # Shut down scheduler
    if scheduler.running:
        scheduler.shutdown()

@app.get("/")
async def root():
    """Root endpoint providing basic information"""
    return {
        "name": "AI Speech Coach",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "transcript": "/api/transcript",
            "audio": "/api/audio",
            "dashboard": "/dashboard"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/trigger-analysis")
async def trigger_analysis(background_tasks: BackgroundTasks):
    """Manually trigger end-of-day analysis"""
    background_tasks.add_task(run_end_of_day_analysis)
    return {"status": "analysis_triggered", "message": "End-of-day analysis has been triggered"}

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app", 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("DEBUG", "True").lower() == "true")
    )