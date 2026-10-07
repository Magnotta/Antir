"""
Location environment resolution.

Two independent concerns, deliberately kept separate:

- Dwelling environment (ambient shelter/ventilation/temperature): only
  meaningful while a player is stationary somewhere -- a locality Site, or
  the Site stretch of a Path they've paused in to do a task. Resolved by
  resolve_dwelling_environment().

- Travel conditions (PointCondition / SegmentCondition on a Path): describe
  what it's like to move *through* a stretch of path -- speed penalties,
  tasks required to get past an obstacle, and hazards to roll for while
  attempting them. They say nothing about shelter/ventilation/temperature.
  Resolved by resolve_travel_conditions().

A player doing a task at a Site uses only the first. A player currently in
transit along a path uses only the second. The two are never merged.
"""

from dataclasses import dataclass, field

from db.models.world import (
    Path,
    PointCondition,
    SegmentCondition,
    Site,
)

POINT_CONDITION_TOLERANCE_M = 20


# ---------------------------------------------------------------------------
# Dwelling environment (ambient exposure while stationary at a Site)
# ---------------------------------------------------------------------------


@dataclass
class DwellingEnvironment:
    site: Site
    rain_shelter: float
    sun_shelter: float
    ventilation: float
    base_temperature_offset: int


def resolve_dwelling_environment(
    site: Site,
) -> DwellingEnvironment:
    """Ambient exposure for a player stationary at `site` -- a locality
    Site, or the Site stretch of a Path they've stopped in. Conditions
    never factor in here; they only describe movement, not dwelling.
    """
    return DwellingEnvironment(
        site=site,
        rain_shelter=site.rain_shelter,
        sun_shelter=site.sun_shelter,
        ventilation=site.ventilation,
        base_temperature_offset=site.base_temperature_offset,
    )


def find_site_at_position(
    path: Path, position: int
) -> Site | None:
    """Which Site stretch (if any) covers `position` meters along `path`.
    Used when a player stops mid-path to do a task and needs a dwelling
    context. Half-open [start, end); assumes authored stretches don't
    overlap and, ideally, tile the whole path with no gaps -- worth a
    separate content-validation pass rather than handling here.
    """
    for candidate in path.sites:  # already ordered by start
        if candidate.start is None or candidate.end is None:
            continue
        if candidate.start <= position < candidate.end:
            return candidate
    return None


# ---------------------------------------------------------------------------
# Travel conditions (obstacles encountered while moving through a Path)
# ---------------------------------------------------------------------------


@dataclass
class ActiveTravelCondition:
    kind: str
    data: dict
    description: str | None
    source: str  # "point" or "segment"
    speed_multiplier: float
    requires_task: str | None


@dataclass
class TravelConditions:
    position: int
    active: list[ActiveTravelCondition] = field(
        default_factory=list
    )

    @property
    def speed_multiplier(self) -> float:
        # Stack multiplicatively -- e.g. muddy (0.7) + bushy_overgrowth
        # (0.7) together => 0.49, not 0.7.
        result = 1.0
        for cond in self.active:
            result *= cond.speed_multiplier
        return result

    @property
    def required_tasks(self) -> list[str]:
        return [
            c.requires_task
            for c in self.active
            if c.requires_task
        ]

    def has(self, kind: str) -> bool:
        return any(c.kind == kind for c in self.active)


# Placeholder travel effects per condition kind. speed_multiplier is 1.0 =
# no penalty; requires_task names a task type that must be completed to
# proceed (None = passable at reduced speed, no task needed). These numbers
# are illustrative -- tune for your game's pacing, and confirm which of the
# flavor-only kinds (scenic_view, landmark, terrain, lakeside) should stay
# at no-effect vs carry some minor drag.
TRAVEL_EFFECTS = {
    "fallen_tree": lambda data: (
        1.0,
        "clear_or_climb_obstacle",
    ),
    "muddy": lambda data: (
        max(0.3, 1 - 0.15 * data.get("depth", 0)),
        None,
    ),
    "washout": lambda data: (0.5, None),
    "gully": lambda data: (0.6, None),
    "exposed_roots": lambda data: (0.85, None),
    "inclination_change": lambda data: (
        max(0.4, 1 - abs(data.get("angle", 0)) / 90),
        None,
    ),
    "thorny_overgrowth": lambda data: (
        0.5,
        "push_through_overgrowth",
    ),
    "fibrous_overgrowth": lambda data: (
        0.6,
        "push_through_overgrowth",
    ),
    "bushy_overgrowth": lambda data: (0.7, None),
    "bridge": lambda data: (1.0, None),
    "river_crossing": lambda data: (0.3, "ford_river"),
    "rock_slide": lambda data: (
        0.4,
        "climb_over_rockslide",
    ),
    "scenic_view": lambda data: (1.0, None),
    "cliff_edge": lambda data: (1.0, None),
    "lakeside": lambda data: (1.0, None),
    "terrain": lambda data: (1.0, None),
    "landmark": lambda data: (1.0, None),
}


def _point_conditions_near(
    path: Path, position: int
) -> list[PointCondition]:
    return [
        c
        for c in path.point_conditions
        if abs(c.position - position)
        <= POINT_CONDITION_TOLERANCE_M
    ]


def _segment_conditions_at(
    path: Path, position: int
) -> list[SegmentCondition]:
    return [
        c
        for c in path.segment_conditions
        if c.start <= position <= c.end
    ]


def resolve_travel_conditions(
    path: Path, position: int
) -> TravelConditions:
    """What a player experiences while moving through `position` meters
    along `path`: active obstacles, combined speed multiplier, and any
    tasks required to proceed. Says nothing about ambient shelter/temp.
    """
    result = TravelConditions(position=position)

    sources: list[
        tuple[str, PointCondition | SegmentCondition]
    ] = [
        ("point", c)
        for c in _point_conditions_near(path, position)
    ] + [
        ("segment", c)
        for c in _segment_conditions_at(path, position)
    ]

    for source, cond in sources:
        effect = TRAVEL_EFFECTS.get(cond.kind)
        speed_multiplier, requires_task = (
            effect(cond.data or {})
            if effect
            else (1.0, None)
        )
        result.active.append(
            ActiveTravelCondition(
                kind=cond.kind,
                data=cond.data or {},
                description=cond.description,
                source=source,
                speed_multiplier=speed_multiplier,
                requires_task=requires_task,
            )
        )

    return result
