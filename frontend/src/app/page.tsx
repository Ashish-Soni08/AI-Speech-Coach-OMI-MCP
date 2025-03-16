"use client";

import { useEffect, useState } from "react";
import { getUserStatistics, getUserHistory, getDemoUserStatistics, getDemoAnalysisHistory } from "@/lib/api";
import { UserStatistics, AnalysisResult } from "@/lib/types";
import { DashboardHeader } from "@/components/dashboard-header";
import { DashboardCards } from "@/components/dashboard-cards";
import { ProgressCharts } from "@/components/progress-charts";
import { SuggestionsPanel } from "@/components/suggestions-panel";

export default function DashboardPage() {
  const [statistics, setStatistics] = useState<UserStatistics | null>(null);
  const [history, setHistory] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from the API with fallback to mock data
    setLoading(true);
    
    // Define a demo user ID - in a real app this would come from authentication
    const userId = "demo-user";
    
    // Fetch user statistics and history in parallel
    Promise.all([
      getUserStatistics(userId),
      getUserHistory(userId, 10)
    ])
      .then(([statsData, historyData]) => {
        setStatistics(statsData);
        setHistory(historyData);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
        // Fallback to mock data
        setStatistics(getDemoUserStatistics());
        setHistory(getDemoAnalysisHistory());
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="flex flex-col items-center">
          <svg
            className="animate-spin h-12 w-12 text-primary mb-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <p className="text-xl font-medium">Loading your speech data...</p>
        </div>
      </div>
    );
  }

  if (!statistics || history.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="max-w-md mx-auto p-6 bg-card rounded-lg shadow-md">
          <h1 className="text-2xl font-bold mb-4">No Data Found</h1>
          <p className="mb-6">
            We don't have any speech data for you yet. Try uploading an audio
            recording or connecting your OMI device.
          </p>
          <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md">
            Upload Recording
          </button>
        </div>
      </div>
    );
  }

  // Get the most recent analysis for suggestions
  const latestAnalysis = history[0];

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Your Speech Dashboard</h1>
        
        {/* Key metrics cards */}
        <DashboardCards statistics={statistics} latestAnalysis={latestAnalysis} />
        
        {/* Progress charts */}
        <ProgressCharts statistics={statistics} className="mt-8" />
        
        {/* Improvement suggestions */}
        <SuggestionsPanel 
          suggestions={latestAnalysis.suggestions} 
          className="mt-8" 
        />
      </main>
    </div>
  );
}