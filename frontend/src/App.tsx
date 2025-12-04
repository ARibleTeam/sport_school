import { Toaster as Sonner, Toaster } from "sonner";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import Schedule from "./pages/Schedule";
import Trainers from "./pages/Trainers";
import TrainerProfile from "./pages/TrainerProfile";
import NotFound from "./pages/NotFound";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Logout from "./pages/Logout";
import { TooltipProvider } from "@radix-ui/react-tooltip";
import React, { useState, useEffect } from 'react';
import { getCurrentUser, User } from './lib/api';
import ScheduleForm from "./pages/Admin/ScheduleForm";
import AdminIndex from "./pages/Admin/AdminIndex";

const queryClient = new QueryClient();

const App = () => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const loadUser = async () => {
        setIsLoading(true);
        const currentUser = await getCurrentUser();
        setUser(currentUser);
        setIsLoading(false);
    };

    useEffect(() => {
        loadUser();
        // Добавляем слушатель события storage
        window.addEventListener('storage', loadUser);
        // Убираем слушатель события при размонтировании компонента
        return () => {
            window.removeEventListener('storage', loadUser);
        };
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="text-3xl font-bold text-gray-700 animate-pulse">
                    Загрузка...
                </div>
            </div>
        );
    }

    // Проверка авторизации
    const isLoggedIn = !!user;

    const handleLogoutComplete = () => {
        setUser(null); // Явно устанавливаем user в null после выхода
    };

    return (
        <QueryClientProvider client={queryClient}>
            <TooltipProvider>
                <Toaster />
                <Sonner />
                <BrowserRouter>
                    <Routes>
                        {/* Роуты, доступные только для неавторизованных пользователей */}
                        <Route path="/signin" element={isLoggedIn ? <Navigate to="/" replace /> : <SignIn />} />
                        <Route path="/signup" element={isLoggedIn ? <Navigate to="/" replace /> : <SignUp />} />

                        {/* Роуты, доступные только для авторизованных пользователей */}
                        <Route
                            path="/"
                            element={isLoggedIn ? (user.isAdmin ? <AdminIndex user={user} /> : <Index user={user} />) : <Navigate to="/signin" replace />}
                        />
                        <Route
                            path="/schedule"
                            element={isLoggedIn ? <Schedule user={user} /> : <Navigate to="/signin" replace />}
                        />
                         <Route
                            path="/admin/schedule/new"
                            element={isLoggedIn && user.isAdmin ?  <ScheduleForm /> : <Navigate to="/signin" replace />}
                        />
                         <Route
                            path="/admin/schedule/edit/:id"
                            element={isLoggedIn && user.isAdmin ?  <ScheduleForm /> : <Navigate to="/signin" replace />}
                        />
                        <Route path="/logout" element={<Logout />} />


                        {/* Остальные роуты */}
                        <Route path="/coaches" element={isLoggedIn ? <Trainers /> : <Navigate to="/signin" replace />} />
                        <Route path="/trainers/:id" element={isLoggedIn ? <TrainerProfile /> : <Navigate to="/signin" replace />} />
                        <Route path="*" element={<NotFound />} />
                    </Routes>
                </BrowserRouter>
            </TooltipProvider>
        </QueryClientProvider>
    );
};

export default App;