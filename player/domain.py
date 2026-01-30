from db.models import Player
from db.repository import ItemRepository, PlayerRepository
from player.anatomy import Anatomy
from player.inventory import Inventory
from player.stats import Stats

class PlayerDomain:
    def __init__(self, player: Player, item_repo: ItemRepository):
        self.player = player
        self.inventory = Inventory(item_repo, self.player.id)
        self.anatomy = Anatomy(self.player.id)
        self.stats = Stats()