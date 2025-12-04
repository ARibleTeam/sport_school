// src/components/layout/mainlayout.tsx - Обновленный код (Убрана кнопка Выйти)
import * as React from "react";
import { Sidebar } from "./sidebar";
import { MobileSidebar } from "./mobile-sidebar";
// Удален импорт Button, LogOut и Link/useNavigate, так как они больше не нужны в Header
import { Bell, Menu, X } from 'lucide-react'; 
import { cn } from "@/lib/utils";
// import { Link, useNavigate } from "react-router-dom"; // Удалены

interface MainLayoutProps {
    children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

    return (
        // Основной фон: светлый
        <div className="min-h-screen bg-white">
            <Sidebar />

            {/* Main Content Area: Сдвиг на 250px только на больших экранах */}
            <div className="lg:ml-[250px]">

                {/* Header (Top Bar) */}
                <header 
                    className={cn(
                        "h-20 flex items-center justify-between p-4 md:px-8 sticky top-0 z-20",
                        "border-b border-gray-200",
                        "bg-white" 
                    )}
                >
                    {/* H1 Title Placeholder */}
                    <div className="hidden lg:block text-xl font-bold text-gray-900 opacity-0"> 
                        {/* Невидимый элемент для выравнивания */}
                    </div>

                    {/* Мобильное меню и заголовок */}
                    <div className="lg:hidden flex items-center space-x-4">
                        <button 
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} 
                            className="text-gray-900 p-2 rounded-lg hover:bg-gray-100"
                        >
                            {isMobileMenuOpen ? <X className="w-6 h-6 stroke-[1.5px]" /> : <Menu className="w-6 h-6 stroke-[1.5px]" />}
                        </button>
                        <h2 className="text-xl font-bold text-gray-900">
                             SPORT SCHOOL
                        </h2>
                    </div>

                    {/* Правая сторона: Уведомления (осталась только кнопка Bell) */}
                    <div className="flex items-center space-x-4">
                        <button className="text-gray-500 hover:text-gray-900 transition-colors">
                             <Bell className="w-6 h-6 stroke-[1.5px]" />
                        </button>
                        {/* Кнопка "Выйти" была здесь, теперь удалена */}
                    </div>
                </header>

                {/* Content Area */}
                <main className="p-4 md:p-8">
                    {children}
                </main>
            </div>
            
            {/* Mobile Sidebar */}
            <MobileSidebar 
                isOpen={isMobileMenuOpen} 
                onClose={() => setIsMobileMenuOpen(false)} 
            />
        </div>
    );
};