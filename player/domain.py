from db.models.item import Item
from db.models.player_record import PlayerRecord
from db.repository.item import ItemRepository
from db.repository.player import PlayerRepository
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

    def equip_item_event(self, item: Item, slot_id_list):
        mold = self.inventory.repo.get_original_mold(item)
        for slot_id in slot_id_list:
            slot = self.anatomy.get_slot_by_id(slot_id)
            self.anatomy.repo.occupy_equipment_slot(
                slot, item
            )

    def is_alive(self):
        life_bool = (
            self.stats.get("pneuma") > 0
            and self.stats.get("blood") > 0
            and self.anatomy.get_head_health() > 0
        )
        return life_bool

    def occupy_both_hands(self):
        # if self.weapon_drawn?
        # if self.
        self.stats.set("right_hand_occupied", 1)
        self.stats.set("left_hand_occupied", 1)

    def free_both_hands(self):
        self.stats.set("right_hand_occupied", 0)
        self.stats.set("right_hand_occupied", 0)

    def get_slot_id(self, slot_dict):
        slot = self.anatomy.repo.get_slot_id(
            self.player_rec.id,
            slot_dict["body_name"],
            slot_dict["slot"],
        )
        return slot.id
