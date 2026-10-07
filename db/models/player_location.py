from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from db.models.base import Base
from .world import Path, Site


class PlayerLocation(Base):
    """
    One row per site the player has occupied -- an itinerary log, not a
    single mutable "current location" row. get_location() always fetches
    the most recent row by arrival_time; that row IS the player's current
    location. Earlier rows are history, kept for reconstructing an
    itinerary later.

    site_id is always populated on every row, whether "locality" or
    "path": even mid-transit, the player is within whichever Site stretch
    tiles the path at path_position. Ambient dwelling conditions (shelter/
    ventilation/temperature) always come from that site, unconditionally.
    Path-specific fields (path_id, path_position, heading_to_site_id) are
    populated only on "path" rows and drive travel conditions (obstacles/
    speed/required tasks), which only matter during an actual
    path-traversal event, not as part of the player's constant ambient
    environment.
    """

    __tablename__ = "player_itinerary"
    __table_args__ = (
        CheckConstraint(
            "("
            "  location_kind = 'locality'"
            "  AND path_id IS NULL"
            "  AND path_position IS NULL"
            "  AND heading_to_site_id IS NULL"
            ") OR ("
            "  location_kind = 'path'"
            "  AND path_id IS NOT NULL"
            "  AND path_position IS NOT NULL"
            "  AND heading_to_site_id IS NOT NULL"
            ")",
            name="player_location_kind_consistency",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    arrival_time: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    location_kind: Mapped[str] = mapped_column(
        String, nullable=False
    )  # "locality" or "path"
    site_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sites.id"), nullable=False
    )
    site: Mapped[Site] = relationship(
        foreign_keys=[site_id]
    )
    path_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("paths.id")
    )
    path: Mapped[Path | None] = relationship(
        foreign_keys=[path_id]
    )
    path_position: Mapped[int | None] = mapped_column(
        Integer
    )
    heading_to_site_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sites.id")
    )
    heading_to_site: Mapped[Site | None] = relationship(
        foreign_keys=[heading_to_site_id]
    )
