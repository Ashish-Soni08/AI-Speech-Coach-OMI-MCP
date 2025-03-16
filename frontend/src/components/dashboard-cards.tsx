"use client";

import { UserStatistics, AnalysisResult } from "@/lib/types";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { formatTime } from "@/lib/utils";
import {
  Clock,
  MessageSquare,
  BarChart2,
  Activity,
  Zap,
  AlignJustify,
  BookOpen,
} from "lucide-react";

interface DashboardCardsProps {
  statistics: UserStatistics;
  latestAnalysis: AnalysisResult;
}

export function DashboardCards({ statistics, latestAnalysis }: DashboardCardsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {/* Total speaking time */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Speaking Time
          </CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {formatTime(statistics.total_speaking_time)}
          </div>
          <p className="text-xs text-muted-foreground">
            Total time across {statistics.total_conversations} conversations
          </p>
        </CardContent>
      </Card>

      {/* Filler words percentage */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Filler Words
          </CardTitle>
          <MessageSquare className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {statistics.average_metrics.avg_filler_percentage.toFixed(1)}%
          </div>
          <p className="text-xs text-muted-foreground">
            Average usage of filler words in speech
          </p>
        </CardContent>
      </Card>

      {/* Words per minute */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Speaking Pace
          </CardTitle>
          <BarChart2 className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {Math.round(statistics.average_metrics.avg_words_per_minute)} WPM
          </div>
          <p className="text-xs text-muted-foreground">
            Average words per minute (150-160 is optimal)
          </p>
        </CardContent>
      </Card>

      {/* Confidence score */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Confidence Score
          </CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {Math.round(statistics.average_metrics.avg_confidence_score)}/100
          </div>
          <p className="text-xs text-muted-foreground">
            Based on pace, fillers, and structure
          </p>
        </CardContent>
      </Card>

      {/* Second row */}
      <Card className="md:col-span-2">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle className="text-sm font-medium">
              Today's Performance
            </CardTitle>
            <CardDescription>
              Based on your most recent speech analysis
            </CardDescription>
          </div>
          <Zap className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="flex flex-col">
              <span className="text-xs text-muted-foreground">Filler Words</span>
              <span className="text-lg font-semibold">
                {latestAnalysis.metrics.filler_word_count}
              </span>
              <span className="text-xs text-muted-foreground">
                {(latestAnalysis.metrics.filler_word_percentage).toFixed(1)}% of speech
              </span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-muted-foreground">Words/Min</span>
              <span className="text-lg font-semibold">
                {latestAnalysis.metrics.avg_words_per_minute}
              </span>
              <span className="text-xs text-muted-foreground">
                {latestAnalysis.metrics.pace_variability && 
                  `±${Math.round(latestAnalysis.metrics.pace_variability)} variance`}
              </span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-muted-foreground">Rating</span>
              <span className="text-lg font-semibold">
                {Math.round(latestAnalysis.metrics.overall_rating)}/100
              </span>
              <span className="text-xs text-text-muted-foreground">
                Overall quality
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Vocabulary diversity */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Vocabulary
          </CardTitle>
          <BookOpen className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {(statistics.average_metrics.avg_vocabulary_diversity * 100).toFixed(0)}%
          </div>
          <p className="text-xs text-muted-foreground">
            Word variety score (higher is better)
          </p>
        </CardContent>
      </Card>

      {/* Clarity */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Clarity
          </CardTitle>
          <AlignJustify className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {Math.round(statistics.average_metrics.avg_clarity_score)}/100
          </div>
          <p className="text-xs text-muted-foreground">
            Speech structure and articulation
          </p>
        </CardContent>
      </Card>
    </div>
  );
}