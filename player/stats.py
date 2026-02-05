from db.repository import PlayerStatRepository


class Stats:
    def __init__(
        self, stat_repo: PlayerStatRepository, player_id
    ):
        self.repo = stat_repo
        self.player_id = player_id

    def get(self, stat_name: str):
        return self.repo.get(self.player_id, stat_name)

    def get_all(self) -> dict:
        return self.repo.get_all(self.player_id)

    def add(self, stat_name: str, amount: int):
        self.repo.add(self.player_id, stat_name, amount)
