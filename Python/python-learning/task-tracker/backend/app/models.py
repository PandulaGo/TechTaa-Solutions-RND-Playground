from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class Task(Base):
    __tablename__ = "tasks" # - Define the name of the database table that this model will be mapped to. In this case, the table name is "tasks".
    id: Mapped[int] = mapped_column(primary_key=True) # -
    title: Mapped[str] = mapped_column(String(255)) 
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
