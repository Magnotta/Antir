from random import randint
from sqlalchemy import select
from typing import Optional
from db.models import (
    PlayerRecord,
    Location,
    BodyNode,
    EquipmentSlot,
    ParamSpec,
    Mold,
    ItemParam,
    Item,
    PlayerStat,
)
from core.defs import (
    TAG_TO_PARAMS,
    ITEM_PARAM_MAXES,
    ITEM_PARAM_MODES,
    ITEM_PARAM_DEFAULTS,
)


class PlayerStatRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self, player_id: int) -> dict[str, float]:
        rows = (
            self.session.query(PlayerStat)
            .filter(PlayerStat.player_id == player_id)
            .all()
        )
        return {row.name: row.value for row in rows}

    def get(self, player_id: int, statname: str) -> int:
        row = (
            self.session.query(PlayerStat)
            .filter(
                PlayerStat.player_id == player_id,
                PlayerStat.name == statname,
            )
            .one()
        )
        return row.value

    def set(self, player_id: int, stat: str, value: float):
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

    def add(self, player_id: int, stat: str, delta: float):
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


class AnatomyRepository:
    def __init__(self, session):
        self.session = session


class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def get(self, id: int):
        return self.session.get(PlayerRecord, id)

    def set(self, id: int, **fields):
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return None
        for key, value in fields.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(PlayerRecord, id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True


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


class SpecRepository:
    def __init__(self, session):
        self.session = session

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


class ParamRepository:
    def __init__(self, session):
        self.session = session

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


class MoldRepository:
    def __init__(self, session):
        self.session = session

    def add(self, mold: Mold):
        self.session.add(mold)
        self.session.commit()

    def update(
        self, mold: Mold, **fields
    ) -> Optional[Mold]:
        for key, value in fields.items():
            setattr(mold, key, value)
        self.session.commit()

    def delete(self, mold: Mold):
        self.session.delete(mold)
        self.session.commit()

    def get_all(
        self, search: str | None = None
    ) -> list[Mold]:
        stmt = select(Mold)
        if search:
            stmt = stmt.where(
                Mold.name.ilike(f"%{search}%")
            )
        return self.session.scalars(stmt).all()


class ItemRepository:
    def __init__(self, session):
        self.session = session

    def spawn(
        self,
        param_repo: ParamRepository,
        mold: Mold,
        owner_id: int,
        manual_params: dict[str, int],
    ):
        manual_params = manual_params or {}
        new_item = Item(
            original_mold_id=mold.id,
            owner_id=owner_id,
            description=mold.description,
        )
        self.session.add(new_item)
        self.session.flush()
        param_repo.populate_item_params(
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

    def destroy(self, item):
        self.session.delete(item)
        self.session.commit()

    def get_loose_items(self, player_id: int):
        equipped_ids = select(EquipmentSlot.item_id).where(
            EquipmentSlot.item_id.isnot(None)
        )
        return (
            self.session.query(Item)
            .filter(Item.owner_id == player_id)
            .filter(Item.container_item_id.is_(None))
            .filter(~Item.id.in_(equipped_ids))
            .all()
        )

    def get_equipped_items(self, player_id: int):
        return (
            self.session.query(EquipmentSlot)
            .join(BodyNode)
            .filter(BodyNode.owner_id == player_id)
            .filter(EquipmentSlot.item_id.isnot(None))
            .all()
        )

    def get_containers(self, player_id: int):
        return (
            self.session.query(Item)
            .filter(Item.owner_id == player_id)
            .filter(Item.contained_items.any())
            .all()
        )

    def get_all(
        self, search: str | None = None
    ) -> list[Item]:
        stmt = select(Item)
        if search:
            stmt = stmt.where(
                Item.name.ilike(f"%{search}%")
            )
        return self.session.scalars(stmt).all()
