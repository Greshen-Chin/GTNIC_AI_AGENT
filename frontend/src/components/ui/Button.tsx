import React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "destructive" | "secondary" | "outline" | "ghost" | "emerald";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "secondary",
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
    const sizeClasses = {
      sm: "h-8 px-3 text-xs font-mono",
      md: "h-9 px-4 text-xs font-mono font-medium",
      lg: "h-11 px-6 text-sm font-mono font-semibold",
    };

    const variantClasses = {
      primary:
        "bg-cyan-600 hover:bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.35)] border border-cyan-400/40 active:translate-y-0.5",
      emerald:
        "bg-emerald-600 hover:bg-emerald-500 text-emerald-950 font-bold shadow-[0_0_18px_rgba(16,185,129,0.45)] border border-emerald-400 active:translate-y-0.5",
      destructive:
        "bg-rose-900/60 hover:bg-rose-800/80 text-rose-200 border border-rose-500/50 shadow-[0_0_15px_rgba(244,63,94,0.3)] active:translate-y-0.5",
      secondary:
        "bg-slate-900 hover:bg-slate-800/90 text-slate-200 border border-slate-700/80 hover:border-slate-600 shadow-sm active:translate-y-0.5",
      outline:
        "bg-transparent hover:bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700 active:translate-y-0.5",
      ghost:
        "bg-transparent hover:bg-slate-900/80 text-slate-400 hover:text-slate-100 border border-transparent",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-md transition-all duration-150 select-none focus:outline-none focus:ring-2 focus:ring-emerald-500/40 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none cursor-pointer",
          sizeClasses[size],
          variantClasses[variant],
          className
        )}
        {...props}
      >
        {isLoading ? (
          <svg
            className="animate-spin h-3.5 w-3.5 text-current"
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
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
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
