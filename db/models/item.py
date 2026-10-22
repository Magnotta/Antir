from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    JSON,
    ForeignKey,
    UniqueConstraint,
)
from db.models.base import Base
from core.defs.task import ToolProfile


class ItemParam(Base):
    __tablename__ = "item_params"
    __table_args__ = (UniqueConstraint("item_id", "name"),)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    value: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    item: Mapped["Item"] = relationship(
        back_populates="param_list"
    )


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    original_mold_id: Mapped[int] = mapped_column(
        ForeignKey("molds.id"),
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    destroyed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    param_list: Mapped[list[ItemParam]] = relationship(
        cascade="all, delete-orphan",
        back_populates="item",
    )
    container_item_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=True
    )
    container_item: Mapped["Item | None"] = relationship(
        back_populates="contained_items", remote_side=[id]
    )
    contained_items: Mapped[list["Item"]] = relationship(
        back_populates="container_item"
    )
    mold: Mapped["Mold"] = relationship(
        back_populates="spawned_items"
    )

    def __repr__(self):
        return (
            f"<Item id={self.id} mold={self.original_mold_id} "
            f"owner={self.owner_id} "
            f"container={self.container_item}>"
        )

    def get_param(
        self,
        name: "str",
        default: int | None = None,
    ) -> int | None:
        for param in self.param_list:
            if param.name == name:
                return param.value
        return default

    def set_param(self, name: "str", value: int) -> None:
        for param in self.param_list:
            if param.name == name:
                param.value = value
                return
        self.param_list.append(
            ItemParam(name=name, value=value)
        )


class ParamSpec(Base):
    __tablename__ = "mold_param_specs"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    mold_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("molds.id"), nullable=False
    )
    param: Mapped[str] = mapped_column(
        String, nullable=False
    )
    base: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    variance: Mapped[int] = mapped_column(
        Integer, default=0
    )
    mold: Mapped["Mold"] = relationship(
        back_populates="param_specs"
    )
    __table_args__ = (UniqueConstraint("mold_id", "param"),)


class Mold(Base):
    __tablename__ = "molds"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    tags: Mapped[str] = mapped_column(
        String, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    occupied_slots: Mapped[dict | None] = mapped_column(
        JSON
    )
    tool_profile: Mapped[ToolProfile | None] = (
        mapped_column(JSON)
    )
    param_specs: Mapped[list[ParamSpec]] = relationship(
        back_populates="mold", cascade="all, delete-orphan"
    )
    spawned_items: Mapped[list[Item]] = relationship(
        back_populates="mold", cascade="all, delete-orphan"
    )
