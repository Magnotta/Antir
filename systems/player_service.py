from db.repository import PlayerRepository

class PlayerService:
    def __init__(self):
        self.repo = PlayerRepository()

    def create_new_player(self, name: str):
        return self.repo.create(name=name)

    def level_up(self, player_id: int):
        player = self.repo.get(player_id)
        if not player:
            return None

        return self.repo.update(
            player_id,
            level=player.level + 1,
            hp=player.hp + 10
        )