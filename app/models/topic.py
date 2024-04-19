from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models._base import Base
from app.models.response import Response


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    responses = relationship(Response, back_populates="topic")
