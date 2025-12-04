// src/components/ui/input.tsx
import * as React from "react";
import { cn } from "@/lib/utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  // Вы можете добавить варианты (variant) для разных стилей,
  // но пока сделаем один стандартный, чистый стиль.
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-12 w-full rounded-xl border border-gray-300 bg-white px-4 py-2 text-base shadow-sm transition-colors duration-200",
          "placeholder:text-gray-400", // Стиль для плейсхолдера
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-0", // Фокус
          "disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";