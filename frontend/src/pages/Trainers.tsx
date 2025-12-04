// src/pages/Trainers.tsx
import * as React from "react";
import { MainLayout } from "../components/layout/mainlayout";
// Явные импорты
import { Card } from "../components/ui/card";
import { Calendar, User, Mail, Zap, ChevronRight } from 'lucide-react';
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom"; // Для перехода на профиль тренера
import { getTrainers, Trainer } from "@/lib/api"; // Импортируем getTrainers

// --- Компонент Карточки Тренера ---
const TrainerCard: React.FC<{ trainer: Trainer }> = ({ trainer }) => {
    return (
        <Card className="flex flex-col h-full hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center space-x-4 pb-4 border-b border-gray-100">
                {/* Аватар (Заглушка) */}
                <div className="flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full text-blue-600">
                    <User className="w-8 h-8 stroke-[1.5px]" />
                </div>

                <div>
                    <h3 className="text-xl font-bold text-gray-900">{trainer.full_name}</h3>
                    <p className="flex items-center text-sm text-gray-500">
                        <Zap className="w-4 h-4 mr-1 text-blue-500" />
                        {trainer.specialization[0]}
                    </p> 
                </div>
            </div>

            <div className="pt-4 flex-grow space-y-3 text-sm">
                <p className="text-gray-600 line-clamp-2">{trainer.bio}</p>

                {/* Email */}
                <p className="flex items-center space-x-2 text-gray-500">
                    <Mail className="w-4 h-4 stroke-[1.5px]" />
                    <span>{trainer.email}</span>
                </p>

                {/* Кнопка Просмотра Расписания/Профиля */}
                <Link to={`/trainers/${trainer.id}`} className="block pt-3">
                    <button className="flex items-center text-blue-600 hover:text-blue-700 font-semibold transition-colors">
                        <Calendar className="w-5 h-5 mr-2" />
                        <span>Профиль</span>
                        <ChevronRight className="w-4 h-4 ml-1" />
                    </button>
                </Link>
            </div>
        </Card>
    );
};

const Trainers: React.FC = () => {
    const [trainers, setTrainers] = React.useState<Trainer[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState<string | null>(null);

    React.useEffect(() => {
        const fetchTrainers = async () => {
            try {
                const data = await getTrainers();
                setTrainers(data);
            } catch (error: any) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTrainers();
    }, []);

    if (loading) {
        return (
            <MainLayout>
                <p>Загрузка тренеров...</p>
            </MainLayout>
        );
    }

    if (error) {
        return (
            <MainLayout>
                <p>Ошибка при загрузке тренеров: {error}</p>
            </MainLayout>
        );
    }

    return (
        <MainLayout>
            <h1 className="text-4xl md:text-5xl font-extrabold mb-8 md:mb-12 text-gray-900">
                Наши Тренеры
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trainers.map(trainer => (
                    <TrainerCard key={trainer.id} trainer={trainer} />
                ))}
            </div>

            {/* Если нет тренеров, показать заглушку */}
            {trainers.length === 0 && (
                <Card className="text-center p-12 mt-8">
                    <p className="text-gray-500">
                        Список тренеров временно недоступен.
                    </p>
                </Card>
            )}
        </MainLayout>
    );
};

export default Trainers;