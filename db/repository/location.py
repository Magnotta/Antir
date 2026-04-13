import pprint
from core.world import LOCALITIES, PATHS
from db.models.world import (
    Locality,
    Path,
    PointCondition,
    SegmentCondition,
)


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
