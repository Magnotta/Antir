from db.models import (
    Item, EquipmentSlot
)

EVENTS = {}

class Event:
    type: str = "base"

    def __init__(self, payload: dict | None = None, due_tick: int = 0):
        self.id = 0
        self.payload = payload or {}
        self.due_tick = due_tick

    def _set_id(self, id):
        self.id = id

    def condition(self, state):
        return True

    def apply(self, state):
        raise NotImplementedError
    
class EquipItemEvent(Event):
    def execute(self, engine):
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
