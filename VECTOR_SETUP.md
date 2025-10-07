# Настройка гибридного поиска с векторной БД

## 📋 Обзор системы

Система использует **гибридный поиск** - комбинирует структурированный поиск в MongoDB с семантическим поиском в векторной БД Chroma.

### Архитектура:
1. **MongoDB** - структурированные данные (цена, комнаты, район, и т.д.)
2. **Chroma** - векторная БД для семантического поиска по описаниям
3. **OpenAI Embeddings** - создание векторов из текста

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка OpenAI API
Создайте `.env` файл:
```
OPENAI_API_KEY=your_api_key_here
```

### 3. Заполнение векторной БД из MongoDB
```bash
# Заполнить векторную БД из всех объявлений в MongoDB
python real_estate_vector_db.py --populate

# Для тестирования - только первые 100 объявлений
python real_estate_vector_db.py --populate --limit 100

# Очистить векторную БД
python real_estate_vector_db.py --reset

# Показать статистику
python real_estate_vector_db.py --stats
```

### 4. Тестирование поиска
```bash
# Семантический поиск
python real_estate_vector_db.py --search "тихий район с парковкой"

# Тестирование гибридного поиска
python hybrid_search.py
```

---

## 🔧 Интеграция с существующим кодом

### Обновление скрапинга (scarpy.py)

Замените в `scarpy.py`:
```python
# Старое
custom_settings = {
    'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1}
}

# Новое
custom_settings = {
    'ITEM_PIPELINES': {'hybrid_pipeline.HybridMongoDBPipeline': 1}
}
```

### Использование в API (main.py или app.py)

```python
from hybrid_search import HybridRealEstateSearch

# Инициализация
search_engine = HybridRealEstateSearch()

# Гибридный поиск
results = search_engine.search(
    filters={
        "city": "Gdansk",
        "rooms": 2,
        "max_price": 4000
    },
    semantic_query="тихий район с балконом",
    listing_type="rent",
    limit=10
)

for result in results:
    print(f"ID: {result['_id']}")
    print(f"Заголовок: {result.get('title')}")
    print(f"Семантический скор: {result.get('semantic_score', 0)}")
    print(f"Цена: {result.get('price')}")
```

---

## 📊 Примеры использования

### 1. Только структурированные фильтры
```python
results = search_engine.search(
    filters={
        "city": "Warszawa",
        "rooms": [2, 3],
        "min_price": 2000,
        "max_price": 5000,
        "building_type": "block"
    },
    listing_type="rent"
)
```

### 2. Только семантический поиск
```python
results = search_engine.search(
    semantic_query="новая квартира с современным ремонтом рядом с метро",
    listing_type="sale"
)
```

### 3. Гибридный поиск (рекомендуемый)
```python
results = search_engine.search(
    filters={
        "city": "Gdansk", 
        "max_price": 4000
    },
    semantic_query="семейная квартира в тихом районе с парковкой",
    listing_type="rent"
)
```

---

## 🗂️ Структура файлов

- `real_estate_embedding_function.py` - функции для создания embeddings
- `real_estate_vector_db.py` - работа с векторной БД Chroma
- `hybrid_pipeline.py` - pipeline для одновременного сохранения в MongoDB + Chroma
- `hybrid_search.py` - основная логика гибридного поиска

---

## 🔍 Как работает поиск

### Этап 1: MongoDB фильтрация
```
Запрос: "2 комнаты в Гданьске до 4000 зл с парковкой"
├── Структурированные фильтры → MongoDB
│   ├── room_count: 2
│   ├── city: "Gdansk"
│   └── price: ≤ 4000
│
└── Результат: 150 объявлений → [ID1, ID2, ..., ID150]
```

### Этап 2: Семантический поиск
```
Семантический запрос: "с парковкой"
├── Создание embedding → [0.1, -0.2, 0.5, ...]
├── Поиск в Chroma среди ID1-ID150
└── Результат: 10 самых релевантных объявлений
```

### Этап 3: Объединение результатов
```
Финальный результат:
├── Полные данные из MongoDB
├── Семантический скор из Chroma
└── Ранжирование по релевантности
```

---

## ⚡ Производительность

- **MongoDB фильтрация**: ~10-50ms (с индексами)
- **Векторный поиск**: ~100-300ms (зависит от размера БД)
- **Общее время**: ~200-400ms для гибридного поиска

### Оптимизация:
1. Создайте индексы в MongoDB:
   ```javascript
   db.rent_listings.createIndex({"city": 1, "room_count": 1, "price": 1})
   db.sale_listings.createIndex({"city": 1, "room_count": 1, "price": 1})
   ```

2. Ограничивайте размер векторной БД по времени (например, только объявления за последний год)

---

## 🛠️ Устранение неполадок

### Ошибка OpenAI API
```
Убедитесь что:
1. OPENAI_API_KEY установлен в .env
2. У вас есть средства на аккаунте OpenAI
3. API ключ действительный
```

### Chroma не находит документы
```bash
# Проверьте статистику
python real_estate_vector_db.py --stats

# Пересоздайте БД
python real_estate_vector_db.py --reset --populate
```

### MongoDB пустой
```bash
# Сначала запустите скрапинг
python scarpy.py

# Потом заполните векторную БД
python real_estate_vector_db.py --populate
```
