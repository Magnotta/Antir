from typing import List, Optional
from sqlalchemy import select
from db.models import (
    Player, Location, BodyNode,
    EquipmentSlot, Item
)

class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def get(self, id: int):
        return self.session.get(Player, id)

    def update(self, id: int, **fields):
        instance = self.session.get(Player, id)
        if not instance:
            return None

        for key, value in fields.items():
            setattr(instance, key, value)

        self.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(Player, id)
        if not instance:
            return False

        self.session.delete(instance)
        self.session.commit()
        return True
    
    # def list_all(self) -> List[Player]:
    #     return self.session.query(Player).all()
    
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

    def update(self, id: int, **fields):
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
        equipped_ids = (
            select(EquipmentSlot.item_id)
            .where(EquipmentSlot.item_id.isnot(None))
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