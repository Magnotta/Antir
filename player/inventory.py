from db.repository import ItemRepository
from db.models.mold import Item


class Inventory:
    def __init__(
        self, item_repo: ItemRepository, player_id: int
    ):
        self.repo = item_repo
        self.player_id = player_id

    def get_items(self) -> list[Item]:
        """Get all non-destroyed items owned by this player."""
        # Get all extant items and filter by owner
        all_items = self.repo.get_extant_items()
        return [
            item
            for item in all_items
            if item.owner_id == self.player_id
        ]
