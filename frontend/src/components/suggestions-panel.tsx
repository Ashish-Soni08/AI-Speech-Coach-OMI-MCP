"use client";

import { ImprovementSuggestion } from "@/lib/types";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import {
  Mic,
  Zap,
  MessageSquare,
  BookOpen,
  BarChart2,
  CheckCircle,
  AlertCircle
} from "lucide-react";

interface SuggestionsPanelProps {
  suggestions: ImprovementSuggestion[];
  className?: string;
}

export function SuggestionsPanel({ suggestions, className = "" }: SuggestionsPanelProps) {
  // Sort suggestions by priority level (higher first)
  const sortedSuggestions = [...suggestions].sort((a, b) => 
    (b.priority_level || 0) - (a.priority_level || 0)
  );

  // Get the icon for a suggestion type
  const getSuggestionIcon = (type: string) => {
    switch (type) {
      case "filler_words":
        return <MessageSquare className="h-5 w-5" />;
      case "pace":
      case "pace_consistency":
      case "pace_dynamics":
        return <BarChart2 className="h-5 w-5" />;
      case "vocabulary":
        return <BookOpen className="h-5 w-5" />;
      case "structure":
        return <CheckCircle className="h-5 w-5" />;
      case "confidence":
        return <Mic className="h-5 w-5" />;
      default:
        return <Zap className="h-5 w-5" />;
    }
  };

  // Get the color class for a suggestion based on priority
  const getPriorityClass = (priority?: number) => {
    if (!priority) return "bg-secondary text-secondary-foreground";
    
    if (priority >= 4) {
      return "bg-destructive/10 text-destructive border-destructive/20";
    } else if (priority >= 2) {
      return "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 border-yellow-500/20";
    } else {
      return "bg-green-500/10 text-green-600 dark:text-green-400 border-green-500/20";
    }
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Improvement Suggestions</CardTitle>
        <CardDescription>
          Personalized tips to help you become more articulate
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sortedSuggestions.map((suggestion) => (
            <div 
              key={suggestion.suggestion_id}
              className={`p-4 rounded-lg border ${getPriorityClass(suggestion.priority_level)}`}
            >
              <div className="flex gap-3">
                <div className="mt-0.5">
                  {getSuggestionIcon(suggestion.suggestion_type)}
                </div>
                <div className="flex-1">
                  <h4 className="font-medium mb-1">
                    {suggestion.suggestion_type.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </h4>
                  <p className="text-sm">{suggestion.suggestion_text}</p>
                  
                  {suggestion.example_text && suggestion.improved_example && (
                    <div className="mt-3 space-y-2">
                      <div className="text-xs font-medium">Example:</div>
                      <div className="grid grid-cols-1 gap-2 text-sm">
                        <div className="p-2 rounded bg-background border">
                          <span className="text-xs font-medium text-muted-foreground mr-2">Original:</span>
                          {suggestion.example_text}
                        </div>
                        <div className="p-2 rounded bg-background border">
                          <span className="text-xs font-medium text-muted-foreground mr-2">Improved:</span>
                          {suggestion.improved_example}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                {suggestion.priority_level && suggestion.priority_level >= 4 && (
                  <div className="mt-0.5">
                    <AlertCircle className="h-5 w-5 text-destructive" />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}