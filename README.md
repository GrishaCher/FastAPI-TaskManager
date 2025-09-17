🚀 FastAPI Task Manager
Простой и эффективный менеджер задач с современным стеком технологий.

📋 О проекте
FastAPI Task Manager - это бэкенд-приложение для управления задачами с аутентификацией пользователей и верификацией email.

🛠️ Технологический стек
Backend

FastAPI - современный Python фреймворк

SQLAlchemy 2.0 - ORM с асинхронной поддержкой

PostgreSQL - реляционная база данных

AsyncPG - асинхронный драйвер для PostgreSQL

Pydantic v2 - валидация данных и сериализация

JWT - аутентификация через токены

Alembic - миграции базы данных

Безопасность

bcrypt - хеширование паролей

JOSE - JWT токены

Email верификация - подтверждение email адресов

Инструменты разработки

Poetry - управление зависимостями

Uvicorn - ASGI сервер


🚀 Быстрый старт
Предварительные требования

Python 3.12+

PostgreSQL 14+

Poetry


Установка

Клонируйте репозиторий

```
git clone https://github.com/GrishaCher/FastAPI-TaskManager.git

cd FastAPI-TaskManager/backend
```

Установите зависимости

Перейдите в папку backend и пропишите в терминалк:
```bash
poetry install --no-root

poetry shell
```

Настройте переменные окружения

Создайте файл .env в папке backend и настройте его


Создайте бд:
```bash
poetry run alembic upgrade head
```
Можно пользоваться:
```bash
poetry run uvicorn app.main:app --reload
```
Приложение будет доступно по адресу: http://localhost:8000

📚 Документация API

После запуска приложения доступны:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Применение миграций
```bash
poetry run create_migration -m "your_comment" 

poetry run migrate-up 

poetry run migrate-down 
```
