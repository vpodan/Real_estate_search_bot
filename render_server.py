#!/usr/bin/env python3
"""
FastAPI wrapper для MCP сервера недвижимости для деплоя на Render
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем FastAPI приложение
app = FastAPI(
    title="Real Estate Search API",
    description="API для поиска недвижимости через естественный язык",
    version="1.0.0"
)

# Импортируем наши функции
try:
    from hybrid_search import hybrid_search
    from real_estate_vector_db import RealEstateVectorDB
    
    # Инициализируем векторную базу данных
    vector_db = RealEstateVectorDB()
    logger.info("Инициализация завершена успешно")
    
except Exception as e:
    logger.error(f"Ошибка инициализации: {e}")
    vector_db = None

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
    status: str

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Real Estate Search API",
        "status": "running",
        "endpoints": {
            "search": "/search",
            "stats": "/stats",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "service": "real-estate-search",
        "version": "1.0.0"
    }

@app.post("/search", response_model=SearchResponse)
async def search_real_estate(request: SearchRequest):
    """Поиск недвижимости по естественному языку"""
    try:
        logger.info(f"Выполняется поиск: {request.query}")
        
        # Выполняем гибридный поиск
        search_results = hybrid_search(request.query)
        
        if not search_results or search_results is None:
            return SearchResponse(
                results=[],
                total=0,
                status="no_results"
            )
        
        # Получаем финальные результаты из hybrid_search
        results = search_results.get("final_results", [])
        
        if not results:
            return SearchResponse(
                results=[],
                total=0,
                status="no_results"
            )
        
        # Ограничиваем количество результатов
        limited_results = results[:request.max_results] if results else []
        
        # Форматируем результаты
        formatted_results = []
        for result in limited_results:
            formatted_result = {
                "title": result.get('title', 'Без названия'),
                "price": result.get('price', 'Не указана'),
                "room_count": result.get('room_count', 'Не указано'),
                "space_sm": result.get('space_sm', 'Не указана'),
                "city": result.get('city', 'Не указано'),
                "district": result.get('district', 'Не указано'),
                "link": result.get('link', ''),
                "score": result.get('score', 0),
                "description": result.get('description', '')[:200] + "..." if result.get('description') else ""
            }
            formatted_results.append(formatted_result)
        
        return SearchResponse(
            results=formatted_results,
            total=len(formatted_results),
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_database_stats():
    """Получить статистику базы данных"""
    try:
        if vector_db is None:
            raise HTTPException(status_code=500, detail="Векторная база данных не инициализирована")
        
        stats = vector_db.get_stats()
        
        return {
            "total_listings": stats.get('total', 0),
            "rent_listings": stats.get('rent', 0),
            "sale_listings": stats.get('sale', 0),
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Получаем порт из переменной окружения
    port = int(os.environ.get("PORT", 10000))
    
    logger.info(f"Запуск сервера на порту {port}")
    
    # Запускаем сервер
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
