# Сервис для поиска соседа по общежитию или совместной аренде жилья

Внутренний «Tinder» для студентов: анкета с привычками (ложитесь/встаете рано, курите, любите тишину), поиск по критериям, лайки, чат для связи.

## Состав команды и роли

- **@Annett-a** — Frontend Developer
- **@NastyaKovyrzina** — Frontend Developer
- **@Viktoriazavr** — Frontend Developer
- **@operupolnomochennaya** — Backend Developer
- **@sam1rrrr** — Backend Developer

## Запуск через Docker Compose

### Требования

- [Docker](https://docs.docker.com/get-docker/) (версия 24+)

### Шаги

1. Склонируйте репозиторий:

```bash
git clone <repo-url>
cd backend
```

2. Создайте файл `.env` на основе `.env.example`:

3. Запустите проект:

```bash
docker compose up
```

После запуска:

| Адрес | Что это |
|---|---|
| `http://localhost` | Главная страница |
| `http://localhost/api/v1/docs` | Swagger UI (документация API) |

> Все запросы к API нужно делать через `http://localhost/api/v1/...` — nginx проксирует их на бэкенд автоматически.

### Остановка

```bash
docker compose down          # остановить контейнеры
docker compose down -v       # остановить и удалить БД (данные будут потеряны)
```

---

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

### Production run

```
gunicorn app.main:app -c gunicorn.conf.py
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

# Запуск проекта через Docker Compose

Проект можно запустить локально через Docker Compose. Этот способ рекомендуется для проверки взаимодействия backend, базы данных и reverse proxy в окружении, приближенном к production.

### 1. Подготовка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example` и заполните значения переменных.

Минимальный набор переменных для локального запуска:

```env
DB_SCHEME=postgresql+asyncpg
DB_HOST=db
DB_PORT=5432
DB_USER=roomie
DB_PASSWORD=roomie_password
DB_NAME=roomiematch

POSTGRES_USER=roomie
POSTGRES_PASSWORD=roomie_password
POSTGRES_DB=roomiematch

JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=900
REFRESH_TOKEN_EXPIRE_SECONDS=2592000
REFRESH_COOKIE_NAME=refresh_token

RBAC_ADMIN_ROLE=admin
RBAC_PUBLIC_ROLE=public
RBAC_ADMIN_EMAIL=admin@admin.com
RBAC_ADMIN_PASSWORD=adminpassword
RBAC_ADMIN_FIRST_NAME=Admin
RBAC_ADMIN_LAST_NAME=User

LOG_LEVEL=INFO
LOG_FILE_PATH=logs/app.log

EMAIL_NOTIFICATIONS_ENABLED=false
SMTP_HOST=smtp.yandex.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Roomie Match
SMTP_STARTTLS=true
SMTP_SSL_TLS=false

EMAIL_CONFIRMATION_CODE_EXPIRE_MINUTES=15
PASSWORD_RESET_CODE_EXPIRE_MINUTES=15

FRONTEND_BASE_URL=http://localhost
CORS_ALLOW_ORIGINS=http://localhost,http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=100/minute
RATE_LIMIT_AUTH=10/minute
```

Для локального запуска можно отключить email-уведомления:

```env
EMAIL_NOTIFICATIONS_ENABLED=false
```

Для production-окружения необходимо использовать отдельные безопасные значения паролей, JWT-секрета и SMTP-доступов.

### 2. Запуск контейнеров

Из корня проекта выполните:

```bash
docker compose up
```

Для запуска в фоновом режиме:

```bash
docker compose up -d
```

После запуска приложение будет доступно через reverse proxy:

```text
http://localhost
```

API-документация доступна по адресу:

```text
http://localhost/docs
```

API-запросы проксируются через префикс:

```text
/api
```

### 3. Остановка контейнеров

```bash
docker compose down
```

Для удаления контейнеров вместе с volume базы данных:

```bash
docker compose down -v
```

Команду с `-v` следует использовать осторожно, так как она удаляет данные PostgreSQL.

### 4. Структура Docker Compose

В compose-файле используются следующие сервисы:

```text
db              PostgreSQL 18
migrate         применение миграций Alembic
bootstrap       создание базовых RBAC-ресурсов
api             backend-приложение
nginx           reverse proxy / frontend gateway
```

Для PostgreSQL используется постоянный volume:

```text
postgres_data
```

Наружу открыт только порт `80`. База данных и внутренние backend-сервисы не публикуют внешние порты.

## Deployment через Ansible и GitHub Actions

Для автоматизации deployment-процесса в проект добавлены Ansible playbook-и и GitHub Actions workflow.

### 1. Ansible-структура

```text
ansible/
  ansible.cfg
  requirements.yml
  inventories.ini.example
  playbooks/
    init-vm.yml
    build-and-push-image.yml
    update-compose.yml
  templates/
    docker-compose.prod.yml.j2
  nginx/
    nginx.conf
```

Назначение playbook-ов:

```text
init-vm.yml                 инициализация виртуальной машины
build-and-push-image.yml    сборка и публикация Docker-образа backend
update-compose.yml          обновление compose-файла и перезапуск приложения на ВМ
```

Локальный файл inventory не должен попадать в Git:

```text
ansible/inventories.ini
```

Для примера используется файл:

```text
ansible/inventories.ini.example
```

### 2. Проверка Ansible playbook-ов

Playbook-и проверяются через `ansible-lint`.

Локальная проверка через Docker:

```bash
MSYS_NO_PATHCONV=1 docker run --rm --entrypoint sh -v "$(pwd -W):/work" -w /work cytopia/ansible-lint -c "ansible-galaxy collection install -r ansible/requirements.yml && ansible-lint ansible/playbooks/init-vm.yml"

MSYS_NO_PATHCONV=1 docker run --rm --entrypoint sh -v "$(pwd -W):/work" -w /work cytopia/ansible-lint -c "ansible-galaxy collection install -r ansible/requirements.yml && ansible-lint ansible/playbooks/build-and-push-image.yml"

MSYS_NO_PATHCONV=1 docker run --rm --entrypoint sh -v "$(pwd -W):/work" -w /work cytopia/ansible-lint -c "ansible-galaxy collection install -r ansible/requirements.yml && ansible-lint ansible/playbooks/update-compose.yml"
```

Также проверка Ansible playbook-ов запускается в GitHub Actions.

### 3. GitHub Actions

В проекте используются следующие workflow:

```text
.github/workflows/init-vm.yml          ручная инициализация ВМ
.github/workflows/deploy.yml           release и deployment из main
.github/workflows/ansible-lint.yml     проверка Ansible playbook-ов
```

Общий код для настройки SSH и Ansible вынесен в custom action:

```text
.github/actions/setup-ansible/action.yml
```

### 4. Переменные и секреты для deployment

Для работы deployment workflow необходимо настроить GitHub Actions variables и secrets.

Repository / organization variables:

```text
VM_HOST              публичный IP виртуальной машины
VM_USER              SSH-пользователь на ВМ
DOCKER_USER          логин DockerHub
DOCKER_IMAGE_NAME    имя Docker-образа backend
```

Repository / organization secrets:

```text
SSH_PRIVATE_KEY_B64  приватный SSH-ключ в base64
SSH_KNOWN_HOSTS      known_hosts для ВМ
DOCKER_TOKEN         DockerHub access token
GH_TOKEN             GitHub token для semantic-release
ENV                  production .env для приложения
```

Секреты не должны храниться в репозитории. Они добавляются через интерфейс GitHub:

```text
Settings → Secrets and variables → Actions
```

### 5. Deployment workflow

Deployment запускается только из ветки `main`.

Общий процесс:

```text
push в main
→ semantic-release создаёт release tag
→ release tag используется как Docker image tag
→ Ansible собирает и публикует backend image
→ Ansible обновляет docker-compose.yml на ВМ
→ приложение перезапускается через Docker Compose
```

Если semantic-release не создал новый release, deployment-job не выполняется.

### 6. Инициализация ВМ

Workflow инициализации ВМ запускается вручную через GitHub Actions:

```text
Actions → Init VM → Run workflow
```

Он выполняет playbook:

```text
ansible/playbooks/init-vm.yml
```

Playbook устанавливает необходимые утилиты, Docker, Docker Compose plugin, `curl`, `rsync` и проверяет доступность Docker на сервере.

## HTTPS

Для HTTPS-подключения планируется использовать:

```text
DuckDNS
Nginx Proxy Manager
Let’s Encrypt
```

На стороне cloud-провайдера должны быть открыты порты:

```text
80    HTTP
81    Nginx Proxy Manager admin panel
443   HTTPS
```

После настройки домена и сертификата необходимо обновить production-переменные:

```env
FRONTEND_BASE_URL=https://your-domain.duckdns.org
CORS_ALLOW_ORIGINS=https://your-domain.duckdns.org
```