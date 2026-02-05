from sqlalchemy import select
from db.models import (
    PlayerRecord,
    Location,
    BodyNode,
    EquipmentSlot,
    Item,
    PlayerStat,
)


class PlayerStatRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self, player_id: int) -> dict[str, float]:
        rows = (
            self.session.query(PlayerStat)
            .filter(PlayerStat.player_id == player_id)
            .all()
        )
        return {row.name: row.value for row in rows}

    def get(self, player_id: int, statname: str) -> int:
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == statname,
            )
            .one()
        )
        return row.value

    def set(self, player_id: int, stat: str, value: float):
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == stat,
            )
            .one()
        )
        row.value = value
        self.session.commit()

    def add(self, player_id: int, stat: str, delta: float):
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == stat,
            )
            .one()
        )
        row.value += delta
        self.session.commit()


class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def get(self, id: int):
        return self.session.get(PlayerRecord, id)

    def set(self, id: int, **fields):
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return None
        for key, value in fields.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True


class LocationRepository:
    def __init__(self, session):
        self.session = session

    def create(self, name: str):
        instance = Location(name=name)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int):
        return self.session.get(Location, id)

    def set(self, id: int, **fields):
        instance = self.session.get(Location, id)
        if not instance:
            return None
        for key, value in fields.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(Location, id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True


class ItemRepository:
    def __init__(self, session):
        self.session = session

    def get_loose_items(self, player_id: int):
        equipped_ids = select(EquipmentSlot.item_id).where(
            EquipmentSlot.item_id.isnot(None)
        )
        return (
            self.session.query(Item)
            .filter(Item.owner == player_id)
            .filter(Item.container_item_id.is_(None))
            .filter(~Item.id.in_(equipped_ids))
            .all()
        )

    def get_equipped_items(self, player_id: int):
        return (
            self.session.query(EquipmentSlot)
            .join(BodyNode)
            .filter(BodyNode.owner == player_id)
            .filter(EquipmentSlot.item_id.isnot(None))
            .all()
        )

    def get_containers(self, player_id: int):
        return (
            self.session.query(Item)
            .filter(Item.owner == player_id)
            .filter(Item.contained_items.any())
            .all()
        )
