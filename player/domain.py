from db.models.item import Item
from db.models.player_record import PlayerRecord
from db.repository.item import ItemRepository
from db.repository.player import PlayerRepository
from player.anatomy import Anatomy
from player.inventory import Inventory
from player.stats import Stats
from core.time import Time


class PlayerProperty:
    SLEEPING_SINCE = "sleeping_since"
    SLEEP_REF = "sleep_ref"


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

    def get_slot_id(self, slot_dict):
        slot = self.anatomy.repo.get_slot_id(
            self.player_rec.id,
            slot_dict["body_name"],
            slot_dict["slot"],
        )
        return slot.id

    @property
    def sleeping_since(self) -> Time | None:
        raw = self.player_rec.properties.get(
            PlayerProperty.SLEEPING_SINCE
        )
        return Time(raw) if raw is not None else None

    @sleeping_since.setter
    def sleeping_since(self, value: Time | None):
        self.player_rec.properties[
            PlayerProperty.SLEEPING_SINCE
        ] = (value.tick if value else None)

    @property
    def sleep_ref(self) -> Time | None:
        raw = self.player_rec.properties.get(
            PlayerProperty.SLEEP_REF
        )
        return Time(raw) if raw is not None else None

    @sleep_ref.setter
    def sleep_ref(self, value: Time | None):
        self.player_rec.properties[
            PlayerProperty.SLEEP_REF
        ] = (value.tick if value else None)
