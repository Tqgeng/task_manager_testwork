from core.models import User, db_helper
from .send_email import send_email


async def send_welcome_email(user_id: int) -> None:

    async with db_helper.session_factory() as session:
        user: User | None = await session.get(User, user_id)

    await send_email(
        recipient=user.email,
        subject="Welcome to out site!",
        body=f"Dear {user.email.split('@')[0]}, \n\nWelcome to out site!",
    )
