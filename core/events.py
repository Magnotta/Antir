from db.models import Item
from systems.time_service import Time

EVENTS = {}


class Event:
    type: str = "base"
    impacts: str = ""

    def __init__(
        self, due_time: Time, payload: dict | None = None
    ):
        self.payload = payload or {}
        self.due_time = due_time

    def condition(self, state):
        return True

    def apply(self, state):
        raise NotImplementedError


class EquipItemEvent(Event):
    type = "equip item"
    impacts = "equipment"

    def apply(self, engine):
        item = engine.item_repo.get_by_id(
            self.payload["item_id"]
        )
        player = engine.player_repo.get(item.owner_id)
        player.equip_item(item)
        return []


class PutItemInContainerEvent(Event):
    def apply(self, engine):
        session = engine.session
        inv = engine.inventory
        item = session.get(Item, self.payload["item_id"])
        container = session.get(
            Item, self.payload["container_id"]
        )
        inv.put_in_container(item, container)
        return []


class HungerEvent(Event):
    type = "player hunger"
    impacts = "stats"

    def __init__(self, due_time: Time, payload=None):
        super().__init__(due_time, payload)

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.stats.add("hunger", self.payload["amount"])
        return []
