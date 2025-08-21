import enum

from sqlalchemy import (
    Column,
    String,
    Text,
    Enum,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .base import Base
from .mixin.int_id_pk import IdIntPkMix


class TaskStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base, IdIntPkMix):

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED, nullable=False)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User", back_populates="tasks")
