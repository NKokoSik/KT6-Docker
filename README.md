# KT6 — Контейнеризация и автоматический деплой

## Запуск локально через Docker Compose

Требуется установленный Docker Desktop с Docker Compose.

Из корневой папки проекта выполните:

```bash
docker compose up --build
```

После запуска:

- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- Проверка подключения PostgreSQL: http://localhost:8000/db-health

Остановка контейнеров:

```bash
docker compose down
```

Остановка с удалением данных PostgreSQL:

```bash
docker compose down -v
```

## Сервисы

- `app` — FastAPI-приложение.
- `db` — PostgreSQL 16.
- `redis` — Redis 7.
- `celery_worker` — Celery-воркер для фоновых задач.

Внутри Docker-сети приложение обращается к PostgreSQL по имени `db`, а к Redis — по имени `redis`. Настройки находятся в `.env.docker`.

## Автоматические тесты

Тесты запускаются локально командой:

```bash
pytest -q
```

GitHub Actions запускает `pytest` автоматически при push в ветку `main`. Workflow находится в `.github/workflows/tests.yml`.

## Публичный деплой

Платформа: Railway или VPS.

Публичный адрес приложения: **указать после фактического деплоя**.

После деплоя проверьте, что публичный адрес `/docs` открывается из интернета.
