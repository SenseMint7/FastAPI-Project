from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Board(BaseModel):
    __tablename__ = "board"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    public: Mapped[bool] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
