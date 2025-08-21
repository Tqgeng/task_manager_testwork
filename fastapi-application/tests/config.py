from core.config import settings


def auth_login() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.auth,
        "/login",
    )
    path = "".join(parts)
    return path.removeprefix("/")


def auth_register() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.auth,
        "/register",
    )
    path = "".join(parts)
    return path.removeprefix("/")


def task() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.tasks,
    )
    path = "".join(parts)
    return path


def task_for_id(task_id: int) -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.tasks,
        f"/{task_id}",
    )
    path = "".join(parts)
    return path
