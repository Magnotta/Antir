from db.models import (
    Item, EquipmentSlot
)
from systems.time_service import Time

EVENTS = {}

class Event:
    type: str = "base"
    impacts: str = ''

    def __init__(self, due_time: Time, payload: dict | None = None):
        self.id = 0
        self.payload = payload or {}
        self.due_time = due_time

    def _set_id(self, id):
        self.id = id

    def condition(self, state):
        return True

    def apply(self, state):
        raise NotImplementedError
    
class EquipItemEvent(Event):
    def apply(self, engine):
        session = engine.session

        item = session.get(Item, self.payload["item_id"])
        inv = item.owner
        slot = session.get(EquipmentSlot, self.payload["slot_id"])

        if not inv.can_equip(item, slot):
            raise ValueError("Cannot equip item")

        inv.equip_item(item, slot)

        return []
    
class PutItemInContainerEvent(Event):
    def execute(self, engine):
        session = engine.session
        inv = engine.inventory

        item = session.get(Item, self.payload["item_id"])
        container = session.get(Item, self.payload["container_id"])

        inv.put_in_container(item, container)

        return []

class HungerEvent(Event):
    type = "player hunger"
    impacts = "stats"
     
    def __init__(self, due_time: Time, payload = None):
        super().__init__(due_time, payload)

    def apply(self, state):
        player = state.get_player_by_id(self.payload["target"])
        player.stats.add("hunger", self.payload["amount"])
        return []