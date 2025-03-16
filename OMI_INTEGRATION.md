# AI Speech Coach - OMI Integration Guide

This guide explains how to set up and use the AI Speech Coach as an OMI (Open Model Interface) application.

## What is OMI?

OMI (Open Model Interface) allows devices like the OMI DevKit to send transcripts and audio data to external applications for processing. The AI Speech Coach can be registered as an OMI application to receive real-time transcripts from your conversations, analyze them, and provide personalized coaching.

## Setup Instructions

### 1. Deploy Your AI Speech Coach

First, you need to have your AI Speech Coach application accessible via the Internet:

#### Option A: Local Development with Ngrok

For testing during development, you can use ngrok to expose your local server:

1. Start your AI Speech Coach application:
   ```bash
   ./start.sh dev
   ```

2. In a separate terminal, run ngrok to expose your FastAPI server:
   ```bash
   ngrok http 8000
   ```

3. Make note of the ngrok URL (e.g., `https://abcd1234.ngrok.io`)

#### Option B: Cloud Deployment

For production use, deploy your application to a cloud provider:

1. Configure your environment variables in `.env`:
   ```
   ENVIRONMENT=production
   OMI_API_KEY=your_secure_api_key_here
   ```

2. Deploy using Docker Compose:
   ```bash
   ./start.sh prod
   ```

3. Make sure your server has a domain name and HTTPS configured

### 2. Register Your App in the OMI Mobile App

1. Open the OMI mobile app
2. Navigate to Settings > Developer Options > Manage Apps
3. Tap "Add New App"
4. Fill in the details:
   - **App Name**: AI Speech Coach
   - **App Type**: Real-Time Transcript Processor
   - **Webhook URL**: Your server URL + `/api/transcript/analyze` (e.g., `https://your-domain.com/api/transcript/analyze` or your ngrok URL + `/api/transcript/analyze`)
   - **API Key**: The same key you set as `OMI_API_KEY` in your server (if using production mode)
   - **Description**: AI coach that analyzes speech patterns and provides personalized improvement suggestions

### 3. Using the App with OMI DevKit

1. Connect your OMI DevKit to the mobile app
2. Enable the AI Speech Coach app in the OMI mobile app
3. Start having conversations with your OMI DevKit
4. Transcripts will be automatically sent to your AI Speech Coach for analysis
5. At the end of the day (7 PM), all conversations will be processed in a batch analysis
6. Open your AI Speech Coach dashboard at `https://your-domain.com` or `http://localhost:3002` to see your speech analysis and improvement suggestions

## Understanding the Data Flow

1. **Real-time Processing**:
   - The OMI DevKit sends transcript segments to your server's `/api/transcript/analyze` endpoint
   - Each segment contains text, speaker information, and timestamps
   - The AI Speech Coach analyzes each segment for filler words, pace, etc.
   - The analysis is stored in the PostgreSQL database

2. **End-of-Day Analysis**:
   - At 7 PM each day, the scheduled job runs
   - All conversations from the day are analyzed together
   - Aggregate metrics like overall filler word percentage and vocabulary diversity are calculated
   - Personalized improvement suggestions are generated based on the full day's speech patterns

3. **Dashboard Access**:
   - Access the dashboard to view your speech metrics
   - See trends over time in your speaking patterns
   - Review specific improvement suggestions
   - Track your progress as you practice and improve

## Webhook Format

The OMI DevKit sends data to your webhook in the following format:

```json
{
  "session_id": "abc123",
  "user_id": "user456",
  "segments": [
    {
      "text": "Hello, this is a sample segment.",
      "speaker": "SPEAKER_00",
      "speakerId": 0,
      "is_user": true,
      "start": 10.5,
      "end": 13.2
    },
    {
      "text": "This is another segment with some um filler words.",
      "speaker": "SPEAKER_00",
      "speakerId": 0,
      "is_user": true,
      "start": 14.0,
      "end": 17.5
    }
  ]
}
```

## Troubleshooting

### 1. Webhook Not Receiving Data

- Check that your server is running and accessible from the internet
- Verify the webhook URL in the OMI app settings
- Check your server logs for any errors
- Make sure your API key matches in both the OMI app and server config

### 2. Analysis Not Appearing in Dashboard

- Check that data is being stored in the database
- Verify that the end-of-day analysis job is running at 7 PM
- Check for any errors in the server logs during analysis
- Make sure you're using the same user ID in the OMI app and when accessing the dashboard

### 3. API Key Issues

If you receive a 403 Forbidden error, check:
- That your API key is correctly set in your server's environment variables
- That the same API key is configured in the OMI app
- That your server is running in production mode if API key validation is enabled

## Advanced Configuration

### Customizing Analysis Schedule

By default, the end-of-day analysis runs at 7 PM. To change this time:

1. Edit the `main.py` file:
   ```python
   # Schedule end-of-day analysis at a different time (e.g., 9 PM)
   scheduler.add_job(
       run_end_of_day_analysis,
       CronTrigger(hour=21, minute=0),  # 9:00 PM
       id="end_of_day_analysis",
       replace_existing=True
   )
   ```

2. Restart your server to apply the changes

### Configuring Speech Analysis Thresholds

You can customize the thresholds for speech metrics by editing the analyzer components in the `analyzer` directory.