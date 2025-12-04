// src/pages/Index.tsx

import React from "react";
import { MainLayout } from "../components/layout/mainlayout";
import { Card } from "../components/ui/card";
import { Link } from "react-router-dom";
import { Clock, Users, Zap, ArrowRight, TrendingUp, Trophy, ListChecks } from 'lucide-react';
import { cn } from "@/lib/utils";
import { User } from "@/lib/api";

// --- Моковые данные ----
const mockNextTraining = {
    title: "Общая физическая подготовка (ОФП)",
    coach: "Елена Кузнецова",
    time: "СЕГОДНЯ, 11:00 - 12:30",
    location: "Зал №2",
    type: "Групповая",
};

const mockStats = {
    nextWeekLoad: 8,
};

// Компонент-блок для информации/ссылок
const InfoBlock: React.FC<{ icon: React.ReactNode, title: string, subtitle: string, color: string, linkTo?: string }> = ({ icon, title, subtitle, color, linkTo }) => {
    const content = (
        <Card className={cn(
            "flex flex-col items-start justify-center p-6",
            linkTo ? "hover:shadow-lg hover:bg-gray-50 transition-all duration-200 cursor-pointer" : "bg-gray-50 border-gray-200"
        )}>
            <div className={`p-3 rounded-full mb-4 ${color}`}>
                {icon}
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-1">{title}</h2>
            <p className="text-sm text-gray-600 mt-2">
                {subtitle}
            </p>
        </Card>
    );

    return linkTo ? <Link to={linkTo} className="block">{content}</Link> : content;
};

interface IndexProps {
    user: User | null;
}

const Index: React.FC<IndexProps> = ({ user }) => {

    return (
        <MainLayout>
            <div className="space-y-10">
                {/* Секция 1: Приветствие */}
                <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-12">
                    Добро пожаловать, {user?.name}!
                </h1>

                {/* Секция 2: Уникальная информация (3 блока) */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Блок 1: Нагрузка */}
                    <InfoBlock
                        icon={<Clock className="w-6 h-6 text-white" />}
                        title={mockStats.nextWeekLoad + " ч."}
                        subtitle="Нагрузка на следующую неделю"
                        color="bg-green-600"
                        linkTo={undefined}
                    />

                    {/* Блок 2: Достижения */}
                    <InfoBlock
                        icon={<Trophy className="w-6 h-6 text-white" />}
                        title="Достижения"
                        subtitle="Ваши лучшие результаты"
                        color="bg-amber-600"
                        linkTo="/achievements"
                    />

                    {/* Блок 3: История посещений */}
                    <InfoBlock
                        icon={<ListChecks className="w-6 h-6 text-white" />}
                        title="История посещений"
                        subtitle="Ваши последние посещения"
                        color="bg-blue-600"
                        linkTo="/attendance"
                    />
                </div>

                {/* Секция 3: Следующая тренировка / Быстрые действия */}
                <Link to="/schedule" className="block">
                    <Card
                        className={cn(
                            "p-8 border-l-4 border-blue-600 shadow-lg",
                            "hover:shadow-xl hover:bg-gray-50 transition-all duration-200 cursor-pointer"
                        )}
                    >
                        <h2 className="text-3xl font-bold mb-4 text-gray-900">
                            Ваша следующая тренировка
                        </h2>
                        <div className="flex flex-col md:flex-row md:items-center justify-between space-y-4 md:space-y-0">
                            <div className="space-y-2">
                                <p className="text-2xl font-semibold text-blue-600">{mockNextTraining.title}</p>

                                <p className="flex items-center space-x-3 text-gray-600">
                                    <Clock className="w-5 h-5" />
                                    <span className="font-medium text-gray-900">{mockNextTraining.time}</span>
                                </p>
                                <p className="flex items-center space-x-3 text-gray-600">
                                    <Users className="w-5 h-5" />
                                    <span>Тренер: {mockNextTraining.coach}</span>
                                </p>
                                <p className="flex items-center space-x-3 text-gray-600">
                                    <Zap className="w-5 h-5" />
                                    <span>Тип: {mockNextTraining.type}</span>
                                </p>
                            </div>
                            {/* Иконка для наглядности */}
                            <ArrowRight className="w-8 h-8 text-blue-500 min-w-8 hidden md:block" />
                        </div>
                    </Card>
                </Link>
            </div>
        </MainLayout>
    );
};

export default Index;