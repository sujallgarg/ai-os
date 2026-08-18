import React from "react";
import { cn } from "@/lib/utils";

export interface ProgressBarProps {
  value: number; // 0 to 100
  max?: number;
  className?: string;
  barClassName?: string;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  color?: "primary" | "emerald" | "amber" | "rose" | "indigo";
}

export function ProgressBar({
  value,
  max = 100,
  className,
  barClassName,
  size = "md",
  showLabel = false,
  color = "primary",
}: ProgressBarProps) {
  const percentage = Math.min(Math.max(Math.round((value / max) * 100), 0), 100);

  const sizeStyles = {
    sm: "h-1.5",
    md: "h-2",
    lg: "h-3",
  };

  const colorStyles = {
    primary: "bg-primary-600",
    emerald: "bg-emerald-500",
    amber: "bg-amber-500",
    rose: "bg-rose-500",
    indigo: "bg-indigo-600",
  };

  return (
    <div className={cn("w-full", className)}>
      {showLabel && (
        <div className="flex justify-between items-center text-xs text-slate-500 mb-1">
          <span>Progress</span>
          <span className="font-semibold text-slate-700">{percentage}%</span>
        </div>
      )}
      <div className={cn("w-full bg-slate-100 rounded-full overflow-hidden", sizeStyles[size])}>
        <div
          className={cn("h-full transition-all duration-500 ease-out rounded-full", colorStyles[color], barClassName)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
