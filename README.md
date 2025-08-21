# TaskManager - FastAPI + PostgreSQL в Docker

Простое приложение для управления задачами на FastAPI.

## Функционал
- Создание задачи
- Получение задачи по `id`
- Список всех задач
- Обновление задачи
- Удаление задачи
- Swagger UI по адресу `/docs`

## Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [RabbitMQ](https://www.rabbitmq.com/) — брокер сообщений
- [MailDev](https://github.com/maildev/maildev) — тестовый SMTP сервер
- [Pytest](https://docs.pytest.org/)

## Запуск проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Tqgeng/task_manager_testwork.git
cd task_manager_testwork
```

2. Соберите и запустите контейнеры:
```bash
docker compose up -d pg rabbitmq maildev backend
```
3. Приложение будет доступно по адресу:

Swagger UI: http://localhost:8000/docs

4. Тесты

```bash
pytest tests/test_tasks.py -v
```

5. Активация брокера
```bash
taskiq worker core.taskiq_broker:broker tasks_queue.welcome_email_notification
```
