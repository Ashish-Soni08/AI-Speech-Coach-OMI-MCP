from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import List, Optional
import logging
from datetime import datetime

# Import our modules
from api.routes import transcript_router, audio_router
from mcp.server import setup_mcp_server
from models.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting AI Speech Coach application")
    
    # Initialize database
    await init_db()
    
    # Set up MCP server
    setup_mcp_server()

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

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )