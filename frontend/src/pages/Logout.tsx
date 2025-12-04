// src/pages/Logout.tsx
import * as React from "react";
import { useNavigate } from "react-router-dom";
import { LogOut } from 'lucide-react'; 
import { logout } from "@/lib/api";

const Logout: React.FC = () => {
    const navigate = useNavigate();

    React.useEffect(() => {
        const handleLogout = async () => {
            try {
                await logout();
                // Clear access token from localStorage
                localStorage.removeItem("access_token");
                // Отправляем пользовательское событие для обновления данных пользователя
                window.dispatchEvent(new Event('storage'));
                console.log("LOGOUT: User logged out successfully");
                navigate("/signin", { replace: true });
            } catch (error: any) {
                localStorage.removeItem("access_token");
                 // Отправляем пользовательское событие для обновления данных пользователя
                window.dispatchEvent(new Event('storage'));
                console.error("LOGOUT: Logout failed", error);
                navigate("/signin", { replace: true });
            }
        };

        handleLogout();
    }, [navigate]);

    return (
        // Простое отображение, пока идет выход (чтобы не было пустого экрана)
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
            <LogOut className="w-12 h-12 text-gray-400 mb-4 animate-pulse" />
            <p className="text-xl text-gray-600">Выполняется выход из системы...</p>
        </div>
    );
};

export default Logout;