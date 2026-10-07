from dataclasses import dataclass
from sqlalchemy.orm import Session
import pprint
from core.world import LOCALITIES, SITES, PATHS, JUNCTIONS
from db.models.player_location import PlayerLocation
from db.models.world import (
    Locality,
    Path,
    Site,
    Junction,
    PointCondition,
    SegmentCondition,
)


from systems.location_service.site_resolver import (
    DwellingEnvironment,
    TravelConditions,
    find_site_at_position,
    resolve_dwelling_environment,
    resolve_travel_conditions,
)


@dataclass
class AdvanceResult:
    location: PlayerLocation
    # Set only on the step that ends travel -- the player crossed into a
    # locality this call. None means they're still mid-path.
    arrived_at: Locality | None


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def update_locality(self, locality_id: int, **kwargs):
        locality = self.session.get(Locality, locality_id)
        if not locality:
            return None
        for key, value in kwargs.items():
            setattr(locality, key, value)
        return locality

    def delete_locality(self, locality_id: int):
        locality = self.session.get(Locality, locality_id)
        if locality:
            self.session.delete(locality)

    def add_locality(
        self, name: str, description=None, data=None
    ) -> Locality:
        locality = Locality(
            name=name, description=description, data=data
        )
        self.session.add(locality)
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
        origin_site: Site,
        destination_site: Site,
        length_m: int,
        description=None,
        data=None,
    ) -> Path:
        path = Path(
            origin_id=origin.id,
            destination_id=destination.id,
            origin_site_id=origin_site.id,
            destination_site_id=destination_site.id,
            length_m=length_m,
            description=description,
            data=data,
        )
        self.session.add(path)
        return path

    def update_path(
        self, path_id: int, **kwargs
    ) -> Path | None:
        path = self.session.get(Path, path_id)
        if not path:
            return None
        for key, value in kwargs.items():
            setattr(path, key, value)
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

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Sites
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def get_site_by_id(self, site_id: int) -> Site | None:
        return self.session.get(Site, site_id)

    def get_all_sites(self) -> list[Site]:
        return (
            self.session.query(Site).order_by(Site.id).all()
        )

    def add_site(
        self,
        *,
        name: str,
        description=None,
        locality: Locality = None,
        path: Path = None,
        start: int = None,
        end: int = None,
    ) -> Site:
        if (locality is None) == (path is None):
            raise ValueError(
                "add_site needs exactly one of locality or path"
            )
        site = Site(
            name=name,
            description=description,
            locality_id=locality.id if locality else None,
            path_id=path.id if path else None,
            start=start,
            end=end,
        )
        self.session.add(site)
        return site

    def update_site(
        self, site_id: int, **kwargs
    ) -> Site | None:
        site = self.session.get(Site, site_id)
        if not site:
            return None
        for key, value in kwargs.items():
            setattr(site, key, value)
        return site

    def delete_site(self, site: Site):
        self.session.delete(site)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Junctions
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def get_junction_by_id(
        self, junction_id: int
    ) -> Junction | None:
        return self.session.get(Junction, junction_id)

    def get_all_junctions(self) -> list[Junction]:
        return (
            self.session.query(Junction)
            .order_by(Junction.id)
            .all()
        )

    def add_junction(
        self,
        *,
        path_a: Path,
        position_a_m: int,
        path_b: Path,
        position_b_m: int,
        description=None,
        data=None,
    ) -> Junction:
        junction = Junction(
            path_a_id=path_a.id,
            position_a_m=position_a_m,
            path_b_id=path_b.id,
            position_b_m=position_b_m,
            description=description,
            data=data,
        )
        self.session.add(junction)
        return junction

    def update_junction(
        self, junction_id: int, **kwargs
    ) -> Junction | None:
        junction = self.session.get(Junction, junction_id)
        if not junction:
            return None
        for key, value in kwargs.items():
            setattr(junction, key, value)
        return junction

    def delete_junction(self, junction: Junction):
        self.session.delete(junction)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Conditions
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

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
        position: int,
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
        return cond

    def add_segment_condition(
        self,
        path_id: int,
        *,
        start: int,
        end: int,
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
        return cond

    def update_condition(self, condition, **kwargs):
        for key, value in kwargs.items():
            setattr(condition, key, value)
        return condition

    def delete_condition(
        self, condition: PointCondition | SegmentCondition
    ):
        self.session.delete(condition)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Export / import
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def export_world_to_file(self):
        text = self._to_python_text()
        with open(
            "./core/world.py", "w", encoding="utf-8"
        ) as f:
            f.write(text)

    def _export_data(self):
        localities = []
        sites = []
        paths = []
        junctions = []

        for loc in self.get_all_localities():
            localities.append(
                {
                    "id": loc.id,
                    "name": loc.name,
                    "description": loc.description,
                    "data": loc.data,
                }
            )

        for site in self.get_all_sites():
            sites.append(
                {
                    "id": site.id,
                    "name": site.name,
                    "description": site.description,
                    "locality_id": site.locality_id,
                    "path_id": site.path_id,
                    "start": site.start,
                    "end": site.end,
                }
            )

        for path in self.get_all_paths():
            point_conditions = []
            segment_conditions = []
            for cond in path.point_conditions:
                point_conditions.append(
                    {
                        "id": cond.id,
                        "kind": cond.kind,
                        "data": cond.data,
                        "description": cond.description,
                        "position": cond.position,
                    }
                )
            for cond in path.segment_conditions:
                segment_conditions.append(
                    {
                        "id": cond.id,
                        "kind": cond.kind,
                        "data": cond.data,
                        "description": cond.description,
                        "start": cond.start,
                        "end": cond.end,
                    }
                )
            paths.append(
                {
                    "id": path.id,
                    "origin_id": path.origin_id,
                    "destination_id": path.destination_id,
                    "origin_site_id": path.origin_site_id,
                    "destination_site_id": path.destination_site_id,
                    "length_m": path.length_m,
                    "description": path.description,
                    "data": path.data,
                    "point_conditions": point_conditions,
                    "segment_conditions": segment_conditions,
                }
            )

        for junction in self.get_all_junctions():
            junctions.append(
                {
                    "id": junction.id,
                    "path_a_id": junction.path_a_id,
                    "position_a_m": junction.position_a_m,
                    "path_b_id": junction.path_b_id,
                    "position_b_m": junction.position_b_m,
                    "description": junction.description,
                    "data": junction.data,
                }
            )

        return {
            "LOCALITIES": localities,
            "SITES": sites,
            "PATHS": paths,
            "JUNCTIONS": junctions,
        }

    def _import_data(self, data: dict):
        """
        Rebuilds the world from scratch, assigning fresh autoincrement
        ids and remapping every cross-reference accordingly. Order
        matters and isn't arbitrary -- Path.origin_site_id/
        destination_site_id require their Sites to already exist, while
        path-anchored Sites (Site.path_id) require their Path to already
        exist, so the two kinds of Site can't be imported as one pass:

          1. Localities
          2. Locality-anchored sites (assumes every Path's origin/
             destination site is locality-anchored, not path-anchored --
             true for entry sites by design, but nothing enforces it)
          3. Paths, plus their point/segment conditions
          4. Path-anchored sites (the "stream of sites" tiling a path)
          5. Junctions
        """
        locality_id_map = {}
        site_id_map = {}
        path_id_map = {}

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

        site_data_list = sorted(
            data.get("SITES", []), key=lambda x: x["id"]
        )
        locality_site_data = [
            s
            for s in site_data_list
            if s.get("locality_id") is not None
        ]
        path_site_data = [
            s
            for s in site_data_list
            if s.get("path_id") is not None
        ]

        for site_data in locality_site_data:
            site = Site(
                name=site_data["name"],
                description=site_data.get("description"),
                locality_id=locality_id_map[
                    site_data["locality_id"]
                ],
            )
            self.session.add(site)
            self.session.flush()
            site_id_map[site_data["id"]] = site.id

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
                origin_site_id=site_id_map[
                    path_data["origin_site_id"]
                ],
                destination_site_id=site_id_map[
                    path_data["destination_site_id"]
                ],
                length_m=path_data.get("length_m"),
                description=path_data.get("description"),
                data=path_data.get("data"),
            )
            self.session.add(path)
            self.session.flush()
            path_id_map[path_data["id"]] = path.id

            for cond_data in path_data.get(
                "point_conditions", []
            ):
                cond = PointCondition(
                    path_id=path.id,
                    kind=cond_data["kind"],
                    position=cond_data["position"],
                    data=cond_data.get("data"),
                    description=cond_data.get(
                        "description"
                    ),
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
                    description=cond_data.get(
                        "description"
                    ),
                )
                self.session.add(cond)

        for site_data in path_site_data:
            site = Site(
                name=site_data["name"],
                description=site_data.get("description"),
                path_id=path_id_map[site_data["path_id"]],
                start=site_data.get("start"),
                end=site_data.get("end"),
            )
            self.session.add(site)
            self.session.flush()
            site_id_map[site_data["id"]] = site.id

        for junction_data in sorted(
            data.get("JUNCTIONS", []), key=lambda x: x["id"]
        ):
            junction = Junction(
                path_a_id=path_id_map[
                    junction_data["path_a_id"]
                ],
                position_a_m=junction_data["position_a_m"],
                path_b_id=path_id_map[
                    junction_data["path_b_id"]
                ],
                position_b_m=junction_data["position_b_m"],
                description=junction_data.get(
                    "description"
                ),
                data=junction_data.get("data"),
            )
            self.session.add(junction)

    def import_world_from_file(self):
        self._import_data(
            {
                "LOCALITIES": LOCALITIES,
                "SITES": SITES,
                "PATHS": PATHS,
                "JUNCTIONS": JUNCTIONS,
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

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Player location
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def get_location(
        self, player_id: int
    ) -> PlayerLocation:
        """The player's current location: the itinerary row with the
        latest arrival_time. Raises (via .one()) if none exists -- every
        player must go through initialize_location() first; a missing row
        here means that never happened, and should surface as a bug, not
        be handled quietly."""
        return (
            self.session.query(PlayerLocation)
            .filter(PlayerLocation.player_id == player_id)
            .order_by(PlayerLocation.arrival_time.desc())
            .limit(1)
            .one()
        )

    def initialize_location(
        self,
        player_id: int,
        site_id: int,
        arrival_time: int,
    ) -> PlayerLocation:
        """Create the player's very first itinerary row. Call once, at
        character creation / game start. Does not check for an existing
        row first -- calling this twice for the same player is a bug, and
        should fail loudly rather than be silently absorbed.
        """
        site = self.session.get(Site, site_id)
        if site is None or site.locality_id is None:
            raise ValueError(
                f"Site {site_id} is not locality-anchored; "
                "a player must start in a locality"
            )
        location = PlayerLocation(
            player_id=player_id,
            location_kind="locality",
            site_id=site_id,
            locality_id=site.locality_id,
            arrival_time=arrival_time,
        )
        self.session.add(location)
        return location

    def set_locality_site(
        self,
        player_id: int,
        site_id: int,
        arrival_time: int,
    ) -> PlayerLocation:
        """Log the player arriving at (or being moved directly to) a
        locality-anchored Site. Always inserts a new itinerary row.
        """
        site = self.session.get(Site, site_id)
        if site is None or site.locality_id is None:
            raise ValueError(
                f"Site {site_id} is not locality-anchored"
            )
        location = PlayerLocation(
            player_id=player_id,
            location_kind="locality",
            site_id=site_id,
            locality_id=site.locality_id,
            arrival_time=arrival_time,
        )
        self.session.add(location)
        return location

    def set_path_site(
        self,
        player_id: int,
        path_id: int,
        path_position: int,
        heading_to_site_id: int,
        arrival_time: int,
    ) -> PlayerLocation:
        """Log the player entering, or continuing along, a Path at
        `path_position`, heading toward `heading_to_site_id` (the locality
        entry Site they're walking to -- either that path's
        origin_entry_site_id or destination_entry_site_id). Always inserts
        a new itinerary row. Used both to start a fresh journey and, from
        advance_on_path, whenever travel crosses into a new tiled Site
        stretch on the same path."""
        path = self.session.get(Path, path_id)
        site = find_site_at_position(path, path_position)
        if site is None:
            raise ValueError(
                f"No Site covers position {path_position} on path {path_id}"
            )
        location = PlayerLocation(
            player_id=player_id,
            location_kind="path",
            site_id=site.id,
            path_id=path_id,
            path_position=path_position,
            heading_to_site_id=heading_to_site_id,
            arrival_time=arrival_time,
        )
        self.session.add(location)
        return location

    def change_path(
        self,
        player_id: int,
        new_path_id: int,
        new_position: int,
        heading_to_site_id: int,
        arrival_time: int,
    ) -> PlayerLocation:
        """Mid-journey switch to a different Path -- e.g. at a fork --
        without first returning to a locality. Structurally this is the
        same insert as set_path_site; kept as its own explicitly named
        method so call sites are unambiguous about intent, and so
        fork-specific validation has an obvious home once your world
        model represents path junctions. It doesn't yet: nothing here
        checks that new_path_id is actually reachable from the player's
        current position, only that they were on *some* path already.
        """
        current = self.get_location(player_id)
        if current.location_kind != "path":
            raise ValueError(
                f"Player {player_id} is not currently on a path"
            )
        return self.set_path_site(
            player_id,
            new_path_id,
            new_position,
            heading_to_site_id,
            arrival_time,
        )

    def advance_on_path(
        self, player_id: int, delta: int, arrival_time: int
    ) -> AdvanceResult:
        """Move the player `delta` meters along their current heading.
        `delta` may be negative (e.g. pushed back by a hazard); movement
        is resolved relative to path start (position 0 = origin), not
        relative to facing direction.

        - Crossing either end of the path ends travel: logs a new
            "locality" row via set_locality_site, using heading_to_site_id
            directly as the arrival site -- no lookup needed, since it
            already IS the target entry site. Any distance past the
            endpoint is discarded.
        - Crossing into a different tiled Site stretch mid-path (without
            leaving the path) logs a new "path" row via set_path_site.
        - Staying within the same Site stretch just updates path_position
            on the current row in place -- no new itinerary row, since no
            site change occurred.
        """
        location = self.get_location(player_id)
        if location.location_kind != "path":
            raise ValueError(
                f"Player {player_id} is not currently on a path"
            )

        path = self.session.get(Path, location.path_id)
        heading_forward = (
            location.heading_to_site_id
            == path.destination_entry_site_id
        )
        signed_delta = delta if heading_forward else -delta
        new_position = location.path_position + signed_delta

        if (
            new_position >= path.length_m
            or new_position <= 0
        ):
            new_row = self.set_locality_site(
                player_id,
                location.heading_to_site_id,
                arrival_time,
            )
            return AdvanceResult(
                location=new_row,
                arrived_at=new_row.locality,
            )

        covering_site = find_site_at_position(
            path, new_position
        )
        if covering_site is None:
            raise ValueError(
                f"No Site covers position {new_position} on path {path.id}"
            )

        if covering_site.id == location.site_id:
            location.path_position = new_position
            return AdvanceResult(
                location=location, arrived_at=None
            )

        new_row = self.set_path_site(
            player_id,
            path.id,
            new_position,
            location.heading_to_site_id,
            arrival_time,
        )
        return AdvanceResult(
            location=new_row, arrived_at=None
        )

    def get_environment(
        self, player_id: int
    ) -> DwellingEnvironment:
        """Ambient dwelling conditions -- always drawn from the player's
        current site, unconditionally, whether they're stationary in a
        locality or mid-transit along a path's tiled Site stretch.
        """
        location = self.get_location(player_id)
        return resolve_dwelling_environment(location.site)

    def get_travel_conditions(
        self, player_id: int
    ) -> TravelConditions:
        """Active path obstacles/speed/required tasks. Only meaningful
        during a path-traversal event -- call this from whatever handles
        the act of moving (an advance step, a travel-hazard check), not as
        part of a general environment query."""
        location = self.get_location(player_id)
        if location.location_kind != "path":
            raise ValueError(
                f"Player {player_id} is not currently traveling a path"
            )
        return resolve_travel_conditions(
            location.path, location.path_position
        )
