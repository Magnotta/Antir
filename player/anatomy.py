from db.models import BodyNode, EquipmentSlot
from db.repository import PlayerRepository


class Anatomy:
    def __init__(
        self, player_id, player_repo: PlayerRepository
    ):
        self.player_id = player_id
        self.repo = player_repo
        self.head = self.repo.create_body_tree(
            self.player_id
        )
        self.by_name = {}
        self._index_tree(self.head)

    def _index_tree(self, node: BodyNode):
        self.by_name[node.name] = node
        for child in node.children:
            self._index_tree(child)

    def get_bodynode_by_name(
        self, name: str
    ) -> BodyNode | None:
        return self.by_name[name]

    def get_slot_by_id(self, slot_id):
        return self.repo.get_slot_by_id(slot_id)

    def get_slot_by_description(
        self, body_name, slot_name
    ) -> EquipmentSlot:
        body = self.get_bodynode_by_name(body_name)
        if not body:
            raise ValueError(
                f"Body part not found: {body_name}"
            )
        found_slot = False
        for slot in body.slots:
            if slot.slot_type == slot_name:
                found_slot = True
                if slot.item_id is not None:
                    continue
                return slot
        if not found_slot:
            raise ValueError(
                f"Slot '{slot_name}' not found on body part '{body_name}'"
            )
        raise ValueError(
            f"Slot '{slot_name}' is over-encumbered!"
        )
