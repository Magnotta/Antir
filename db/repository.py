from typing import List, Optional
from db.database import Session
from db.models import (
    Player,
    Location,
    Item,
    Item_Mold,
    Item_Param
)

class PlayerRepository:
    def create(self, name: str) -> Player:
        session = Session()
        instance = Player(name=name)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def get(self, id: int):
        session = Session()
        return session.get(Player, id)

    def update(self, id: int, **fields):
        session = Session()
        instance = session.get(Player, id)
        if not instance:
            return None

        for key, value in fields.items():
            setattr(instance, key, value)

        session.commit()
        return instance

    def delete(self, id: int) -> bool:
        session = Session()
        instance = session.get(Player, id)
        if not instance:
            return False

        session.delete(instance)
        session.commit()
        return True
    
    # def list_all(self) -> List[Player]:
    #     session = Session()
    #     return session.query(Player).all()
    
class LocationRepository:
    def create(self, name: str):
        session = Session()
        instance = Location(name=name)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def get(self, id: int):
        session = Session()
        return session.get(Location, id)

    def update(self, id: int, **fields):
        session = Session()
        instance = session.get(Location, id)
        if not instance:
            return None

        for key, value in fields.items():
            setattr(instance, key, value)

        session.commit()
        return instance

    def delete(self, id: int) -> bool:
        session = Session()
        instance = session.get(Location, id)
        if not instance:
            return False

        session.delete(instance)
        session.commit()
        return True