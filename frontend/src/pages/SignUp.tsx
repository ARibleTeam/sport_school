// src/pages/SignUp.tsx - Обновленный код
import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
// Явные импорты
import { Card, CardHeader, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { signup } from "@/lib/api";

const SignUp: React.FC = () => {
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [fullName, setFullName] = React.useState("");
    const [phoneNumber, setPhoneNumber] = React.useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await signup(email, password, fullName, phoneNumber);
            navigate("/signin"); // Перенаправляем на страницу входа
        } catch (error: any) {
            alert(`Ошибка регистрации: ${error.message}`);
        }
    };

    return (
        // Центрирование на весь экран, фон light gray
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md p-8 shadow-2xl">
                
                <CardHeader className="text-center mb-6">
                    <h1 className="text-3xl font-bold text-gray-900">Регистрация</h1>
                    <p className="text-gray-500 text-sm">Создайте аккаунт для начала работы</p>
                </CardHeader>

                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4 pt-0"> {/* Уменьшаем space-y для большего количества полей */}
                        <Input
                            type="text"
                            placeholder="Фамилия Имя Отчество"
                            required
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                        />
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
                        <Input
                            type="tel" // Используем type="tel" для номера телефона
                            placeholder="Номер телефона"
                            required
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                        />

                        <Button type="submit" className="w-full h-12 mt-4">
                            Зарегистрироваться
                        </Button>
                    </form>

                    <div className="mt-6 text-center text-sm text-gray-500">
                        Уже есть аккаунт?{" "}
                        <Link to="/signin" className="text-blue-600 hover:text-blue-700 font-medium underline-offset-4 hover:underline">
                            Войти
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default SignUp;