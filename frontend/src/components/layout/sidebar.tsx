// src/components/layout/sidebar.tsx
import * as React from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, Calendar, Users, Settings, LogOut } from 'lucide-react';
import { cn } from "@/lib/utils";

interface NavItemProps {
    icon: React.ElementType;
    label: string;
    to: string;
}

const NavItem: React.FC<NavItemProps> = ({ icon: Icon, label, to }) => {
    const location = useLocation();
    const isActive = location.pathname === to;
    
    return (
        <Link 
            to={to} 
            className={cn(
                "flex items-center space-x-3 p-3 rounded-xl transition-colors duration-200 text-sm font-medium",
                // Неактивный текст: серый
                "text-gray-500",
                // Hover:
                "hover:bg-gray-100 hover:text-gray-900",
                // Активный фон: серый
                isActive && "bg-gray-100 text-gray-900"
            )}
        >
            {/* Иконки: контурные, 1.5px */}
            <Icon className="w-5 h-5 stroke-[1.5px]" /> 
            <span>{label}</span>
        </Link>
    );
};

export const Sidebar: React.FC = () => {
    const navigationItems = [
        { icon: Home, label: "Dashboard", to: "/" },
        { icon: Calendar, label: "Расписание", to: "/schedule" },
        { icon: Users, label: "Тренеры", to: "/coaches" },
        { icon: Settings, label: "Настройки", to: "/settings" },
    ];

    return (
        <div 
            className={cn(
                // Ширина 250px, фиксированная, показываем только на больших экранах
                "hidden lg:flex flex-col fixed top-0 left-0 h-full w-[250px] z-30", 
                // Фон: белый
                "bg-white",
                // Разделитель: серый
                "border-r border-gray-200"
            )}
        >
            {/* Логотип */}
            <div className="p-6 h-20 flex items-center">
                <h1 className="text-xl font-bold text-gray-900 select-none">
                    SPORT SCHOOL
                </h1>
            </div>

            {/* Навигация (Отступы p-4 = 16px) */}
            <nav className="flex flex-col p-4 space-y-2 flex-grow">
                {navigationItems.map((item) => (
                    <NavItem key={item.to} {...item} />
                ))}
            </nav>

            {/* Футер */}
            <div className="p-4 border-t border-gray-200">
                <NavItem icon={LogOut} label="Выйти" to="/logout" />
            </div>
        </div>
    );
};