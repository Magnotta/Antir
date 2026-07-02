from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models.player_record import PlayerRecord
from db.models.player_stat import (
    PlayerStat,
    StatThreshold,
    HistoricalStat,
)
from db.models.item_slot_occupancy import ItemSlotOccupancy
from db.models.body_node import BodyNode
from db.models.equipment_slot import EquipmentSlot
from db.models.item import Item
from core.defs import (
    SLOT_MAX_INDEX,
    BODY_SCHEMA,
)


class PlayerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_player(self, id: int):
        return self.session.get(PlayerRecord, id)

    def set_player(self, id: int, **fields):
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return None
        for key, value in fields.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete_player(self, id: int) -> bool:
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True

    def get_all_stats(
        self, player_id: int
    ) -> dict[str, int]:
        rows = (
            self.session.query(PlayerStat)
            .filter(PlayerStat.player_id == player_id)
            .all()
        )
        return {row.name: row.value for row in rows}

    def get_all_thresholds(self):
        stmt = select(StatThreshold)
        thresholds = self.session.scalars(stmt).all()
        return {t.stat_name: t for t in thresholds}

    def get_historical_stats(
        self, player_id: int
    ) -> dict[str, HistoricalStat]:
        """Return dict of stat_name -> HistoricalStat for a given player."""
        stmt = select(HistoricalStat).where(
            HistoricalStat.player_id == player_id
        )
        records = self.session.scalars(stmt).all()
        return {r.stat_name: r for r in records}

    def update_historical_stats(
        self,
        player_id: int,
        stats: dict[str, int],
        current_time: int,
    ) -> None:
        """
        Update all-time min/max for a player's stats.
        Creates new records if they don't exist.
        """
        for stat_name, current_value in stats.items():
            record = (
                self.session.query(HistoricalStat)
                .filter_by(
                    player_id=player_id, stat_name=stat_name
                )
                .first()
            )

            if record is None:
                # First time seeing this stat – initialize
                record = HistoricalStat(
                    player_id=player_id,
                    stat_name=stat_name,
                    all_time_max=current_value,
                    last_updated=current_time,
                )
                self.session.add(record)
            else:
                # Update if new peak
                if current_value > record.all_time_max:
                    record.all_time_max = current_value
                    record.last_updated = current_time
        self.session.commit()

    def get_stat(
        self, player_id: int, statname: str
    ) -> int:
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == statname,
            )
            .one()
        )
        return row.value

    def set_stat(self, player_id: int, stat: str, value):
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == stat,
            )
            .one()
        )
        row.value = value
        self.session.commit()

    def set_node_stat(
        self, node: BodyNode, stat: str, val: int, add=False
    ):
        if not add:
            setattr(node, stat, val)
        else:
            old_val = getattr(node, stat)
            setattr(node, stat, old_val + val)
        self.session.commit()

    def add_to_stat(
        self, player_id: int, stat: str, delta: float
    ):
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == stat,
            )
            .one()
        )
        if row.value + delta < 0:
            row.value = 0
        else:
            row.value += delta
        self.session.commit()

    def create_body_tree(self, player_id):
        exists = (
            self.session.query(BodyNode)
            .filter_by(owner_id=player_id, parent_id=None)
            .first()
        )
        if exists:
            return exists
        return self.create_body_node(
            "head", BODY_SCHEMA["head"], player_id
        )

    def create_body_node(
        self, node_name, node_dict, player_id, parent_id=-1
    ):
        if parent_id == -1:
            new_node = BodyNode(
                broken_bone=False,
                torn_ligament=False,
                dislocated_joint=False,
                severed=False,
                venomous_bite=False,
                insect_bite=False,
                poison_sting=False,
                swollen_joint=False,
                sliced=0,
                pierced=0,
                bludgeoned=0,
                notes="",
                owner_id=player_id,
                name=node_name,
            )
        else:
            new_node = BodyNode(
                broken_bone=False,
                torn_ligament=False,
                dislocated_joint=False,
                severed=False,
                venomous_bite=False,
                insect_bite=False,
                poison_sting=False,
                swollen_joint=False,
                sliced=0,
                pierced=0,
                bludgeoned=0,
                notes="",
                owner_id=player_id,
                name=node_name,
                parent_id=parent_id,
            )
        self.session.add(new_node)
        self.session.flush()
        for slot in node_dict["slots"]:
            for idx in range(SLOT_MAX_INDEX[slot]):
                new_node.slots.append(
                    (
                        EquipmentSlot(
                            body_node_id=new_node.id,
                            slot_type=slot,
                            slot_index=idx,
                        )
                    )
                )
        for child in node_dict["children"]:
            new_node.children.append(
                self.create_body_node(
                    child,
                    node_dict["children"][child],
                    player_id,
                    parent_id=new_node.id,
                )
            )
        self.session.commit()
        return new_node

    def get_slot_by_id(self, slot_id):
        return self.session.get(EquipmentSlot, slot_id)

    def get_slot_id(self, player_id, body_name, slot):
        body_node = (
            self.session.query(BodyNode)
            .filter(
                BodyNode.owner_id == player_id,
                BodyNode.name == body_name,
            )
            .one()
        )
        return (
            self.session.query(EquipmentSlot)
            .filter(
                EquipmentSlot.body_node_id == body_node.id,
                EquipmentSlot.slot_type == slot,
                EquipmentSlot.item_id is None,
            )
            .first()
        )

    def occupy_equipment_slot(
        self, slot: EquipmentSlot, item: Item
    ):
        try:
            self.session.add(
                ItemSlotOccupancy(
                    item_id=item.id,
                    equipment_slot_id=slot.id,
                )
            )
            slot.item_id = item.id
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_complete_body(
        self, player_id
    ) -> list[BodyNode]:
        stmt = select(BodyNode).where(
            BodyNode.owner_id == player_id
        )
        return self.session.scalars(stmt).all()
