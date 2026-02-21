from db.models import PlayerRecord, Item
from db.repository import (
    ItemRepository,
    PlayerRepository,
)
from player.anatomy import Anatomy
from player.inventory import Inventory
from player.stats import Stats


class Player:
    def __init__(
        self,
        player: PlayerRecord,
        player_repo: PlayerRepository,
        item_repo: ItemRepository,
    ):
        self.player_rec = player
        self.inventory = Inventory(
            item_repo, self.player_rec.id
        )
        self.anatomy = Anatomy(
            self.player_rec.id, player_repo
        )
        self.stats = Stats(self.player_rec.id, player_repo)

    def equip_item(self, item: Item, slot_id_list):
        mold = self.inventory.repo.get_original_mold(item)
        for slot_id in slot_id_list:
            slot = self.anatomy.get_slot_by_id(slot_id)
            self.anatomy.repo.occupy_equipment_slot(slot, item)

    def get_slot_id(self, slot_dict):
        slot = self.anatomy.repo.get_slot_id(
            self.player_rec.id,
            slot_dict["body_name"],
            slot_dict["slot"],
        )
        return slot.id
