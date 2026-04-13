from random import randint
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models.item import Mold, ParamSpec, Item, ItemParam
from core.defs import (
    TAG_TO_PARAMS,
    ITEM_PARAM_MAXES,
    ITEM_PARAM_MODES,
    ITEM_PARAM_DEFAULTS,
)


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
        stmt = select(Item).options(joinedload(Item.mold))
        if search:
            stmt = stmt.where(
                Item.name.ilike(f"%{search}%")
            )
        a = self.session.scalars(
            stmt.where(Item.destroyed.is_(False))
        ).all()
        return a

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
