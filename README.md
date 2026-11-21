# KT6 — Контейнеризация и автоматический деплой

## Запуск проекта

Для запуска проекта нужен установленный Docker Desktop с Docker Compose

Чтобы запустить приложение, нужно открыть папку проекта в терминале и выполнить команду:

```bash
docker compose up --build
```

После запуска приложение будет доступно по следующим адресам:

- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- Проверка подключения к базе данных: http://localhost:8000/db-health

Чтобы остановить контейнеры, нужно выполнить:

```bash
docker compose down
```

Если нужно остановить контейнеры и удалить данные PostgreSQL, используется команда:

```bash
docker compose down -v
```

## Используемые сервисы

В проекте используются следующие сервисы:

- `app` — основное приложение на FastAPI
- `db` — база данных PostgreSQL 16
- `redis` — Redis 7
- `celery_worker` — обработка фоновых задач

Приложение подключается к PostgreSQL через имя `db`, а к Redis через имя `redis`. Настройки переменных окружения находятся в файле `.env.docker`

## Автоматические тесты

Для запуска тестов вручную используется команда:

```bash
pytest -q
```

Также настроен GitHub Actions. При отправке изменений в ветку `main` он автоматически запускает тесты. Файл с настройками находится в `.github/workflows/tests.yml`

## Публичный деплой

Для размещения приложения использована платформа Railway

Ссылка на приложение:

https://kt6-docker-production.up.railway.app

Документация Swagger доступна по адресу:

https://kt6-docker-production.up.railway.app/docs
