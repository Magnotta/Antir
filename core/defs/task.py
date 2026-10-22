from dataclasses import dataclass
from enum import Enum
from core.defs.player import PlayerAttribute


class PhysicalAspect(str, Enum):
    INTENSITY = "intensity"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"
    SAFETY = "safety"


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
    ACCROBATICS = "accrobatics"

    # --- Medicine ---
    HERBLORE = "herblore"
    FIRST_AID = "first_aid"

    # --- Combat (kept here since it shares the attribute/exertion machinery) ---
    MELEE_COMBAT = "melee_combat"
    ARCHERY = "archery"
    UNARMED_COMBAT = "unarmed_combat"


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
class CooperationProfile:
    key: str
    participants_min: int
    participants_max: int
    coeffs: CoefficientMatrix
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


@dataclass(frozen=True)
class ToolProfile:
    name: str
    matrices: dict[str, CoefficientMatrix]

    def usable_for(self, activity: str) -> bool:
        return activity in self.matrices.keys()

    def effective_matrix(
        self, activity: str, condition: float = 1.0
    ) -> CoefficientMatrix:
        """The tool's matrix after wear.

        Tool matrices are multipliers (identity = no effect), so a worn tool
        must fade *toward identity*, not toward zero -- scaling to zero would
        wipe out the activity itself. condition 1.0 -> the full matrix,
        0.0 -> identity (a broken tool is no better than bare hands).
        """
        condition = min(max(condition, 0.0), 1.0)
        return CoefficientMatrix.identity().combine(
            self.matrices[activity],
            op=lambda one, m: one + (m - one) * condition,
        )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "matrices": {
                activity: matrix.to_json()
                for activity, matrix in self.matrices.items()
            },
        }

    @classmethod
    def from_json(cls, data: dict) -> "ToolProfile":
        return cls(
            max_durability=data["max_durability"],
            matrices={
                activity: CoefficientMatrix.from_json(
                    matrix
                )
                for activity, matrix in data[
                    "matrices"
                ].items()
            },
        )
