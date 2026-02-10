from db.repository import ItemRepository


class Inventory:
    def __init__(
        self, item_repo: ItemRepository, player_id: int
    ):
        self.repo = item_repo
        self.player_id = player_id
