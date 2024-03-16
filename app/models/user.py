from sqlalchemy.orm import Mapped, mapped_column

from app.models._base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    password: Mapped[str]
