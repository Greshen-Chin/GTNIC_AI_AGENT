import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "destructive" | "secondary" | "outline" | "ghost" | "emerald";
  size?: "sm" | "md" | "lg" | "xl";
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
      sm: "h-7 px-2.5 text-[11px] font-mono gap-1.5",
      md: "h-9 px-3.5 text-xs font-mono font-medium gap-2",
      lg: "h-11 px-5 text-xs font-mono font-semibold gap-2.5",
      xl: "h-12 px-6 text-sm font-mono font-bold gap-3",
    };

    const variantClasses = {
      primary:
        "bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold shadow-sm border border-emerald-400/80 active:scale-[0.97]",
      emerald:
        "bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold shadow-sm border border-emerald-400 active:scale-[0.97]",
      destructive:
        "bg-rose-950/70 hover:bg-rose-900/90 text-rose-200 border border-rose-600/50 shadow-sm active:scale-[0.97]",
      secondary:
        "bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-800 hover:border-slate-700 shadow-sm active:scale-[0.97]",
      outline:
        "bg-transparent hover:bg-slate-900/60 text-slate-300 border border-slate-800 hover:border-slate-700 active:scale-[0.97]",
      ghost:
        "bg-transparent hover:bg-slate-800/60 text-slate-400 hover:text-slate-200 border border-transparent active:scale-[0.97]",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          "inline-flex items-center justify-center rounded-md transition-all duration-150 select-none",
          "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-500/60",
          "disabled:opacity-45 disabled:cursor-not-allowed disabled:pointer-events-none cursor-pointer",
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
