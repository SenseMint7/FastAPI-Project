from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    fullname: Mapped[str] = mapped_column(String(100), nullable=False, comment="이름")
    email: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False, unique=True, comment="이메일"
    )
    password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="비밀번호"
    )
