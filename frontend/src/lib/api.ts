 export interface User {
  id: string;
  name: string;
  isAdmin: boolean;
  isAthlete: boolean;
}

export interface SigninResponse {
    access_token: string;
    token_type: string;
}

export interface Trainer {
    id: number;
    experience_years: number;
    bio: string;
    full_name: string;
    email: string;
    specialization: [string];
}

export interface Training {
    coach: string;
    id: number;
    type: 'individual' | 'group';
    title: string;
    time: string;
    location: string;
    date: string;
    participants?: number;
}

export interface TrainerWithSchedule {
    trainer: Trainer;
    schedule: Training[];
}

const API_BASE_URL = "http://127.0.0.1:8000"; // Определяем базовый URL

export async function getCurrentUser(): Promise<User | null> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        return null; // Если токена нет, возвращаем null
    }

    const response = await fetch(`${API_BASE_URL}/users/me`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (!response.ok) {
        // Обработка ошибок (например, токен истек)
        console.error("Ошибка при получении данных пользователя:", response.status);
        return null; // Возвращаем null в случае ошибки
    }

    const data = await response.json();
    return data;
}

export async function signup(
  email: string,
  password: string,
  fullName: string,
  phoneNumber: string
): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/users/signup`,{
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
      full_name: fullName,
      phone_number: phoneNumber,
    }),
  });

  if (!response.ok) {
    // Обработка ошибок
    let errorMessage = "Ошибка регистрации";
    try {
      const errorData = await response.json();
      errorMessage = errorData.message || errorMessage;
    } catch (e) {
      // Если не удалось распарсить JSON, используем статус ответа
      errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorMessage);
  }

  const data = await response.json();
  return data;
}

export async function signin(email: string, password: string): Promise<SigninResponse> {
    const response = await fetch(`${API_BASE_URL}/users/signin`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,
            password,
        }),
    });

    if (!response.ok) {
        let errorMessage = "Ошибка входа";
        try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
        } catch (e) {
            errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}

export async function logout(): Promise<{ message: string }> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        return { message: "Logged out successfully" };
    }

    const response = await fetch(`${API_BASE_URL}/users/logout`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (!response.ok) {
        let errorMessage = "Ошибка выхода";
        try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
        } catch (e) {
            errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}

export async function getTrainers(): Promise<Trainer[]> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        throw new Error("Пользователь не авторизован");
    }

    const response = await fetch(`${API_BASE_URL}/coaches`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (!response.ok) {
        let errorMessage = "Ошибка при получении тренеров";
        try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
        } catch (e) {
            errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}

export async function getTrainerById(id: number): Promise<TrainerWithSchedule> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        throw new Error("Пользователь не авторизован");
    }

    const response = await fetch(`${API_BASE_URL}/coaches/${id}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (!response.ok) {
        let errorMessage = "Ошибка при получении тренера";
        try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
        } catch (e) {
            errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}


export interface ScheduleParams {
    type?: 'individual' | 'group';
}

export async function getSchedule(params: ScheduleParams = {}): Promise<Training[]> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        throw new Error("Пользователь не авторизован");
    }

    const url = new URL(`${API_BASE_URL}/schedule`);
    const searchParams = new URLSearchParams();
    if (params.type) {
        searchParams.append('type', params.type);
    }
    url.search = searchParams.toString();

    const response = await fetch(url.toString(), {
        method: "GET",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (!response.ok) {
        let errorMessage = "Ошибка при получении расписания";
        try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
        } catch (e) {
            errorMessage = `Ошибка ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}