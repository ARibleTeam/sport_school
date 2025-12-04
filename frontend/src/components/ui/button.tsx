// src/components/ui/button.tsx
import * as React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", children, ...props }, ref) => {

    const baseClasses = "h-12 px-6 rounded-xl text-base font-semibold transition-colors duration-200 disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2";

    const variantClasses = {
      // Primary: Синий фон, белый текст
      primary: cn(
        "bg-blue-600 text-white", 
        "hover:bg-blue-700", 
        "focus-visible:ring-blue-500"
      ),
      // Secondary: Обводка
      secondary: cn(
        "border border-gray-300 text-gray-900",
        "bg-transparent hover:bg-gray-50"
      ),
      // Ghost: Для табов
      ghost: cn("hover:bg-gray-100 text-gray-900"),
    };

    return (
      <button
        ref={ref}
        className={cn(baseClasses, variantClasses[variant], className)}
        {...props}
      >
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";