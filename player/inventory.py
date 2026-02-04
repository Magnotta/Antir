from db.repository import ItemRepository

class Inventory:
    def __init__(self, item_repo: ItemRepository, player_id: int):
        self.item_repo = item_repo
        self.player_id = player_id

    def loose_items(self):
        return self.item_repo.get_loose_items(self.player_id)

    def equipped_items(self):
        return self.item_repo.get_equipped_items(self.player_id)

    def containers(self):
        return self.item_repo.get_containers(self.player_id)