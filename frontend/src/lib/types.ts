export interface User {
  user_id: number;
  username: string;
  email: string;
  device_id: string;
  created_at: string;
  settings?: any;
}

export interface SpeechSegment {
  segment_id: number;
  conversation_id: number;
  user_id: number;
  start_time: string;
  end_time: string;
  text_content: string;
  is_user_speaking: boolean;
  speaker_identification?: string;
  duration_seconds?: number;
  word_count?: number;
  created_at: string;
}

export interface Conversation {
  conversation_id: number;
  user_id: number;
  start_timestamp: string;
  end_timestamp: string;
  conversation_context?: string;
  participants_count?: number;
  total_duration_seconds?: number;
  created_at: string;
  speech_segments: SpeechSegment[];
}

export interface ImprovementSuggestion {
  suggestion_id: number;
  analysis_id: number;
  segment_id?: number;
  suggestion_type: string;
  suggestion_text: string;
  priority_level?: number;
  example_text?: string;
  improved_example?: string;
  created_at: string;
}

export interface AnalysisMetrics {
  total_speaking_time_seconds: number;
  total_conversations: number;
  filler_word_count: number;
  filler_word_percentage: number;
  avg_words_per_minute: number;
  vocabulary_diversity_score: number;
  clarity_score: number;
  confidence_score: number;
  overall_rating: number;
  filler_words?: Record<string, number>;
  total_words?: number;
  pace_variability?: number;
}

export interface AnalysisResult {
  analysis_id: number;
  date: string;
  metrics: AnalysisMetrics;
  suggestions: ImprovementSuggestion[];
}

export interface UserStatistics {
  user_id: string;
  days_analyzed: number;
  total_speaking_time: number;
  total_conversations: number;
  average_metrics: {
    avg_filler_percentage: number;
    avg_words_per_minute: number;
    avg_vocabulary_diversity: number;
    avg_clarity_score: number;
    avg_confidence_score: number;
  };
  trend_data: {
    dates: string[];
    filler_percentage: number[];
    words_per_minute: number[];
    confidence_score: number[];
    clarity_score: number[];
  };
}