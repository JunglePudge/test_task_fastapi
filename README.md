# FastAPI Test Task

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/JunglePudge/test_task_fastapi.git
cd test_task_fastapi
```


### 2. Создание виртуального окружения

**Примечание:** используемая версия Python 3.11.18
 
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/MacOS:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск сервиса

```
uvicorn main:app --reload
```

Сервис будет доступен по адресу: http://localhost:8000/
## Документация API

Для получения досупа к автоматической документации используйте
http://localhost:8000/docs - Swagger
http://localhost:8000.у/external/docs - ReDoc

## Структура
later