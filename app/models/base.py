from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.rdb import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_dt: Mapped[datetime] = mapped_column(default=func.now())
    updated_dt: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
