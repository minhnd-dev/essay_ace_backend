from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models._base import Base
from app.models.feedback import Feedback


class Response(Base):
    __tablename__ = "responses"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    content: Mapped[str]
    updated_at: Mapped[datetime]
    created_at: Mapped[datetime]

    topic = relationship("Topic", back_populates="responses")
    feedback = relationship(Feedback, back_populates="response")
