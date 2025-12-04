// src/pages/SignIn.tsx
import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card, CardHeader, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { signin } from "@/lib/api"; // Импортируем функцию signin

const SignIn: React.FC = () => {
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const data = await signin(email, password);
            // Сохраняем токен в localStorage (или другом надежном месте)
            localStorage.setItem("access_token", data.access_token);
            // Отправляем пользовательское событие для обновления данных пользователя
            window.dispatchEvent(new Event('storage'));
            navigate("/"); // Перенаправляем на главную страницу
        } catch (error: any) {
            alert(`Ошибка входа: ${error.message}`);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md p-8 shadow-2xl">
                <CardHeader className="text-center mb-6">
                    <h1 className="text-3xl font-bold text-gray-900">Вход в Sport School</h1>
                    <p className="text-gray-500 text-sm">Войдите в свой аккаунт</p>
                </CardHeader>

                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4 pt-0">
                        <Input
                            type="email"
                            placeholder="Email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <Input
                            type="password"
                            placeholder="Пароль"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button type="submit" className="w-full h-12 mt-4">
                            Войти
                        </Button>
                    </form>

                    <div className="mt-6 text-center text-sm text-gray-500">
                        Нет аккаунта?{" "}
                        <Link to="/signup" className="text-blue-600 hover:text-blue-700 font-medium underline-offset-4 hover:underline">
                            Зарегистрироваться
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default SignIn;