import { AnalysisResult, UserStatistics } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";

// Error handling helper
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.detail || `API error: ${response.status} ${response.statusText}`
    );
  }
  return await response.json() as T;
}

// Get user's analysis history - Using real API if available, fallback to mock data
export async function getUserHistory(userId: string, limit: number = 10): Promise<AnalysisResult[]> {
  try {
    // Attempt to use the real API
    const response = await fetch(`${API_BASE_URL}/transcript/history/${userId}?limit=${limit}`);
    if (response.ok) {
      return await handleResponse<AnalysisResult[]>(response);
    } else {
      console.log("API endpoint not available, using mock data");
      return getDemoAnalysisHistory();
    }
  } catch (error) {
    console.log("Error connecting to API, using mock data", error);
    return getDemoAnalysisHistory();
  }
}

// Get user's statistics - Using real API if available, fallback to mock data
export async function getUserStatistics(userId: string, days: number = 30): Promise<UserStatistics> {
  try {
    // Attempt to use the real API
    const response = await fetch(`${API_BASE_URL}/transcript/statistics/${userId}?days=${days}`);
    if (response.ok) {
      return await handleResponse<UserStatistics>(response);
    } else {
      console.log("API endpoint not available, using mock data");
      return getDemoUserStatistics();
    }
  } catch (error) {
    console.log("Error connecting to API, using mock data", error);
    return getDemoUserStatistics();
  }
}

// Upload audio file for analysis - Using real API if available, fallback to mock response
export async function uploadAudioForAnalysis(audioFile: File, userId: string, analyzeImmediately: boolean = true): Promise<any> {
  const formData = new FormData();
  formData.append('audio_file', audioFile);
  formData.append('user_id', userId);
  formData.append('analyze_immediately', analyzeImmediately.toString());
  
  try {
    // Attempt to use the real API
    const response = await fetch(`${API_BASE_URL}/audio/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (response.ok) {
      return await handleResponse<any>(response);
    } else {
      console.log("API endpoint not available, using mock response");
      // Return mock upload result
      return {
        status: "success",
        message: "Audio file uploaded successfully (mock)",
        session_id: `mock-session-${Math.random().toString(36).substring(2, 10)}`,
        analysis: {
          status: "pending",
          message: "Analysis is being processed (mock)"
        }
      };
    }
  } catch (error) {
    console.log("Error connecting to API, using mock response", error);
    // Return mock upload result
    return {
      status: "success",
      message: "Audio file uploaded successfully (mock)",
      session_id: `mock-session-${Math.random().toString(36).substring(2, 10)}`,
      analysis: null
    };
  }
}

// Check status of audio processing - Using real API if available, fallback to mock status
export async function checkAudioProcessingStatus(sessionId: string): Promise<any> {
  try {
    // Attempt to use the real API
    const response = await fetch(`${API_BASE_URL}/audio/status/${sessionId}`);
    
    if (response.ok) {
      return await handleResponse<any>(response);
    } else {
      console.log("API endpoint not available, using mock status");
      // Return mock status
      return {
        session_id: sessionId,
        status: "completed",
        message: "Audio processing completed (mock)",
        progress: 100,
        estimated_completion: null
      };
    }
  } catch (error) {
    console.log("Error connecting to API, using mock status", error);
    // Return mock status
    return {
      session_id: sessionId,
      status: "completed",
      message: "Audio processing completed (mock)",
      progress: 100,
      estimated_completion: null
    };
  }
}

// Mock function to get demo data for development
export function getDemoUserStatistics(): UserStatistics {
  return {
    user_id: "demo-user",
    days_analyzed: 30,
    total_speaking_time: 18240, // 5 hours and 4 minutes
    total_conversations: 42,
    average_metrics: {
      avg_filler_percentage: 4.2,
      avg_words_per_minute: 162,
      avg_vocabulary_diversity: 0.68,
      avg_clarity_score: 78,
      avg_confidence_score: 72
    },
    trend_data: {
      dates: Array.from({ length: 30 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() - (29 - i));
        return date.toISOString().split('T')[0];
      }),
      filler_percentage: Array.from({ length: 30 }, () => Math.random() * 8 + 2), // 2-10%
      words_per_minute: Array.from({ length: 30 }, () => Math.random() * 50 + 140), // 140-190 wpm
      confidence_score: Array.from({ length: 30 }, (_, i) => Math.min(100, 60 + i * 0.5 + Math.random() * 10)), // Increasing trend
      clarity_score: Array.from({ length: 30 }, (_, i) => Math.min(100, 65 + i * 0.4 + Math.random() * 10)), // Increasing trend
    }
  };
}

// Mock function to get demo analysis history
export function getDemoAnalysisHistory(): AnalysisResult[] {
  return Array.from({ length: 10 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - i);
    
    const fillerWords: Record<string, number> = {
      "um": Math.floor(Math.random() * 10 + 5),
      "uh": Math.floor(Math.random() * 8 + 3),
      "like": Math.floor(Math.random() * 15 + 8),
      "you know": Math.floor(Math.random() * 6 + 2),
      "sort of": Math.floor(Math.random() * 4 + 1),
    };
    
    const totalFillers = Object.values(fillerWords).reduce((sum, count) => sum + count, 0);
    const totalWords = Math.floor(Math.random() * 1000 + 1500);
    
    return {
      analysis_id: i + 1,
      date: date.toISOString().split('T')[0],
      metrics: {
        total_speaking_time_seconds: Math.floor(Math.random() * 1800 + 900), // 15-45 minutes
        total_conversations: Math.floor(Math.random() * 3 + 1),
        filler_word_count: totalFillers,
        filler_word_percentage: (totalFillers / totalWords) * 100,
        avg_words_per_minute: Math.floor(Math.random() * 40 + 140), // 140-180 wpm
        vocabulary_diversity_score: Math.random() * 0.3 + 0.5, // 0.5-0.8
        clarity_score: Math.floor(Math.random() * 20 + 65), // 65-85
        confidence_score: Math.floor(Math.random() * 25 + 60), // 60-85
        overall_rating: Math.floor(Math.random() * 20 + 70), // 70-90
        filler_words: fillerWords,
        total_words: totalWords,
        pace_variability: Math.random() * 20 + 5, // 5-25
      },
      suggestions: [
        {
          suggestion_id: i * 3 + 1,
          analysis_id: i + 1,
          suggestion_type: "filler_words",
          suggestion_text: `Try to reduce the use of "${Object.entries(fillerWords).sort((a, b) => b[1] - a[1])[0][0]}" by using strategic pauses instead.`,
          priority_level: 5,
          example_text: `When I was presenting the, ${Object.entries(fillerWords).sort((a, b) => b[1] - a[1])[0][0]}, quarterly results, I noticed a trend.`,
          improved_example: `When I was presenting the [pause] quarterly results, I noticed a trend.`,
          created_at: date.toISOString(),
        },
        {
          suggestion_id: i * 3 + 2,
          analysis_id: i + 1,
          suggestion_type: "pace",
          suggestion_text: "Your speaking pace varies significantly. Work on maintaining a more consistent pace for clarity.",
          priority_level: 3,
          created_at: date.toISOString(),
        },
        {
          suggestion_id: i * 3 + 3,
          analysis_id: i + 1,
          suggestion_type: "vocabulary",
          suggestion_text: "Expand your vocabulary by incorporating more precise terms when describing concepts.",
          priority_level: 2,
          created_at: date.toISOString(),
        }
      ]
    };
  });
}