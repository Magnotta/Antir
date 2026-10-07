from db.repository.location import LocationRepository


class Location:
    def __init__(
        self,
        player_id,
        loc_repo: LocationRepository,
    ):
        self.player_id = player_id
        self.repo = loc_repo
