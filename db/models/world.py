from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    Float,
    String,
    JSON,
    ForeignKey,
)
from .base import Base


class Path(Base):
    __tablename__ = "paths"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    origin_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    distance_km: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)
    origin: Mapped["Locality"] = relationship(
        back_populates="outgoing_paths",
        foreign_keys=[origin_id],
    )
    destination: Mapped["Locality"] = relationship(
        back_populates="incoming_paths",
        foreign_keys=[destination_id],
    )
    point_conditions: Mapped[list["PointCondition"]] = (
        relationship(
            back_populates="path",
            cascade="all, delete-orphan",
            order_by="PointCondition.position",
        )
    )
    segment_conditions: Mapped[list["SegmentCondition"]] = (
        relationship(
            back_populates="path",
            cascade="all, delete-orphan",
            order_by="SegmentCondition.start",
        )
    )

    def __repr__(self):
        return f"<Path {self.origin_id} -> {self.destination_id}>"


class Locality(Base):
    __tablename__ = "localities"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)
    outgoing_paths: Mapped[list[Path]] = relationship(
        back_populates="origin",
        foreign_keys=[Path.origin_id],
        cascade="all, delete-orphan",
    )
    incoming_paths: Mapped[list[Path]] = relationship(
        back_populates="destination",
        foreign_keys=[Path.destination_id],
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"{self.name}"


class PointCondition(Base):
    __tablename__ = "point_conditions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    path_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
    )
    position: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String, nullable=False
    )
    data: Mapped[dict | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    path: Mapped[Path] = relationship(
        back_populates="point_conditions"
    )


class SegmentCondition(Base):
    __tablename__ = "segment_conditions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    path_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
    )
    start: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    end: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String, nullable=False
    )
    data: Mapped[dict | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    path: Mapped[Path] = relationship(
        back_populates="segment_conditions"
    )
