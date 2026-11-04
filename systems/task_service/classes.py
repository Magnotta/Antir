from dataclasses import dataclass, asdict, fields
from typing import Iterator, Mapping
from enum import Enum
from core.defs.player import PlayerAttribute
from systems.item_service.classes import ToolModality


class PhysicalAspect(str, Enum):
    INTENSITY = "intensity"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"
    SAFETY = "safety"


@dataclass(frozen=True)
class CoefficientMatrix:
    """grid of coefficients: PhysicalAspect rows x PlayerAttribute columns."""

    values: dict[
        PhysicalAspect, dict[PlayerAttribute, float]
    ]

    @classmethod
    def zero(cls) -> "CoefficientMatrix":
        return cls(
            {
                p: {a: 0.0 for a in PlayerAttribute}
                for p in PhysicalAspect
            }
        )

    @classmethod
    def identity(cls) -> "CoefficientMatrix":
        """Neutral element for tool matrices — combining with this changes nothing."""
        return cls(
            {
                p: {a: 1.0 for a in PlayerAttribute}
                for p in PhysicalAspect
            }
        )

    @classmethod
    def sparse(
        cls,
        entries: dict[str, dict[str, float]],
        base: "CoefficientMatrix | None" = None,
    ) -> "CoefficientMatrix":
        """Build from only the nonzero/non-identity cells, e.g.
        {"intensity": {"arm_strength": 0.8}, "safety": {"dexterity": 0.5, "arm_strength": 0.2}}
        """
        grid = {
            p: dict(row)
            for p, row in (
                base or cls.zero()
            ).values.items()
        }
        for aspect_name, attrs in entries.items():
            aspect = PhysicalAspect(aspect_name)
            for attr_name, val in attrs.items():
                grid[aspect][
                    PlayerAttribute(attr_name)
                ] = val
        return cls(grid)

    def get(
        self, aspect: PhysicalAspect, attr: PlayerAttribute
    ) -> float:
        return self.values[aspect][attr]

    def row(
        self, aspect: PhysicalAspect
    ) -> dict[PlayerAttribute, float]:
        """All attribute coefficients contributing to a single aspect —
        exactly what upper layers need when computing task intensity/efficiency/etc.
        """
        return self.values[aspect]

    def combine(
        self,
        other: "CoefficientMatrix",
        op=lambda a, b: a * b,
    ) -> "CoefficientMatrix":
        """Elementwise combine two matrices of the same shape — used to layer a
        tool's matrix on top of an activity's base matrix.
        """
        return CoefficientMatrix(
            {
                aspect: {
                    attr: op(
                        self.values[aspect][attr],
                        other.values[aspect][attr],
                    )
                    for attr in PlayerAttribute
                }
                for aspect in PhysicalAspect
            }
        )

    def to_json(self) -> dict:
        return {
            p.value: {a.value: v for a, v in row.items()}
            for p, row in self.values.items()
        }

    @classmethod
    def from_json(cls, data: dict) -> "CoefficientMatrix":
        return cls(
            {
                PhysicalAspect(p): {
                    PlayerAttribute(a): v
                    for a, v in row.items()
                }
                for p, row in data.items()
            }
        )


@dataclass(frozen=True)
class Accident:
    key: str
    targets: list[str]
    threshold: int
    weight: float


class PhysicalActivityName(str, Enum):
    HEAVY_TOOL_SWING = "heavy_tool_swing"
    HEAVY_TOOL_USE = "heavy_tool_use"
    LIGHT_TOOL_USE = "light_tool_use"
    WORKSTATION_USE = "workstation_use"
    ANIMAL_HANDLING = "animal_handling"
    PUMPING = "pumping"
    HAULING = "hauling"
    LOADING = "loading"
    PRECISION_STRIKE = "precision_strike"
    LOCOMOTION = "locomotion"
    SPRINTING = "sprinting"
    JUMPING = "jumping"
    CLIMBING = "climbing"
    KNEADING = "kneading"
    THROWING = "throwing"


@dataclass(frozen=True)
class PhysicalActivityDefinition:
    name: str
    attr_coeffs: CoefficientMatrix
    accidents: list[Accident]


@dataclass(frozen=True)
class AspectVector:
    intensity: float = 1.0
    efficiency: float = 1.0
    quality: float = 1.0
    safety: float = 1.0

    ASPECT_ORDER = (
        PhysicalAspect.INTENSITY,
        PhysicalAspect.EFFICIENCY,
        PhysicalAspect.QUALITY,
        PhysicalAspect.SAFETY,
    )

    __iter__ = None

    def __post_init__(self):
        # Guard: the field names are used as PhysicalAspect values above.
        if [a.value for a in self.ASPECT_ORDER] != [
            f.name for f in fields(AspectVector)
        ]:
            raise RuntimeError(
                "AspectVector fields must match PhysicalAspect values, in order"
            )

    @classmethod
    def ones(cls) -> "AspectVector":
        return cls()

    @classmethod
    def from_tuple(cls, values) -> "AspectVector":
        if len(values) != len(cls.ASPECT_ORDER):
            raise ValueError(
                f"expected {len(cls.ASPECT_ORDER)} values, got {len(values)}"
            )
        return cls(*values)

    @classmethod
    def from_mapping(
        cls, values: Mapping[PhysicalAspect, float]
    ) -> "AspectVector":
        """Aspects missing from `values` stay at 1.0."""
        return cls(
            **{a.value: v for a, v in values.items()}
        )

    def __getitem__(self, aspect: PhysicalAspect) -> float:
        return getattr(self, aspect.value)

    def __mul__(
        self, other: "AspectVector"
    ) -> "AspectVector":
        if not isinstance(other, AspectVector):
            return NotImplemented
        return AspectVector(
            *(self[a] * other[a] for a in self.ASPECT_ORDER)
        )

    def items(
        self,
    ) -> Iterator[tuple[PhysicalAspect, float]]:
        for aspect in self.ASPECT_ORDER:
            yield aspect, self[aspect]

    def to_tuple(self) -> tuple[float, ...]:
        return tuple(self[a] for a in self.ASPECT_ORDER)

    def to_json(self) -> dict:
        return {a.value: v for a, v in self.items()}

    @classmethod
    def from_json(cls, data: dict) -> "AspectVector":
        return cls(**data)


