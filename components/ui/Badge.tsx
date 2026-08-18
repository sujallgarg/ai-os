import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "neutral" | "primary" | "success" | "warning" | "error" | "purple" | "outline";
  size?: "sm" | "md";
  dot?: boolean;
}

export function Badge({
  className,
  variant = "neutral",
  size = "md",
  dot = false,
  children,
  ...props
}: BadgeProps) {
  const variantStyles = {
    neutral: "bg-slate-100 text-slate-700 border-slate-200",
    primary: "bg-primary-50 text-primary-700 border-primary-200/80",
    success: "bg-emerald-50 text-emerald-700 border-emerald-200/80",
    warning: "bg-amber-50 text-amber-800 border-amber-200/80",
    error: "bg-red-50 text-red-700 border-red-200/80",
    purple: "bg-purple-50 text-purple-700 border-purple-200/80",
    outline: "bg-white text-slate-600 border-slate-200",
  };

  const dotColors = {
    neutral: "bg-slate-400",
    primary: "bg-primary-500",
    success: "bg-emerald-500",
    warning: "bg-amber-500",
    error: "bg-red-500",
    purple: "bg-purple-500",
    outline: "bg-slate-400",
  };

  const sizeStyles = {
    sm: "text-[11px] px-2 py-0.5 rounded-md gap-1 font-medium",
    md: "text-xs px-2.5 py-1 rounded-lg gap-1.5 font-medium",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center border select-none transition-colors",
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {dot && (
        <span
          className={cn(
            "w-1.5 h-1.5 rounded-full flex-shrink-0",
            dotColors[variant]
          )}
        />
      )}
      {children}
    </span>
  );
}
