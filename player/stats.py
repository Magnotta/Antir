from db.repository import PlayerRepository


class Stats:
    def __init__(
        self, player_id, player_repo: PlayerRepository
    ):
        self.player_id = player_id
        self.repo = player_repo

    def get(self, stat_name: str):
        return self.repo.get_stat(self.player_id, stat_name)

    def get_all(self) -> dict:
        return self.repo.get_all_stats(self.player_id)

    def add(self, stat_name: str, amount: int):
        self.repo.add_to_stat(
            self.player_id, stat_name, amount
        )
