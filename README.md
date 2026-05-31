# Сервис для поиска соседа по общежитию или совместной аренде жилья

Внутренний «Tinder» для студентов: анкета с привычками (ложитесь/встаете рано, курите, любите тишину), поиск по критериям, лайки, чат для связи.

## Состав команды и роли

- **@Annett-a** — Frontend Developer
- **@NastyaKovyrzina** — Frontend Developer
- **@Viktoriazavr** — Frontend Developer
- **@operupolnomochennaya** — Backend Developer
- **@sam1rrrr** — Backend Developer

## Инструкция по запуску

### 1. Установка зависимостей

Убедитесь, что у вас установлен `uv`. Затем выполните:

```bash
uv sync
```

### 2. Запуск приложения

```bash
uv run uvicorn app.main:app --reload
```

## Переменные среды

| Название переменной          | Тип | Описание                               | Значение по умолчанию |
| ---------------------------- | --- | -------------------------------------- | --------------------- |
| DB_SCHEMA                    | str | Схема подключения БД                   | postgresql+asyncpg    |
| DB_HOST                      | str | Хост базы данных                       | localhost             |
| DB_PORT                      | int | Порт базы данных                       | 5432                  |
| DB_USER                      | str | Имя пользователя БД                    |                       |
| DB_PASSWORD                  | str | Пароль пользователя БД                 |                       |
| DB_NAME                      | str | Название базы данных                   |                       |
| JWT_SECRET_KEY               | str | Секретный ключ для подписи JWT-токенов |                       |
| JWT_ALGORITHM                | str | Алгоритм подписи JWT                   | HS256                 |
| ACCESS_TOKEN_EXPIRE_SECONDS  | int | Время жизни access-токена в секундах   | 900                   |
| REFRESH_TOKEN_EXPIRE_SECONDS | int | Время жизни refresh-токена в секундах  | 1800                  |
| REFRESH_COOKIE_NAME          | str | Название cookie для refresh-токена     | refresh_token         |
| RBAC_ADMIN_ROLE              | str | Название роли администратора           | admin                 |
| RBAC_PUBLIC_ROLE             | str | Название публичной роли                | public                |
| RBAC_ADMIN_EMAIL             | str | Email начального admin-пользователя    | admin@admin.com       |
| RBAC_ADMIN_PASSWORD          | str | Пароль начального admin-пользователя   | adminpassword         |
| RBAC_ADMIN_FIRST_NAME        | str | Имя начального admin-пользователя      | Admin                 |
| RBAC_ADMIN_LAST_NAME         | str | Фамилия начального admin-пользователя  | User                  |
