from core.game_state import GameState
from systems.time_service import Time
from systems.signal_service import Signal

EVENTS = {}


class Event:
    type: str = "base"
    signals: list[Signal] = []

    def __init__(
        self, due_time: Time, payload: dict | None = None
    ):
        self.payload = payload or {}
        self.due_time = due_time

    def condition(self, state: GameState):
        return True

    def begin(self, state: GameState) -> list:
        raise NotImplementedError

    def apply(self, state: GameState):
        raise NotImplementedError


class EquipItemEvent(Event):
    type = "equip item"
    signals = [Signal.equipment]

    def begin(self, state: GameState) -> list:
        # item = state.item_repo.get_item_by_id(
        #     self.payload["item_id"]
        # )
        # player = state.get_player_by_id(item.owner_id)
        # player.occupy_both_hands()
        return [
            EquipItemEvent(
                state.time + self.payload["equip_delay"],
                payload=self.payload,
            )
        ]

    def apply(self, state: GameState):
        item = state.item_repo.get_item_by_id(
            self.payload["item_id"]
        )
        player = state.get_player_by_id(item.owner_id)
        player.equip_item_event(
            item, self.payload["slot_ids"]
        )


class ItemOwnershipEvent(Event):
    type = "change item ownership"
    signals = [Signal.inventory]

    def begin(self, state: GameState) -> list:
        self.apply(state)
        return []

    def apply(self, state: GameState):
        state.item_repo.item_chown(
            self.payload["item_id"],
            self.payload["new_owner_id"],
        )


# class PutItemInContainerEvent(Event):
#     def apply(self, state):
#         session = engine.session
#         inv = engine.inventory
#         item = session.get(Item, self.payload["item_id"])
#         container = session.get(
#             Item, self.payload["container_id"]
#         )
#         inv.put_in_container(item, container)
#         return []


class HungerEvent(Event):
    type = "player hunger"
    signals = [Signal.stats]

    def __init__(self, due_time: Time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state: GameState) -> list:
        self.apply(state)
        return []

    def apply(self, state: GameState):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.stats.add("hunger", self.payload["amount"])
