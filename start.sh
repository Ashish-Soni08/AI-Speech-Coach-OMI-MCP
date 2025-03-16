#!/bin/bash

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check requirements
check_requirements() {
  echo -e "${BLUE}Checking requirements...${NC}"
  
  # Check if Docker is installed
  if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker to continue.${NC}"
    exit 1
  fi
  
  # Check if Docker Compose is installed
  if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose to continue.${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}All requirements met!${NC}"
}

# Function to set up the environment
setup_environment() {
  echo -e "${BLUE}Setting up environment...${NC}"
  
  # Check if .env file exists, create it if it doesn't
  if [ ! -f ai-speech-coach/.env ]; then
    echo -e "${BLUE}Creating .env file in the ai-speech-coach directory...${NC}"
    cat > ai-speech-coach/.env << EOL
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres/speech_coach

# API Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# MCP Server Configuration
MCP_TRANSPORT=stdio
EOL
    echo -e "${GREEN}.env file created!${NC}"
  else
    echo -e "${GREEN}.env file already exists.${NC}"
  fi
  
  # Check if .env.local file exists for frontend, create it if it doesn't
  if [ ! -f frontend/.env.local ]; then
    echo -e "${BLUE}Creating .env.local file in the frontend directory...${NC}"
    cat > frontend/.env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOL
    echo -e "${GREEN}.env.local file created!${NC}"
  else
    echo -e "${GREEN}.env.local file for frontend already exists.${NC}"
  fi
}

# Function to start the development environment
start_dev() {
  echo -e "${BLUE}Starting development environment...${NC}"
  
  # Start PostgreSQL container
  echo -e "${BLUE}Starting PostgreSQL container...${NC}"
  docker run --name speech_coach_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=speech_coach -p 5432:5432 -d postgres:16
  
  # Wait for PostgreSQL to start
  echo -e "${BLUE}Waiting for PostgreSQL to start...${NC}"
  sleep 5
  
  # Install backend dependencies
  echo -e "${BLUE}Installing backend dependencies...${NC}"
  cd ai-speech-coach && pip install -r requirements.txt
  
  # Initialize the database
  echo -e "${BLUE}Initializing the database...${NC}"
  cd ai-speech-coach && python setup_database.py
  
  # Start the backend server
  echo -e "${BLUE}Starting the backend server...${NC}"
  cd ai-speech-coach && python main.py &
  
  # Install frontend dependencies
  echo -e "${BLUE}Installing frontend dependencies...${NC}"
  cd frontend && npm install
  
  # Start the frontend server
  echo -e "${BLUE}Starting the frontend server...${NC}"
  cd frontend && npm run dev
}

# Function to start the production environment
start_prod() {
  echo -e "${BLUE}Starting production environment...${NC}"
  
  # Build and start containers
  docker-compose up -d
  
  echo -e "${GREEN}Production environment started!${NC}"
  echo -e "${GREEN}Backend API is available at http://localhost:8000${NC}"
  echo -e "${GREEN}Frontend dashboard is available at http://localhost:3000${NC}"
}

# Function to stop the environment
stop() {
  echo -e "${BLUE}Stopping environment...${NC}"
  
  # Stop containers
  docker-compose down
  
  # Stop individual containers if they're running
  docker stop speech_coach_db &> /dev/null || true
  docker rm speech_coach_db &> /dev/null || true
  
  echo -e "${GREEN}Environment stopped!${NC}"
}

# Check requirements
check_requirements

# Parse command
case "$1" in
  dev)
    setup_environment
    start_dev
    ;;
  prod)
    setup_environment
    start_prod
    ;;
  stop)
    stop
    ;;
  *)
    echo -e "${BLUE}Usage: $0 {dev|prod|stop}${NC}"
    echo -e "${BLUE}  dev:  Start development environment (PostgreSQL in Docker, backend and frontend directly)${NC}"
    echo -e "${BLUE}  prod: Start production environment (all components in Docker)${NC}"
    echo -e "${BLUE}  stop: Stop all containers${NC}"
    exit 1
esac

exit 0