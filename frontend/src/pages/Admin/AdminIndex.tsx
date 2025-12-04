// src/pages/Admin/AdminIndex.tsx

import React from "react";
import { MainLayout } from "../../components/layout/mainlayout";
import { Card } from "../../components/ui/card";
import { Link } from "react-router-dom";
import { Users, Calendar } from 'lucide-react';
import { User } from "@/lib/api";

// --- Моковые данные для админа ----
const mockAdminStats = {
    totalUsers: 150,
    activeTrainers: 25,
    scheduledTrainings: 80,
};

// Компонент-блок для информации/ссылок
const InfoBlock: React.FC<{ icon: React.ReactNode, title: string, subtitle: string, color: string, linkTo?: string }> = ({ icon, title, subtitle, color, linkTo }) => {
    const content = (
        <Card className="flex flex-col items-start justify-center p-6 hover:shadow-lg hover:bg-gray-50 transition-all duration-200 cursor-pointer">
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

interface AdminIndexProps {
    user: User | null;
}

const AdminIndex: React.FC<AdminIndexProps> = ({ user }) => {
    return (
        <MainLayout>
            <div className="space-y-10">
                {/* Секция 1: Приветствие */}
                <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-12">
                    Панель администратора: {user?.name}
                </h1>

                {/* Секция 2: Уникальная информация (3 блока) */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    <InfoBlock
                        icon={<Users className="w-6 h-6 text-white" />}
                        title={mockAdminStats.totalUsers.toString()}
                        subtitle="Общее количество спортсменов"
                        color="bg-blue-600"
                        linkTo={undefined}
                    />
                    <InfoBlock
                        icon={<Calendar className="w-6 h-6 text-white" />}
                        title={mockAdminStats.activeTrainers.toString()}
                        subtitle="Количество активных тренеров"
                        color="bg-green-600"
                        linkTo={undefined}
                    />
                    <InfoBlock
                        icon={<Calendar className="w-6 h-6 text-white" />}
                        title={mockAdminStats.scheduledTrainings.toString()}
                        subtitle="Запланировано тренировок на неделю"
                        color="bg-amber-600"
                        linkTo={undefined}
                    />
                </div>

                {/* Секция 3: Быстрые действия */}
                <Card className="p-8 border-l-4 border-green-600 shadow-lg">
                    <h2 className="text-3xl font-bold mb-4 text-gray-900">Быстрые действия</h2>
                    <div className="space-y-4">
                        <Link to="/admin/users" className="flex items-center text-blue-600 hover:text-blue-700 font-semibold transition-colors">
                            <Users className="w-5 h-5 mr-2" />
                            Управление пользователями
                        </Link>
                        <Link to="/admin/trainers" className="flex items-center text-blue-600 hover:text-blue-700 font-semibold transition-colors">
                            <Users className="w-5 h-5 mr-2" />
                            Управление тренерами
                        </Link>
                        <Link to="/admin/schedule/new" className="flex items-center text-blue-600 hover:text-blue-700 font-semibold transition-colors">
                            <Calendar className="w-5 h-5 mr-2" />
                            Создать тренировку
                        </Link>
                    </div>
                </Card>
            </div>
        </MainLayout>
    );
};

export default AdminIndex;