from db.models import PlayerRecord
from db.repository import ItemRepository, PlayerStatRepository
from player.anatomy import Anatomy
from player.inventory import Inventory
from player.stats import Stats

class Player:
    def __init__(self, player: PlayerRecord, item_repo: ItemRepository, stat_repo: PlayerStatRepository):
        self.player_rec = player
        self.inventory = Inventory(item_repo, self.player_rec.id)
        self.anatomy = Anatomy(self.player_rec.id)
        self.stats = Stats(stat_repo, self.player_rec.id)