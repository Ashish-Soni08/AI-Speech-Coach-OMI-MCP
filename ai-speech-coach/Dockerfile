FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]