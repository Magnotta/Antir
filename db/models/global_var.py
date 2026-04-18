from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import Integer, String
from .base import Base


class GlobalVar(Base):
    __tablename__ = 'global_vars'
    key: Mapped[str] = mapped_column(
        String, primary_key=True
    )
    value = mapped_column(Integer, nullable=False)
