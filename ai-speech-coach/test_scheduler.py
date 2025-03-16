import asyncio
import logging
import sys
from datetime import datetime

# Import the function we want to test
from main import run_end_of_day_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_end_of_day_analysis():
    """
    Test the end-of-day analysis job functionality.
    
    This will manually trigger the analysis that normally runs at 7 PM.
    """
    logger.info("Starting test of end-of-day analysis job")
    
    try:
        # Run the analysis function
        logger.info("Triggering end-of-day analysis...")
        await run_end_of_day_analysis()
        
        logger.info("End-of-day analysis completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during end-of-day analysis: {str(e)}")
        return False

# Run the test
if __name__ == "__main__":
    logger.info(f"Testing end-of-day analysis at {datetime.now().isoformat()}")
    
    try:
        result = asyncio.run(test_end_of_day_analysis())
        
        if result:
            logger.info("End-of-day analysis test completed successfully!")
            sys.exit(0)
        else:
            logger.error("End-of-day analysis test failed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Test interrupted by user.")
        sys.exit(130)