from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import create_db_and_tables
from app.user.router import user_router
from app.coach.router import coach_router
from app.test.router import test_router
from app.training.router import training_router

async def lifespan(app: FastAPI):
    await create_db_and_tables(app)
    yield


# Создаем экземпляр FastAPI
app = FastAPI(
    title="SPORT SCHOOL",
    description="API для проекта SPORT SCHOOL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(coach_router)
app.include_router(test_router)
app.include_router(training_router)

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )





