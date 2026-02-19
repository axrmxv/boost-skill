# Boost Skill

**REST API микросервис для управления навыками и тренировочными сессиями.**  
Проект реализован на Python с использованием FastAPI и предназначен для создания, хранения и обработки данных о навыках и тренировочных сессиях.

---

## Описание

Boost Skill — это backend-сервис, позволяющий пользователям регистрировать свои навыки, создавать тренировочные сессии и отслеживать прогресс в рамках набора упражнений. API предоставляет CRUD-функционал для работы с навыками, сессиями и пользователями, а также реализует базовую аутентификацию.

Проект может использоваться как основа для образовательных платформ, личных трекеров обучения или сервисов геймификации навыков.

---

## Что делает проект

- Принимает данные о навыках и тренировочных сессиях через REST API.
- Сохраняет данные в базе PostgreSQL.
- Обеспечивает аутентификацию пользователей (создание, вход).
- Позволяет создавать и управлять записями о навыках и сессиях.
- Обеспечивает фильтрацию и получение данных по различным параметрам (например, по пользователю).

---

## Технологии

| Компонент              | Инструмент                       |
|------------------------|----------------------------------|
| Язык                   | Python                           |
| Web-фреймворк          | FastAPI                          |
| HTTP-сервер            | Uvicorn                          |
| ORM                    | SQLAlchemy                       |
| База данных            | PostgreSQL                       |
| Завершение миграций    | Alembic                          |
| Контейнеризация        | Docker                           |
| Тестирование           | Pytest                           |

---

## Как запустить

### Запуск БД через Docker

1. Клонируй репозиторий:
```bash
   git clone https://github.com/axrmxv/boost-skill.git
   cd boost-skill
```
2. Запусти контейнеры:
```bash
docker compose up --build
```

### Локальный запуск без Docker
1. Создай виртуальное окружение и установи зависимости:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Настрой переменные окружения в `.env`.
3. Запусти сервер:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Примеры запросов к API
### Регистрация пользователя

POST /auth/register
```json
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "password": "securepassword"
      }'
```
Ответ:
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### Вход (получение токена)

POST /auth/login
```json
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "password": "securepassword"
      }'
```
Ответ:
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer"
}
```

### Создание навыка

POST /skills/
```json
curl -X POST "http://localhost:8000/skills/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Python",
        "description": "Backend development"
      }'
```
Ответ:
```json
{
  "id": 1,
  "name": "Python",
  "description": "Backend development"
}
```

### Получение всех навыков
```json
curl "http://localhost:8000/skills/"
```

Ответ:
```json
[
  {
    "id": 1,
    "name": "Python",
    "description": "Backend development"
  }
]
```
