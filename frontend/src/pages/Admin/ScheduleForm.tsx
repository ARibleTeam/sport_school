// src/pages/Admin/ScheduleForm.tsx

import React, { useState, useEffect } from 'react';
import { MainLayout } from "../../components/layout/mainlayout.tsx";
// TODO ТУТ ОШИБКААА
import { Button } from "../../components/ui/button";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useNavigate, useParams } from 'react-router-dom';
import { Input } from '@/components/ui/input.tsx';
import { createTraining, CreateTrainingPayload, getGroups, getHalls } from '@/lib//api';


interface Training {
    id: number;
    groupId: number;
    hallId: number;
    date: string; // "YYYY-MM-DD"
    startTime: string; // "HH:mm"
    endTime: string; // "HH:mm"
    type: 'individual' | 'group';
    title: string;
    coach: string;
    participants?: number;
}

export interface Group {
    id: number;
    name: string;
}

export interface Hall {
    id: number;
    name: string;
    capacity: number;
}

const ScheduleForm: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();


    const [groups, setGroups] = useState<Group[]>([]);
    const [halls, setHalls] = useState<Hall[]>([]);
    const [selectedDate, setSelectedDate] = useState<Date | null>(null);
    const [startTime, setStartTime] = useState<string>("");
    const [endTime, setEndTime] = useState<string>("");
    const [selectedGroupId, setSelectedGroupId] = useState<number | null>(null);
    const [selectedHallId, setSelectedHallId] = useState<number | null>(null);
    const [isDateTimeModalOpen, setIsDateTimeModalOpen] = useState(false);
    const [startDateTime, setStartDateTime] = useState<Date | null>(null);
    const [endDateTime, setEndDateTime] = useState<Date | null>(null);

    useEffect(() => {
        // ЗАМЕНИТЕ ВЕСЬ fetchData НА ЭТОТ БЛОК
        const fetchData = async () => {
            try {
                // Вызываем наши новые API функции
                const groupsData = await getGroups();
                const hallsData = await getHalls();
                
                // Записываем реальные данные в состояние
                setGroups(groupsData);
                setHalls(hallsData);

            } catch (error) {
                console.error("Ошибка при загрузке данных для формы:", error);
                // Здесь можно добавить обработку ошибок, например, показать уведомление
            }
        };
        
        fetchData();

        if (id) {
            // Fetch training data based on ID
            const fetchTraining = async () => {
                // TODO: Implement getTrainingById in api.ts
                // const data = await getTrainingById(parseInt(id));
                // setTraining(data);
                // setGroupId(data.groupId);
                // setHallId(data.hallId);
                // setSelectedDate(new Date(data.date));
                // setStartTime(data.startTime);
                // setEndTime(data.endTime);

                console.log("TODO: Implement getTrainingById in api.ts");
                console.log("Implement API call to pre-fill the form");

                // Mock data
                const mockData: Training = {
                    id: 1,
                    groupId: 1,
                    hallId: 2,
                    date: "2024-01-20",
                    startTime: "10:00",
                    endTime: "11:30",
                    type: 'individual',
                    title: "Анализ техники плавания",
                    coach: "Алексей Смирнов",
                    participants: 0,
                };
                //  const parsedDate = new Date(mockData.date);
                setSelectedGroupId(mockData.groupId);
                setSelectedHallId(mockData.hallId);
                setSelectedDate(new Date(mockData.date));
                setStartTime(mockData.startTime);
                setEndTime(mockData.endTime);
            /*  setTraining(mockData) */
            //  console.log("mockData : " +mockData.date)
            };
            fetchTraining();
        }
    }, [id]);


    const handleDateChange = (date: Date) => {
        setSelectedDate(date);
    };

    const handleStartTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setStartTime(e.target.value);
    };

    const handleEndTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEndTime(e.target.value);
    };


    const handleGroupChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedGroupId(parseInt(e.target.value));
    };

    const handleHallChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedHallId(parseInt(e.target.value));
    };

    const handleOpenDateTimeModal = () => {
        setIsDateTimeModalOpen(true);
    };

    const handleCloseDateTimeModal = () => {
        setIsDateTimeModalOpen(false);
    };

    const handleSetDateTime = (start: Date, end: Date) => {
        setStartDateTime(start);
        setEndDateTime(end);
        setIsDateTimeModalOpen(false);
    };

    const handleSubmit = async (e: React.FormEvent) => {
            e.preventDefault();

            // 1. Валидация: Проверяем, что все поля заполнены
            if (!selectedDate || !startTime || !endTime || !selectedGroupId || !selectedHallId) {
                alert("Пожалуйста, заполните все поля формы.");
                return;
            }

            // 2. Сборка datetime: Совмещаем дату и время в полноценные объекты Date
            try {
                const [startHours, startMinutes] = startTime.split(':').map(Number);
                const [endHours, endMinutes] = endTime.split(':').map(Number);

                const startDateTime = new Date(selectedDate);
                startDateTime.setHours(startHours, startMinutes, 0, 0); // Устанавливаем часы и минуты

                const endDateTime = new Date(selectedDate);
                endDateTime.setHours(endHours, endMinutes, 0, 0);

                // Дополнительная проверка
                if (endDateTime <= startDateTime) {
                    alert("Время окончания должно быть позже времени начала.");
                    return;
                }

                // 3. Формирование тела запроса (payload)
                const payload: CreateTrainingPayload = {
                    start_time: startDateTime.toISOString(), // Преобразуем в ISO строку
                    end_time: endDateTime.toISOString(),
                    group_id: selectedGroupId,
                    hall_id: selectedHallId
                };

                // 4. Вызов API
                // TODO: Когда будете реализовывать редактирование, здесь будет `if (id)`
                const response = await createTraining(payload);

                alert(response.message); // Показываем успешное сообщение от бэкенда
                navigate('/schedule'); // Перенаправляем на страницу расписания

            } catch (error) {
                // Отлавливаем ошибку (например, 409 Conflict от бэкенда)
                console.error("Ошибка при создании тренировки:", error);
                alert((error as Error).message); // Показываем пользователю текст ошибки
            }
    };

    return (
        <MainLayout>
            <div className="flex justify-center items-center h-full">
                <div className="bg-gray-100 p-8 rounded-lg shadow-md w-full max-w-md">
                    <h1 className="text-2xl font-bold mb-6 text-gray-800">{id ? 'Редактировать тренировку' : 'Добавить тренировку'}</h1>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="group" className="block text-gray-700 text-sm font-bold mb-2">Группа</label>
                            <select
                                id="group"
                                name="group"
                                onChange={handleGroupChange}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={selectedGroupId || ""}
                                required
                            >
                                <option value="">Выберите группу</option>
                                {groups.map(group => (
                                    <option key={group.id} value={group.id}>{group.name}</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label htmlFor="hall" className="block text-gray-700 text-sm font-bold mb-2">Зал</label>
                            <select
                                id="hall"
                                name="hall"
                                onChange={handleHallChange}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={selectedHallId || ""}
                                required
                            >
                                <option value="">Выберите зал</option>
                                {halls.map(hall => (
                                    <option key={hall.id} value={hall.id}>{hall.name} ({hall.capacity} мест)</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label htmlFor="date" className="block text-gray-700 text-sm font-bold mb-2">Дата</label>
                            <DatePicker
                                selected={selectedDate}
                                onChange={handleDateChange}
                                dateFormat="dd/MM/yyyy"
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="startTime" className="block text-gray-700 text-sm font-bold mb-2">Время начала</label>
                            <Input
                                type="time"
                                id="startTime"
                                name="startTime"
                                value={startTime}
                                onChange={handleStartTimeChange}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="endTime" className="block text-gray-700 text-sm font-bold mb-2">Время окончания</label>
                            <Input
                                type="time"
                                id="endTime"
                                name="endTime"
                                value={endTime}
                                onChange={handleEndTimeChange}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                required
                            />
                        </div>
                        <Button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                            {id ? 'Сохранить' : 'Создать'}
                        </Button>
                    </form>
                </div>
            </div>
        </MainLayout>
    );
};

export default ScheduleForm;