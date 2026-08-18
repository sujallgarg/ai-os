import React from "react";
import { cn } from "@/lib/utils";

export interface StatProps {
  label: string;
  value: string | number;
  description?: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon?: React.ReactNode;
  className?: string;
}

export function Stat({
  label,
  value,
  description,
  change,
  changeType = "neutral",
  icon,
  className,
}: StatProps) {
  const changeColor = {
    positive: "text-emerald-700 bg-emerald-50 border-emerald-200",
    negative: "text-red-700 bg-red-50 border-red-200",
    neutral: "text-slate-600 bg-slate-100 border-slate-200",
  };

  return (
    <div
      className={cn(
        "bg-white rounded-2xl p-5 border border-slate-200/80 shadow-card hover:shadow-elevated transition-all duration-200",
        className
      )}
    >
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs font-semibold text-slate-500 tracking-tight">
          {label}
        </span>
        {icon && (
          <div className="w-8 h-8 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600">
            {icon}
          </div>
        )}
      </div>
      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-2xl font-bold text-slate-900 tracking-tight">
          {value}
        </span>
        {change && (
          <span
            className={cn(
              "text-[11px] font-semibold px-2 py-0.5 rounded-full border",
              changeColor[changeType]
            )}
          >
            {change}
          </span>
        )}
      </div>
      {description && (
        <p className="mt-1 text-xs text-slate-400 font-normal">{description}</p>
      )}
    </div>
  );
}
