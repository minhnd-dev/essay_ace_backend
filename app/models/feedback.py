from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.models._base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    content: Mapped[str]
    rewrite: Mapped[str]
