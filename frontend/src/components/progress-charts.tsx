"use client";

import { UserStatistics } from "@/lib/types";
import { 
  Card, 
  CardContent,
  CardDescription,
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar
} from "recharts";

interface ProgressChartsProps {
  statistics: UserStatistics;
  className?: string;
}

export function ProgressCharts({ statistics, className = "" }: ProgressChartsProps) {
  // Format the data for the charts
  const chartsData = statistics.trend_data.dates.map((date, index) => ({
    date,
    fillerPercentage: statistics.trend_data.filler_percentage[index],
    wpm: statistics.trend_data.words_per_minute[index],
    confidence: statistics.trend_data.confidence_score[index],
    clarity: statistics.trend_data.clarity_score[index],
  }));

  // Get just the dates for display (show every 5 days)
  const filteredDates = chartsData.filter((_, i) => i % 5 === 0 || i === chartsData.length - 1);

  return (
    <div className={`grid gap-4 md:grid-cols-2 ${className}`}>
      {/* Filler Words Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Filler Word Usage</CardTitle>
          <CardDescription>
            Percentage of filler words in your speech over time
          </CardDescription>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartsData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 25,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                ticks={filteredDates.map(d => d.date)}
                angle={-45}
                textAnchor="end"
                className="text-xs"
              />
              <YAxis unit="%" domain={[0, 10]} className="text-xs" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: "hsl(var(--card))",
                  borderColor: "hsl(var(--border))",
                  color: "hsl(var(--foreground))"
                }}
                formatter={(value: any) => [`${value.toFixed(1)}%`, "Filler Words"]}
              />
              <Line
                type="monotone"
                dataKey="fillerPercentage"
                name="Filler Words"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Words Per Minute Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Speaking Pace</CardTitle>
          <CardDescription>
            Words per minute over time (ideal range: 140-180 WPM)
          </CardDescription>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartsData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 25,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                ticks={filteredDates.map(d => d.date)}
                angle={-45}
                textAnchor="end"
                className="text-xs"
              />
              <YAxis domain={[100, 200]} unit=" WPM" className="text-xs" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: "hsl(var(--card))",
                  borderColor: "hsl(var(--border))",
                  color: "hsl(var(--foreground))"
                }}
                formatter={(value: any) => [`${Math.round(value)} WPM`, "Speaking Pace"]}
              />
              <Line
                type="monotone"
                dataKey="wpm"
                name="Words per Minute"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Scores Comparison */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>Speaking Performance</CardTitle>
          <CardDescription>
            Your confidence and clarity scores over time
          </CardDescription>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartsData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 25,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                ticks={filteredDates.map(d => d.date)}
                angle={-45}
                textAnchor="end"
                className="text-xs"
              />
              <YAxis domain={[0, 100]} className="text-xs" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: "hsl(var(--card))",
                  borderColor: "hsl(var(--border))",
                  color: "hsl(var(--foreground))"
                }}
                formatter={(value: any, name: string) => [
                  `${Math.round(value)}/100`, 
                  name === "confidence" ? "Confidence" : "Clarity"
                ]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="confidence"
                name="Confidence"
                stroke="#9333ea"
                strokeWidth={2}
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="clarity"
                name="Clarity"
                stroke="#2563eb"
                strokeWidth={2}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}