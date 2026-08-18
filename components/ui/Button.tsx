import React from "react";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger" | "soft";
  size?: "sm" | "md" | "lg" | "icon";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:opacity-50 disabled:pointer-events-none disabled:cursor-not-allowed select-none";

    const variantStyles = {
      primary:
        "bg-primary-600 hover:bg-primary-700 text-white shadow-sm hover:shadow active:bg-primary-800",
      secondary:
        "bg-slate-900 hover:bg-slate-800 text-white shadow-sm active:bg-slate-950",
      outline:
        "border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 hover:text-slate-900 active:bg-slate-100",
      soft:
        "bg-primary-50 hover:bg-primary-100 text-primary-700 active:bg-primary-200/70",
      ghost:
        "hover:bg-slate-100 text-slate-600 hover:text-slate-900 active:bg-slate-200/60",
      danger:
        "bg-red-600 hover:bg-red-700 text-white shadow-sm active:bg-red-800",
    };

    const sizeStyles = {
      sm: "text-xs px-2.5 py-1.5 rounded-lg gap-1.5",
      md: "text-sm px-3.5 py-2 rounded-xl gap-2",
      lg: "text-base px-5 py-2.5 rounded-xl gap-2.5",
      icon: "h-9 w-9 rounded-xl p-0",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin text-current" />
        ) : (
          leftIcon
        )}
        {children}
        {!isLoading && rightIcon}
      </button>
    );
  }
);

Button.displayName = "Button";
