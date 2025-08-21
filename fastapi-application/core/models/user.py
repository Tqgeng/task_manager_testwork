from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from sqlalchemy.orm import relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixin.int_id_pk import IdIntPkMix

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdIntPkMix, SQLAlchemyBaseUserTable[UserIdType]):

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)
