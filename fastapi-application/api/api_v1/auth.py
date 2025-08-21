from fastapi import APIRouter, Request

from core.shemas.user import (
    UserRead,
    UserCreate,
)
from .fastapi_users_router import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from core.config import settings
from mailing.send_welcome_email import send_welcome_email

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


# /login /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
