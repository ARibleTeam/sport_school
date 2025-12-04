// src/pages/TrainerProfile.tsx
import * as React from "react";
import { MainLayout } from "../components/layout/mainlayout";
// Явные импорты
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { useParams, Link } from "react-router-dom"; 
import { ArrowLeft, User, Mail, Zap, Phone, Calendar, Clock, MapPin } from 'lucide-react'; 
import { cn } from "@/lib/utils";
import { getTrainerById, Trainer, Training, TrainerWithSchedule } from "@/lib/api";
import { useEffect, useState } from 'react';

// --- Моковые данные (дублируем, чтобы не зависеть от Trainers.tsx) ---
// ... (оставляем типы и моковые данные без изменений)
// Моковое расписание для тренера (для примера)
//const mockSchedule: Training[] = [
//    { id: 101, type: 'individual', title: "Анализ техники плавания", time: "09:00 - 10:30", location: "Бассейн 1", date: "Сегодня, 25 Мая" },
//    { id: 102, type: 'group', title: "Кардио и выносливость (Плавательный клуб)", time: "11:00 - 12:30", location: "Бассейн 1", date: "Сегодня, 25 Мая", participants: 15 },
//    { id: 103, type: 'individual', title: "Восстановительный массаж", time: "18:00 - 19:00", location: "Кабинет реабилитации", date: "Сегодня, 25 Мая" },
//    { id: 104, type: 'group', title: "Утренний заплыв", time: "07:00 - 08:30", location: "Бассейн 2", date: "Завтра, 26 Мая", participants: 25 },
//];
// --- Компонент Карточки Тренировки (без изменений) ---
const TrainingItem: React.FC<{ training: Training }> = ({ training }) => {
    const isGroup = training.type === 'group';
    
    return (
        <div className="flex justify-between items-center p-4 border-b border-gray-100 last:border-b-0">
            <div className="flex flex-col space-y-1">
                <h4 className="font-semibold text-gray-900">{training.title}</h4>
                <p className="flex items-center space-x-2 text-sm text-gray-500">
                    <Clock className="w-4 h-4 stroke-[1.5px]" />
                    <span>{training.time}</span>
                    <span className="text-gray-300">|</span>
                    <MapPin className="w-4 h-4 stroke-[1.5px]" />
                    <span>{training.location}</span>
                </p>
            </div>
            <div 
                className={cn(
                    "flex items-center space-x-1 p-2 rounded-full text-xs font-medium",
                    isGroup ? "bg-blue-100 text-blue-600" : "bg-amber-100 text-amber-600"
                )}
            >
                {isGroup ? <User className="w-4 h-4" /> : <User className="w-4 h-4" />}
                <span>{isGroup ? 'Группа' : 'Индивид.'}</span>
            </div>
        </div>
    );
};


const TrainerProfile: React.FC = () => {
    const { id } = useParams<{ id: string }>(); 
    const trainerId = Number(id);
    //const trainer = mockTrainers.find(t => t.id === 1);
    const [trainerData, setTrainerData] = useState<TrainerWithSchedule | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (trainerId) {
            setLoading(true);
            getTrainerById(trainerId)
                .then(data => {
                    setTrainerData(data);
                    setLoading(false);
                })
                .catch(error => {
                    console.error("Ошибка при загрузке тренера:", error);
                    setError("Не удалось загрузить данные тренера.");
                    setLoading(false);
                });
        }
    }, [trainerId]);

    // ... (код для обработки "Тренер не найден" остается без изменений)
    if (loading) {
        return (
            <MainLayout>
                <div className="p-12 text-center">
                    <h1 className="text-3xl font-bold mb-4">Загрузка...</h1>
                </div>
            </MainLayout>
        );
    }
    
    if (error) {
        return (
        <MainLayout>
                <div className="p-12 text-center">
                    <h1 className="text-3xl font-bold mb-4">{error}</h1>
                    <Link to="/coaches">
                        <Button variant="secondary">
                            Вернуться к списку
                        </Button>
            </Link>
                </div>
            </MainLayout>
    );
    }

    if (!trainerData) {
        return (
            <MainLayout>
                <div className="p-12 text-center">
                    <h1 className="text-3xl font-bold mb-4">Тренер не найден</h1>
                    <Link to="/coaches">
                        <Button variant="secondary">
                            Вернуться к списку
                        </Button>
                    </Link>
                </div>
            </MainLayout>
        );
    }

    const { trainer, schedule } = trainerData;

    // Группировка расписания по дням (остается без изменений)
    const scheduleByDay = schedule.reduce((acc, training) => {
        if (!acc[training.date]) {
            acc[training.date] = [];
        }
        acc[training.date].push(training);
        return acc;
    }, {} as Record<string, Training[]>);


    return (
        <MainLayout>
            {/* Кнопка назад */}
            <Link to="/coaches" className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium mb-6">
                <ArrowLeft className="w-5 h-5 mr-2" />
                Вернуться к тренерам
            </Link>

            {/* Заголовок (убрана кнопка Записаться) */}
            <div className="mb-8">
                <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900">
                    {trainer.full_name}
                </h1>
                {/* Кнопка "Записаться на тренировку" была удалена */}
            </div>

            {/* Вертикальный макет (без lg:grid-cols-3) */}
            <div className="space-y-8"> {/* Убираем grid-cols, используем space-y */}

                {/* Блок Профиля (был lg:col-span-1) */}
                <Card>
                    <h2 className="text-2xl font-semibold mb-4 text-gray-900">Профиль</h2>
                    <div className="flex flex-col space-y-3">
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Zap className="w-5 h-5 text-blue-500" />
                            <span className="font-medium">Специализация:</span>
                            <span>{trainer.specialization.join(', ')}</span>
                        </div>
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Calendar className="w-5 h-5 text-blue-500" />
                            <span className="font-medium">Опыт:</span>
                            <span>{trainer.experience_years} лет</span>
                        </div>
                        <div className="flex items-center space-x-3 text-gray-700">
                            <Mail className="w-5 h-5 text-blue-500" />
                            <span className="font-medium">Email:</span>
                            <span>{trainer.email}</span>
                        </div>
                        {/*<div className="flex items-center space-x-3 text-gray-700">
                            <Phone className="w-5 h-5 text-blue-500" />
                            <span className="font-medium">Телефон:</span>
                            <span>{trainer.phone}</span>
                        </div>*/}
                    </div>
                </Card>

                {/* Блок О тренере */}
                <Card>
                    <h2 className="text-2xl font-semibold mb-4 text-gray-900">О тренере</h2>
                    <p className="text-gray-600">
                        {trainer.bio}
                    </p>
                </Card>

                {/* Блок Расписания (был lg:col-span-2) */}
                <Card>
                    <h2 className="text-2xl font-semibold mb-4 text-gray-900">Ближайшее расписание</h2>
                    <div className="space-y-4">
                        {Object.entries(scheduleByDay).map(([date, trainings]) => (
                            <div key={date}>
                                <h3 className="text-lg font-semibold text-gray-900 border-b pb-2 mb-2">
                                    {date}
                                </h3>
                                <div className="divide-y divide-gray-100">
                                    {trainings.map(training => (
                                        <TrainingItem key={training.id} training={training} />
                                    ))}
                                </div>
                            </div>
                        ))}
                        {schedule.length === 0 && (
                            <p className="text-gray-500">
                                На ближайшие дни расписание отсутствует.
                            </p>
                        )}
                    </div>
                </Card>
            </div>
        </MainLayout>
    );
};

export default TrainerProfile;