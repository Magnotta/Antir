from random import randint
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from db.models import (
    EventRecord,
    PlayerRecord,
    Location,
    BodyNode,
    EquipmentSlot,
    ParamSpec,
    Mold,
    ItemParam,
    Item,
    PlayerStat,
    ItemSlotOccupancy,
)
from core.defs import (
    TAG_TO_PARAMS,
    ITEM_PARAM_MAXES,
    ITEM_PARAM_MODES,
    ITEM_PARAM_DEFAULTS,
    SLOT_MAX_INDEX,
    BODY_SCHEMA,
)


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_record(self, event, org: str):
        rec = EventRecord(
            type=event.type,
            payload=event.payload,
            due_tick=event.due_time.tick,
            origin=org,
        )
        self.session.add(rec)
        self.session.commit()


class PlayerRepository:
    def __init__(self, session):
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
    ) -> dict[str, float]:
        rows = (
            self.session.query(PlayerStat)
            .filter(PlayerStat.player_id == player_id)
            .all()
        )
        return {row.name: row.value for row in rows}

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

    def set_stat(
        self, player_id: int, stat: str, value: float
    ):
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
                health=1000,
                owner_id=player_id,
                name=node_name,
            )
        else:
            new_node = BodyNode(
                health=1000,
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
                        self.create_equipment_slot(
                            slot, new_node.id, idx
                        )
                    )
                )
        self.session.commit()
        for child in node_dict["children"]:
            self.create_body_node(
                child,
                node_dict["children"][child],
                player_id,
                parent_id=new_node.id,
            )
        return new_node

    def create_equipment_slot(self, slot, node_id, idx):
        return EquipmentSlot(
            body_node_id=node_id,
            slot_type=slot,
            slot_index=idx,
        )

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
        self, slot_id: int, item_id: int
    ):
        try:
            self.session.add(
                ItemSlotOccupancy(
                    item_id=item_id,
                    equipment_slot_id=slot_id,
                )
            )
            slot = (
                self.session.query(EquipmentSlot)
                .filter(EquipmentSlot.id == slot_id)
                .first()
            )
            slot.item_id = item_id
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class LocationRepository:
    def __init__(self, session):
        self.session = session

    def create(self, name: str):
        instance = Location(name=name)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int):
        return self.session.get(Location, id)

    def set(self, id: int, **fields):
        instance = self.session.get(Location, id)
        if not instance:
            return None
        for key, value in fields.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(Location, id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True


class ItemRepository:
    def __init__(self, session):
        self.session = session

    def spawn(
        self,
        mold: Mold,
        owner_id: int,
        manual_params: dict[str, int],
    ):
        manual_params = manual_params or {}
        new_item = Item(
            name=mold.name,
            original_mold_id=mold.id,
            owner_id=owner_id,
            description=mold.description,
        )
        self.session.add(new_item)
        self.session.flush()
        self.populate_item_params(
            mold=mold,
            item=new_item,
            manual_values=manual_params,
        )
        self.session.commit()
        return new_item

    def get_param_max(self, param) -> int:
        return ITEM_PARAM_MAXES[param.name]

    def get_manual_param_defaults(
        self, mold: Mold
    ) -> dict[str:int]:
        params = []
        for spec in mold.param_specs:
            if ITEM_PARAM_MODES[spec.param] != "manual":
                continue
            params.append(
                {
                    "param": spec.param,
                    "value": ITEM_PARAM_DEFAULTS[
                        spec.param
                    ]["base"],
                    "max": ITEM_PARAM_MAXES[spec.param],
                }
            )
        return params

    def destroy_item(self, item):
        self.session.delete(item)
        self.session.commit()

    def get_all_items(
        self, search: str | None = None
    ) -> list[Item]:
        stmt = select(Item)
        if search:
            stmt = stmt.where(
                Item.name.ilike(f"%{search}%")
            )
        return self.session.scalars(stmt).all()

    def get_item_by_id(self, id: int) -> Item:
        return (
            self.session.query(Item)
            .filter(Item.id == id)
            .one()
        )

    def get_original_mold(self, item: Item) -> Mold:
        return (
            self.session.query(Mold)
            .filter(Mold.id == item.original_mold_id)
            .one()
        )

    def add_mold(self, mold: Mold):
        self.session.add(mold)
        self.session.commit()

    def get_mold_by_id(self, mold_id: int):
        return (
            self.session.query(Mold)
            .filter(Mold.id == mold_id)
            .one()
        )

    def update_mold(
        self, mold: Mold, **fields
    ) -> Optional[Mold]:
        for key, value in fields.items():
            setattr(mold, key, value)
        self.session.commit()

    def delete_mold(self, mold: Mold):
        self.session.delete(mold)
        self.session.commit()

    def get_all_molds(
        self, search: str | None = None
    ) -> list[Mold]:
        stmt = select(Mold)
        if search:
            stmt = stmt.where(
                Mold.name.ilike(f"%{search}%")
            )
        return self.session.scalars(stmt).all()

    def populate_item_params(
        self,
        mold: Mold,
        item: Item,
        manual_values: dict[str, float],
    ) -> list[ItemParam]:
        for spec in mold.param_specs:
            base = spec.base
            var = spec.variance
            if ITEM_PARAM_MODES[spec.param] == "manual":
                new_value = manual_values[spec.param]
            elif ITEM_PARAM_MODES[spec.param] == "semi":
                roll = randint(0, 999)
                if roll < 150:
                    new_value = base - var
                elif roll > 899:
                    new_value = base + var
                else:
                    new_value = base
            elif ITEM_PARAM_MODES[spec.param] == "auto":
                new_value = randint(
                    base - 3 * var // 4, base + var // 4
                )
            new_param = ItemParam(
                item_id=item.id,
                name=spec.param,
                value=new_value,
            )
            item.param_list.append(new_param)

    def params_from_tags(self, tags: list[str]) -> set[str]:
        params = set()
        for tag in tags:
            candidates = TAG_TO_PARAMS[tag]
            for param in candidates:
                params.add(param)
        return params

    def default_spec_for_param(self, param: str) -> dict:
        return ITEM_PARAM_DEFAULTS.get(
            param,
            dict(
                base=0.0,
                variance=0.0,
            ),
        )

    def create_specs_from_tags(
        self,
        mold: Mold,
        overwrite: bool = False,
    ) -> list[ParamSpec]:
        tags = [t.strip() for t in mold.tags.split(",")]
        params = self.params_from_tags(tags)
        existing = {
            spec.param: spec for spec in mold.param_specs
        }
        created = []
        for param in params:
            if param in existing and not overwrite:
                continue
            defaults = self.default_spec_for_param(param)
            spec = ParamSpec(
                param=param,
                base=defaults["base"],
                variance=defaults["variance"],
            )
            if param in existing:
                mold.param_specs.remove(existing[param])
            mold.param_specs.append(spec)
            created.append(spec)
        return created

    def validate_specs(
        self,
        mold: Mold,
    ) -> list[str]:
        errors = []
        valid_params = self.params_from_tags(
            mold.tags.split(",")
        )
        for spec in mold.param_specs:
            if spec.param not in valid_params:
                errors.append(
                    f"Param '{spec.param}' not implied by tags"
                )
        return errors
