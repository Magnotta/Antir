from db.repository import PlayerRepository
from db.models import BodyNode


class PlayerService:
    def __init__(self):
        self.repo = PlayerRepository()

    def create_new_player(self, name: str):
        return self.repo.create(name=name)

    def create_player_anatomy(self, player_id):
        head = BodyNode(owner=player_id, name="head")

        spine = BodyNode(owner=player_id, name="spine", parent=head)

        neck = BodyNode(owner=player_id, name="head", parent=spine)

        torso = BodyNode(owner=player_id, name="torso", parent=neck)
        left_shoulder = BodyNode(
            owner=player_id,
            name="left_shoulder",
            parent=torso,
        )
        left_arm = BodyNode(
            owner=player_id,
            name="left_arm",
            parent=left_shoulder,
        )
        left_forearm = BodyNode(
            owner=player_id,
            name="left_forearm",
            parent=left_arm,
        )
        left_hand = BodyNode(
            owner=player_id,
            name="left_hand",
            parent=left_forearm,
        )
        right_shoulder = BodyNode(
            owner=player_id,
            name="right_shoulder",
            parent=torso,
        )
        right_arm = BodyNode(
            owner=player_id,
            name="right_arm",
            parent=right_shoulder,
        )
        right_forearm = BodyNode(
            owner=player_id,
            name="right_forearm",
            parent=right_arm,
        )
        right_hand = BodyNode(
            owner=player_id,
            name="right_hand",
            parent=right_forearm,
        )
        hips = BodyNode(
            owner=player_id,
            name="hips",
            parent=spine,
        )
        left_thigh = BodyNode(
            owner=player_id,
            name="left_thigh",
            parent=hips,
        )
        left_shank = BodyNode(
            owner=player_id,
            name="left_shank",
            parent=left_thigh,
        )
        left_foot = BodyNode(
            owner=player_id,
            name="left_foot",
            parent=left_shank,
        )
        right_thigh = BodyNode(
            owner=player_id,
            name="right_thigh",
            parent=hips,
        )
        right_shank = BodyNode(
            owner=player_id,
            name="right_shank",
            parent=right_thigh,
        )
        right_foot = BodyNode(
            owner=player_id,
            name="right_foot",
            parent=right_shank,
        )
        return head