class SkillTrack(str, Enum):
    # --- Extraction & Gathering ---
    WOODCUTTING = "woodcutting"
    MINING = "mining"
    QUARRYING = "quarrying"
    FORAGING = "foraging"
    HERBALISM = "herbalism"
    FISHING = "fishing"
    HUNTING = "hunting"
    TRAPPING = "trapping"

    # --- Agriculture & Animal Husbandry ---
    FARMING = "farming"
    ANIMAL_HUSBANDRY = "animal_husbandry"
    MILKING = "milking"
    SHEARING = "shearing"
    BEEKEEPING = "beekeeping"

    # --- Food Production ---
    BUTCHERY = "butchery"
    COOKING = "cooking"
    BAKING = "baking"
    BREWING = "brewing"
    PRESERVING = "preserving"

    # --- Textiles & Leather ---
    SPINNING = "spinning"
    WEAVING = "weaving"
    TAILORING = "tailoring"
    DYEING = "dyeing"
    TANNING = "tanning"
    LEATHERWORKING = "leatherworking"

    # --- Construction & Woodcraft ---
    CARPENTRY = "carpentry"
    COOPERING = "coopering"
    MASONRY = "masonry"
    THATCHING = "thatching"
    WOODCARVING = "woodcarving"

    # --- Metal & Fine Crafts ---
    SMITHING = "smithing"
    SMELTING = "smelting"
    BOWYER = "bowyer"
    FLETCHING = "fletching"
    POTTERY = "pottery"
    BASKETRY = "basketry"
    GEM_CUTTING = "gem_cutting"
    GLASS_BLOWING = "glass_blowing"

    # --- Domestic & General Labor ---
    DOMESTIC_LABOR = "domestic_labor"
    FIREMAKING = "firemaking"

    # --- Body & Movement ---
    ATHLETICS = "athletics"
    ACROBATICS = "acrobatics"

    # --- Medicine ---
    HERBLORE = "herblore"
    FIRST_AID = "first_aid"

    # --- Combat (kept here since it shares the attribute/exertion machinery) ---
    MELEE_COMBAT = "melee_combat"
    ARCHERY = "archery"
    UNARMED_COMBAT = "unarmed_combat"


@dataclass(frozen=True)
class CooperationProfile:
    key: str
    participants_min: int
    participants_max: int
    coeffs: AspectVector
    aggregation_rules: str


@dataclass(frozen=True)
class TaskOutput:
    mold_id: int
    quality_mapping: str
    quantity: int

    def to_json(self) -> dict:
        return {
            "mold_id": self.mold_id,
            "quality_mapping": self.quality_mapping,
            "quantity": self.quantity,
        }

    @classmethod
    def from_json(cls, data: dict) -> "TaskOutput":
        return cls(
            mold_id=data["mold_id"],
            quality_mapping=data["quality_mapping"],
            quantity=data["quantity"],
        )


class TaskItemRole(str, Enum):
    TOOL = "tool"
    GEAR = "protective_gear"
    MATERIAL = "material"


@dataclass(frozen=True)
class TaskItem:
    item_id: int
    role: TaskItemRole

    def to_json(self) -> dict:
        return {
            "item_id": self.item_id,
            "role": self.role.value,
        }

    @classmethod
    def from_json(cls, data: dict) -> "TaskItem":
        return cls(
            item_id=data["item_id"],
            role=TaskItemRole(data["role"]),
        )


class Interruptibility(str, Enum):
    FREE = "free"  # stop anytime, no penalty, resumes trivially
    RESUMABLE = "resumable"  # can pause, but resuming costs time/quality
    CRITICAL = "critical"  # interruption ruins progress entirely (smelting)


class TriggerPolicy(str, Enum):
    ONCE = "once"
    CONSTANT = "constant"
    ON_SITE_ENTERED = "on_site_entered"


@dataclass(frozen=True)
class Technicality:
    key: str
    explanation: str
    trigger_handle: str
    trigger_policy: TriggerPolicy
    trigger_time: int

    def to_json(self):
        data = asdict(self)
        data["trigger_policy"] = self.trigger_policy.value
        return data


@dataclass(frozen=True)
class TaskPreset:
    name: str
    skill_track: SkillTrack
    activity: PhysicalActivityName
    tool_mode: ToolModality
    metabolic_mult: float
    min_lighting: int
    technicalities: dict[str, Technicality]
    interruptibility: Interruptibility
    notes: str
