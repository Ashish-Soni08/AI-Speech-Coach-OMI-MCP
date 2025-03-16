"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ModeToggle } from "@/components/mode-toggle";
import { 
  Mic, 
  Upload, 
  BarChart4,
  History,
  User,
  Menu,
} from "lucide-react";

export function DashboardHeader() {
  return (
    <header className="border-b">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Link href="/" className="flex items-center">
            <Mic className="h-6 w-6 mr-2" />
            <span className="text-xl font-bold">AI Speech Coach</span>
          </Link>
        </div>
        
        <nav className="hidden md:flex items-center gap-6">
          <Link 
            href="/" 
            className="text-sm font-medium flex items-center gap-1 transition-colors hover:text-primary"
          >
            <BarChart4 className="h-4 w-4" />
            Dashboard
          </Link>
          <Link 
            href="/history" 
            className="text-sm font-medium flex items-center gap-1 transition-colors hover:text-primary"
          >
            <History className="h-4 w-4" />
            History
          </Link>
          <Link 
            href="/upload" 
            className="text-sm font-medium flex items-center gap-1 transition-colors hover:text-primary"
          >
            <Upload className="h-4 w-4" />
            Upload
          </Link>
        </nav>
        
        <div className="flex items-center gap-4">
          <ModeToggle />
          <Button variant="outline" size="sm" className="hidden md:flex items-center gap-1">
            <User className="h-4 w-4 mr-1" />
            Account
          </Button>
          <Button variant="default" size="sm" className="hidden md:flex items-center gap-1">
            <Mic className="h-4 w-4 mr-1" />
            Record
          </Button>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}