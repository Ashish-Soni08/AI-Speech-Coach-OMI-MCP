# AI Speech Coach Dashboard

A frontend dashboard for the AI Speech Coach built with Next.js and shadcn/ui.

## Features

- **Modern Tech Stack**: Next.js, TypeScript, Tailwind CSS, and shadcn/ui components
- **Responsive Design**: Fully responsive dashboard that works on mobile and desktop
- **Dark Mode Support**: Toggle between light and dark themes
- **Interactive Visualizations**: Charts for tracking progress over time
- **API Integration**: Connects to the AI Speech Coach API for real-time data

## Overview

This dashboard provides a user interface for the AI Speech Coach backend. It displays speech analysis results, shows trends over time, and offers improvement suggestions.

Key visualization components include:
- Summary metrics cards
- Historical performance charts
- Personalized improvement suggestions

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Environment Variables

Create a `.env.local` file with the following variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Project Structure

- `src/app` - Next.js app router pages
- `src/components` - React components
- `src/components/ui` - shadcn/ui components
- `src/lib` - Utility functions and types
- `public` - Static assets

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Create a production build
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint

## API Integration

The dashboard connects to the AI Speech Coach API to fetch:
- User statistics and historical data
- Analysis results for speech recordings
- Improvement suggestions

In development mode, the dashboard uses mock data to simulate the API.