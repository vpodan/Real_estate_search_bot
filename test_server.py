#!/usr/bin/env python3
"""
Минимальный тестовый сервер для проверки работы на Render
"""

from fastapi import FastAPI
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем простое FastAPI приложение
app = FastAPI(
    title="Test Server",
    description="Минимальный тестовый сервер",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Test Server is running!",
        "status": "success",
        "port": os.environ.get("PORT", "not_set")
    }

@app.get("/health")
async def health():
    """Проверка здоровья"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    # Получаем порт из переменной окружения
    port = int(os.environ.get("PORT", 10000))
    
    logger.info(f"Запуск тестового сервера на порту {port}")
    
    try:
        # Запускаем сервер
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Ошибка запуска сервера: {e}")
        raise
