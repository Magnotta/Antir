from db.models import PlayerRecord, ItemSlotOccupancy
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

    def equip_item(self, item_id):
        item = self.inventory.repo.get_item_by_id(item_id)
        mold = self.inventory.repo.get_original_mold(item)
        if "eq" not in mold.tags:
            raise ValueError(
                f"{item.name} is not equipable!"
            )
        self.inventory.repo.check_slots_occupied(
            mold.occupied_slots
        )
        for slot in mold.occupied_slots:
            self.session.add(
                ItemSlotOccupancy(
                    item_id=item_id,
                    equipment_slot_id=slot.id,
                )
            )
        self.session.commit()
