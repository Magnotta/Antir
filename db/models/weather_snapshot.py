from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import Integer
from db.models.base import Base


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    tick: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    temperature: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    wind_latent: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    precip_latent: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
