from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    JSON,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from db.models.base import Base


class Site(Base):
    __tablename__ = "sites"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    locality_id: Mapped[int | None] = mapped_column(
        ForeignKey("localities.id")
    )
    locality: Mapped["Locality | None"] = relationship(
        back_populates="sites",
    )
    path_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "paths.id",
            use_alter=True,
            name="fk_paths_origin_site",
        )
    )
    path: Mapped["Path | None"] = relationship(
        back_populates="sites", foreign_keys=[path_id]
    )
    start: Mapped[int | None]
    end: Mapped[int | None]


class Path(Base):
    __tablename__ = "paths"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    origin_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    origin: Mapped["Locality"] = relationship(
        back_populates="outgoing_paths",
        foreign_keys=[origin_id],
    )
    origin_site_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sites.id",
            use_alter=True,
            name="fk_paths_origin_site",
        )
    )
    origin_site: Mapped[Site] = relationship(
        foreign_keys=[origin_site_id]
    )
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    destination: Mapped["Locality"] = relationship(
        back_populates="incoming_paths",
        foreign_keys=[destination_id],
    )
    destination_site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id")
    )
    destination_site: Mapped[Site] = relationship(
        foreign_keys=[destination_site_id]
    )
    length_m: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)
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
    sites: Mapped[list[Site]] = relationship(
        back_populates="path",
        foreign_keys=[Site.path_id],
        cascade="all, delete-orphan",
        order_by="Site.start",
    )
    junctions_as_a: Mapped[list["Junction"]] = relationship(
        back_populates="path_a",
        foreign_keys="Junction.path_a_id",
        cascade="all, delete-orphan",
    )
    junctions_as_b: Mapped[list["Junction"]] = relationship(
        back_populates="path_b",
        foreign_keys="Junction.path_b_id",
        cascade="all, delete-orphan",
    )

    @property
    def junctions(self) -> list["Junction"]:
        """All junctions touching this path, regardless of which side it is."""
        return [*self.junctions_as_a, *self.junctions_as_b]

    def __repr__(self):
        return f"<Path {self.origin_id} -> {self.destination_id}>"


class Junction(Base):
    __tablename__ = "junctions"
    __table_args__ = (
        # A given pair of paths may only meet once at a given pair of positions.
        UniqueConstraint(
            "path_a_id",
            "position_a_m",
            "path_b_id",
            "position_b_m",
            name="uq_junction_positions",
        ),
        # Prevent a path being paired with itself.
        CheckConstraint(
            "path_a_id <> path_b_id",
            name="ck_junction_distinct_paths",
        ),
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    path_a_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    path_a: Mapped["Path"] = relationship(
        back_populates="junctions_as_a",
        foreign_keys=[path_a_id],
    )
    position_a_m: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    path_b_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    path_b: Mapped["Path"] = relationship(
        back_populates="junctions_as_b",
        foreign_keys=[path_b_id],
    )
    position_b_m: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)

    def __repr__(self) -> str:
        return (
            f"<Junction path_a={self.path_a_id}@{self.position_a_m}m "
            f"<-> path_b={self.path_b_id}@{self.position_b_m}m>"
        )

    def other_path(
        self, from_path: "Path"
    ) -> tuple["Path", int]:
        """Given the path you are currently on, return (other_path, position_on_it)."""
        if from_path.id == self.path_a_id:
            return self.path_b, self.position_b_m
        if from_path.id == self.path_b_id:
            return self.path_a, self.position_a_m
        raise ValueError(
            "Path is not part of this junction"
        )


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
    sites: Mapped[list[Site]] = relationship(
        back_populates="locality",
        foreign_keys=[Site.locality_id],
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
    position: Mapped[int] = mapped_column(
        Integer, nullable=False
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
    start: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    end: Mapped[int] = mapped_column(
        Integer, nullable=False
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
