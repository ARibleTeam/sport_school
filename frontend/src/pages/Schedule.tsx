// src/pages/Schedule.tsx

import * as React from "react";
import { MainLayout } from "../components/layout/mainlayout.tsx";
import { Card, CardHeader, CardContent } from "../components/ui/card";
import { Users as GroupIcon, User as UserIcon, Calendar, Clock, MapPin } from 'lucide-react'; 
import { cn } from "@/lib/utils"; // Предполагаем, что utils.ts доступен
import { User, Training, getSchedule } from "@/lib/api";
import { Button } from "@/components/ui/button"; // Импортируем компонент Button
import { Link } from "react-router-dom"; // Импортируем Link
import { useEffect, useState } from 'react';

// --- Моковые данные ---
// --- Компонент карточки тренировки ---
const ScheduleCard: React.FC<{ training: Training; user: User | null }> = ({ training, user }) => {
    const isGroup = training.type === 'group';
    
    // Используем акцентный цвет для иконок и заголовка
    const iconColorClass = isGroup ? "text-blue-400" : "text-amber-400";
    
    return (
        <Card className="p-6 transition-transform hover:shadow-lg hover:scale-[1.01] duration-300">
            <div className="flex justify-between items-start mb-4">
                {/* H3: Заголовок тренировки */}
                <h3 className="text-xl font-semibold text-gray-900">
                    {training.title}
                </h3>
                
                {/* Тип тренировки (тег-пилюля) */}
                <div 
                    className={cn(
                        "flex items-center space-x-1 p-2 rounded-full text-xs font-semibold",
                        "bg-gray-100 text-gray-900"
                    )}
                >
                    {isGroup ? <GroupIcon className="w-4 h-4" /> : <UserIcon className="w-4 h-4" />}
                    <span>{isGroup ? 'Групповая' : 'Индивидуальная'}</span>
                </div>
            </div>

            <div className="space-y-3 text-sm">
                <p className="flex items-center space-x-3 text-gray-500">
                    <Clock className={cn("w-4 h-4 stroke-[1.5px]", iconColorClass)} />
                    <span className="font-medium text-gray-900">{training.time}</span>
                    <span>с тренером {training.coach}</span>
                </p>

                <p className="flex items-center space-x-3 text-gray-500">
                    <MapPin className={cn("w-4 h-4 stroke-[1.5px]", iconColorClass)} />
                    <span>Место: {training.location}</span>
                </p>

                {isGroup && (
                    <p className="flex items-center space-x-3 text-gray-500">
                        <GroupIcon className={cn("w-4 h-4 stroke-[1.5px]", iconColorClass)} />
                        <span>Участники: {training.participants} человек</span>
                    </p>
                )}
            </div>
            {/* Кнопка "Изменить" (только для админов) */}
            {user?.isAdmin && (
                <div className="mt-4 justify-center">
                    <Link to={`/admin/schedule/edit/${training.id}`}>
                        <Button variant="secondary" className="max-w-xl w-full ">
                            Изменить
                        </Button>
                    </Link>
                </div>
            )}
        </Card>
    );
};

interface ScheduleProps {
    user: User | null;
}

const Schedule: React.FC<ScheduleProps> = ({ user }) => {
    // Состояние для переключения между расписаниями
    const [viewMode, setViewMode] = React.useState<string>('individual');
    const [schedule, setSchedule] = useState<Training[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        setLoading(true);
        getSchedule({ type: viewMode === 'individual' ? 'individual' : 'group' })
            .then(data => {
                setSchedule(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Ошибка при загрузке расписания:", error);
                setError("Не удалось загрузить расписание.");
                setLoading(false);
            });
    }, [viewMode]);
    //const filteredSchedule = mockSchedule.filter(t =>
    //    viewMode === 'individual' ? t.type === 'individual' : t.type === 'group'
    //);

    const scheduleByDay = schedule.reduce((acc, training) => {
        if (!acc[training.date]) {
            acc[training.date] = [];
        }
        acc[training.date].push(training);
        return acc;
    }, {} as Record<string, Training[]>);

    // Кнопка для переключения табов (переиспользование стиля из Index.tsx)
    const TabButton: React.FC<{ tab: 'individual' | 'group', current: string, onClick: () => void, children: React.ReactNode }> = ({ tab, current, onClick, children }) => (
        <button 
            onClick={onClick}
            className={cn(
                "py-3 px-6 text-lg font-semibold rounded-xl transition-colors duration-150 flex-1",
                // Активное состояние: фон серый
                current === tab 
                    ? "bg-gray-100 text-gray-900" 
                    // Неактивное состояние: второстепенный цвет
                    : "text-gray-500 hover:bg-gray-50"
            )}
        >
            {children}
        </button>
    );

    return (
        <MainLayout>
            {/* H1 Заголовок: Крупный, жирный */}
            <h1 className="text-4xl md:text-5xl font-extrabold mb-8 md:mb-12 text-gray-900">
                Просмотр расписания
            </h1>

            {/* Кнопка "Добавить тренировку" (только для админов) */}
            {user?.isAdmin && (
                <div className="mb-8">
                    <Link to="/admin/schedule/new">
                        <Button>
                            Добавить тренировку
                        </Button>
                    </Link>
                </div>
            )}

            {/* Блок переключения режима */}
            <div className="flex justify-between items-center mb-10">
                <div className="flex p-1 bg-white border border-gray-200 rounded-xl max-w-lg w-full">
                    <TabButton tab="individual" current={viewMode} onClick={() => setViewMode('individual')}>
                        <UserIcon className="w-5 h-5 mr-2 stroke-[1.5px]" />
                        Индивидуальное
                    </TabButton>
                    <TabButton tab="group" current={viewMode} onClick={() => setViewMode('group')}>
                        <GroupIcon className="w-5 h-5 mr-2 stroke-[1.5px]" />
                        Групповое
                    </TabButton>
                </div>
            </div>

            {loading ? (
                <Card className="text-center p-12">
                    <p className="text-gray-500">Загрузка расписания...</p>
                </Card>
            ) : error ? (
                <Card className="text-center p-12">
                    <p className="text-red-500">{error}</p>
                </Card>
            ) : (
                /* Основная сетка расписания (Отступы 8px * 4 = 32px) */
                <div className="space-y-8">
                    {Object.keys(scheduleByDay).length === 0 ? (
                        <Card className="text-center p-12">
                            <p className="text-gray-500">
                                На данный момент расписание в режиме "{viewMode === 'individual' ? 'Индивидуальное' : 'Групповое'}" отсутствует.
                            </p>
                        </Card>
                    ) : (
                        Object.entries(scheduleByDay).map(([date, trainings]) => (
                            <div key={date}>
                            {/* Заголовок дня: H2, полужирный */}
                            <h2 className="text-2xl font-semibold mb-6 flex items-center space-x-3 text-gray-900">
                                <Calendar className="w-6 h-6 stroke-[1.5px] text-gray-500" />
                                <span>{date}</span>
                            </h2>
                            
                            {/* Сетка для карточек: 2 колонки на десктопе, gap-6 (24px) */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-full">
                                {trainings.map(training => (
                                        <ScheduleCard key={training.id} training={training} user={user} />
                                ))}
                            </div>
                        </div>
                    ))
                )}
            </div>
            )}
        </MainLayout>
    );
};

export default Schedule;