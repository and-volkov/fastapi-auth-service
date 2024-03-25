
# FastAPI Auth Service

Fastapi сервис для аутентификации пользователей (тестовое задание)

### Функционал

Администратор = superuser

- Пользователь может получить токен по логину/емейлу и паролю
- Администратор может создать нового пользователя
- Администратор может получить список всех пользователей
- Администратор может получить информацию о пользователе по его логину/емейлу
- Администратор может удалить пользователя по его логину/емейлу
- Администратор может добавить сервис
- Администратор может добавить роли
- Администратор может добавить права пользователю для сервиса

#### Сервис запущен и работает на сервере 

- Документация доступна по адресу http://134.209.248.50/api/v1/docs#/
  - Администратор
  email_or_username: "andrey", password: "1234"
  - Пользователь: 
  email_or_username: "example", password: "1234"
- Аутентификация в swagger не происходит, т.к. использована кастомная схема аутентификации
- Для тестирования можно использовать Postman/curl

#### Примеры запросов

- Получение токена
```bash
curl -X 'POST' \                                                    
  'http://134.209.248.50/api/v1/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email_or_username": "andrey",
  "password": "1234"
}'
```
- Получение списка пользователей
```bash
curl --location 'http://134.209.248.50:80/api/v1/users' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmRyZXkiLCJleHAiOjE4MzU2MTg0MTB9.ROrWHWsFh_1sCAG7b9srjA2XXG0H88U0ZgfpOAafCQE'
```
- Добавление роли пользователя
```bash
curl --location 'http://134.209.248.50:80/api/v1/service_role?user_id=2&role_id=2&service_id=1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmRyZXkiLCJleHAiOjE4MzU2MTg0MTB9.ROrWHWsFh_1sCAG7b9srjA2XXG0H88U0ZgfpOAafCQE' \ 
```

### Стек технологий

- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Pydantic
- SQLAlchemy
- Alembic

### Предварительные требования

- Docker
- Docker Compose
- Make

### Установка

1. Клонировать репозиторий
```bash
git clone https://github.com/yourusername/fastapi-auth-service.git
```

2. Перейти в директорию проекта
```bash
cd fastapi-auth-service
```

3. Скопировать файл `example.env` в `.env`
```bash
cp example.env .env
```

4. Build and run the Docker containers
```bash
docker-compose up --build
```
Или с помощью Make
```bash
make compose
```
5. Применить миграции
```bash
docker compose exec app alembic upgrade head
```

### Комментарии
- Не успел автоматизировать создание суперпользователя, добавлять его необходимо через пгадмин или psql
