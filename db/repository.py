import pprint
from random import randint
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from db.models import (
    EventRecord,
    PlayerRecord,
    Locality,
    Path,
    PointCondition,
    SegmentCondition,
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
from core.world import LOCALITIES, PATHS


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


class LocationRepository:
    def __init__(self, session):
        self.session = session

    def update_locality(self, locality_id: int, **kwargs):
        locality = self.session.get(Locality, locality_id)
        if not locality:
            return None
        for key, value in kwargs.items():
            setattr(locality, key, value)
        self.session.commit()
        self.session.refresh(locality)
        return locality

    def delete_locality(self, locality_id: int):
        locality = self.session.get(Locality, locality_id)
        if locality:
            self.session.delete(locality)
            self.session.commit()

    def add_locality(
        self, name: str, description=None, data=None
    ) -> Locality:
        locality = Locality(
            name=name, description=description, data=data
        )
        self.session.add(locality)
        self.session.commit()
        self.session.refresh(locality)
        return locality

    def get_locality_by_id(
        self, locality_id: int
    ) -> Locality | None:
        return self.session.get(Locality, locality_id)

    def get_locality_by_name(
        self, name: str
    ) -> Locality | None:
        return (
            self.session.query(Locality)
            .filter_by(name=name)
            .one_or_none()
        )

    def get_all_localities(self):
        return (
            self.session.query(Locality)
            .order_by(Locality.id)
            .all()
        )

    def get_path_by_id(self, path_id: int) -> Path:
        return self.session.get(Path, path_id)

    def add_path(
        self,
        origin: Locality,
        destination: Locality,
        *,
        distance_km: float,
        description=None,
        data=None,
    ) -> Path:
        path = Path(
            origin_id=origin.id,
            destination_id=destination.id,
            distance_km=distance_km,
            description=description,
            data=data,
        )
        self.session.add(path)
        self.session.commit()
        self.session.refresh(path)
        return path

    def get_paths_from(
        self, locality: Locality
    ) -> list[Path]:
        return (
            self.session.query(Path)
            .filter(Path.origin_id == locality.id)
            .all()
        )

    def get_all_paths(self):
        return (
            self.session.query(Path).order_by(Path.id).all()
        )

    def get_condition_by_id(
        self, condition_id: int
    ) -> PointCondition | SegmentCondition:
        condition = self.session.get(
            PointCondition, condition_id
        )
        if not condition:
            condition = self.session.get(
                SegmentCondition, condition_id
            )
        return condition

    def add_point_condition(
        self,
        *,
        path_id: int,
        position: float,
        kind: str,
        data=None,
        description=None,
    ) -> PointCondition:
        cond = PointCondition(
            path_id=path_id,
            position=position,
            kind=kind,
            data=data,
            description=description,
        )
        self.session.add(cond)
        self.session.flush()
        path = self.get_path_by_id(path_id)
        path.point_conditions.append(cond)
        self.session.commit()
        self.session.refresh(cond)
        print(cond.id)
        return cond

    def add_segment_condition(
        self,
        path_id: int,
        *,
        start: float,
        end: float,
        kind: str,
        data=None,
        description=None,
    ) -> SegmentCondition:
        cond = SegmentCondition(
            path_id=path_id,
            start=start,
            end=end,
            kind=kind,
            data=data,
            description=description,
        )
        self.session.add(cond)
        self.session.flush()
        path = self.get_path_by_id(path_id)
        path.segment_conditions.append(cond)
        self.session.commit()
        self.session.refresh(cond)
        print(cond.id)
        return cond

    def update_condition(self, condition, **kwargs):
        for key, value in kwargs.items():
            setattr(condition, key, value)
        self.session.commit()
        self.session.refresh(condition)
        return condition

    def delete_condition(
        self, condition: PointCondition | SegmentCondition
    ):
        self.session.delete(condition)
        self.session.commit()

    def export_world_to_file(self):
        text = self._to_python_text()
        with open(
            "./core/world.py", "w", encoding="utf-8"
        ) as f:
            f.write(text)

    def _export_data(self):
        localities = []
        paths = []
        for loc in self.get_all_localities():
            localities.append(
                {
                    "id": loc.id,
                    "name": loc.name,
                    "description": loc.description,
                    "data": loc.data,
                }
            )
        for path in self.get_all_paths():
            point_conditions = []
            segment_conditions = []
            for cond in path.point_conditions:
                cond_dict = {
                    "id": cond.id,
                    "path_id": cond.path_id,
                    "kind": cond.kind,
                    "data": cond.data,
                    "description": cond.description,
                    "position": cond.position,
                }
                point_conditions.append(cond_dict)
            for cond in path.segment_conditions:
                cond_dict = {
                    "id": cond.id,
                    "path_id": cond.path_id,
                    "kind": cond.kind,
                    "data": cond.data,
                    "description": cond.description,
                    "start": cond.start,
                    "end": cond.end,
                }
                segment_conditions.append(cond_dict)
            paths.append(
                {
                    "id": path.id,
                    "origin_id": path.origin_id,
                    "destination_id": path.destination_id,
                    "distance_km": path.distance_km,
                    "description": path.description,
                    "data": path.data,
                    "point_conditions": point_conditions,
                    "segment_conditions": segment_conditions,
                }
            )
        return {
            "LOCALITIES": localities,
            "PATHS": paths,
        }

    def _import_data(self, data: dict):
        locality_id_map = {}
        for loc_data in sorted(
            data.get("LOCALITIES", []),
            key=lambda x: x["id"],
        ):
            locality = Locality(
                name=loc_data["name"],
                description=loc_data.get("description"),
                data=loc_data.get("data"),
            )
            self.session.add(locality)
            self.session.flush()
            locality_id_map[loc_data["id"]] = locality.id

        for path_data in sorted(
            data.get("PATHS", []), key=lambda x: x["id"]
        ):
            path = Path(
                origin_id=locality_id_map[
                    path_data["origin_id"]
                ],
                destination_id=locality_id_map[
                    path_data["destination_id"]
                ],
                distance_km=path_data.get("distance_km"),
                description=path_data.get("description"),
                data=path_data.get("data"),
            )
            self.session.add(path)
            self.session.flush()
            for cond_data in path_data.get(
                "point_conditions", []
            ):
                cond = PointCondition(
                    path_id=path.id,
                    kind=cond_data["kind"],
                    position=cond_data["position"],
                    data=cond_data.get("data"),
                )
                self.session.add(cond)
            for cond_data in path_data.get(
                "segment_conditions", []
            ):
                cond = SegmentCondition(
                    path_id=path.id,
                    kind=cond_data["kind"],
                    start=cond_data["start"],
                    end=cond_data["end"],
                    data=cond_data.get("data"),
                )
                self.session.add(cond)
        self.session.commit()

    def import_world_from_file(self):
        self._import_data(
            {
                "LOCALITIES": LOCALITIES,
                "PATHS": PATHS,
            }
        )

    def _to_python_text(self):
        data = self._export_data()
        text = []
        text.append("# Auto-generated world export\n\n")
        for key, value in data.items():
            text.append(f"{key} = ")
            text.append(pprint.pformat(value, indent=4))
            text.append("\n\n")
        return "".join(text)


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
            destroyed=False,
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
        item.destroyed = True
        self.session.commit()

    def get_extant_items(
        self, search: str | None = None
    ) -> list[Item]:
        stmt = select(Item)
        if search:
            stmt = stmt.where(
                Item.name.ilike(f"%{search}%")
            )
        return self.session.scalars(
            stmt.where(Item.destroyed.is_(False))
        ).all()

    def get_item_by_id(self, item_id: int) -> Item:
        return self.session.get(Item, item_id)

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
        return self.session.get(Mold, mold_id)

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

    def item_chown(self, item_id, new_owner_id):
        item = self.get_item_by_id(item_id)
        if item.owner_id == new_owner_id:
            raise ValueError("Specify a new owner!")
            return
        item.owner_id = new_owner_id
        self.session.commit()

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
