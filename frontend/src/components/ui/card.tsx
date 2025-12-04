// src/components/ui/card.tsx
import * as React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          // Фон: белый
          "bg-white",
          // Радиус: 24px
          "rounded-[24px]",
          // Обводка: серая
          "border border-gray-200",
          // Отступы: p-6 (24px, кратно 8px)
          "p-6 md:p-8", 
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";

export const CardHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn("flex flex-col space-y-1.5", className)} {...props} />
);
export const CardContent = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn("p-0 pt-6", className)} {...props} />
);