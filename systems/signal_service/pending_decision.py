from enum import Enum, auto


class DecisonType(Enum):
    slot_choice = auto()
    bodynode_choice = auto()


class PendingDecision:
    def __init__(
        self, decision_type: DecisonType, payload: dict
    ):
        self.type = decision_type
        self.payload = payload
