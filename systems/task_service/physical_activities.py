from dataclasses import dataclass
from core.defs.player import PlayerAttribute
from core.defs.task import PhysicalAspect
from core.defs.task import CoefficientMatrix


@dataclass(frozen=True)
class Accident:
    key: str
    targets: list[str]
    threshold: int
    weight: float


@dataclass(frozen=True)
class PhysicalActivityDefinition:
    name: str
    attr_coeffs: CoefficientMatrix
    exp_coeffs: dict[PhysicalAspect, float]
    accidents: list[Accident]


PHYSICAL_ACTIVITIES_DICT: dict[
    str, PhysicalActivityDefinition
] = {
    "heavy_tool_swing": PhysicalActivityDefinition(
        name="heavy_tool_swing",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: -0.05,
                    PlayerAttribute.ARM_STRENGTH: -0.15,
                    PlayerAttribute.CORE_STRENGTH: -0.05,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.AGILITY: 0.2,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.ARM_STRENGTH: 0.1,
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.2,
                },
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.ARM_STRENGTH: 0.1,
                    PlayerAttribute.AGILITY: 0.2,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.1,
            PhysicalAspect.EFFICIENCY: 0.5,
            PhysicalAspect.QUALITY: 0.6,
            PhysicalAspect.SAFETY: 0.8,
        },
        accidents=[
            Accident(
                "miss",
                ["player_body", "material"],
                1500,
                0.75,
            ),
            Accident(
                "slip",
                ["material", "bystander", "tool"],
                3500,
                0.1,
            ),
        ],
    ),
    "heavy_tool_use": PhysicalActivityDefinition(
        name="heavy_tool_use",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.ARM_STRENGTH: -0.15,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.DEXTERITY: 0.2,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.ARM_STRENGTH: 0.1,
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.15,
                },
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.ARM_STRENGTH: 0.1,
                    PlayerAttribute.DEXTERITY: 0.2,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.2,
            PhysicalAspect.EFFICIENCY: 0.3,
            PhysicalAspect.QUALITY: 0.8,
            PhysicalAspect.SAFETY: 0.6,
        },
        accidents=[
            Accident("slip", ["material"], 5000, 1),
        ],
    ),
    "light_tool_use": PhysicalActivityDefinition(
        name="light_tool_use",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {},
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.DEXTERITY: 0.2,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.DEXTERITY: 0.4,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                    PlayerAttribute.EMOTIONAL_CAMOUFLAGE: -0.1,
                },
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.DEXTERITY: 0.1,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.2,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.0,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.0,
        },
        accidents=[
            Accident("pinch", ["player_body"], 2000, 0.6),
            Accident("slip", ["material"], 3000, 0.1),
        ],
    ),
    "workstation_use": PhysicalActivityDefinition(
        name="workstation_use",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {},
                PhysicalAspect.EFFICIENCY: {},
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {},
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.5,
            PhysicalAspect.EFFICIENCY: 1.0,
            PhysicalAspect.QUALITY: 1.0,
            PhysicalAspect.SAFETY: 1.0,
        },
        accidents=[],
    ),
    "animal_handling": PhysicalActivityDefinition(
        name="animal_handling",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.ARM_STRENGTH: -0.1,
                    PlayerAttribute.AGILITY: -0.15,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.CORE_STRENGTH: 0.1,
                    PlayerAttribute.AGILITY: 0.2,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.15,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.3,
                },
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.4,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.3,
            PhysicalAspect.EFFICIENCY: 0.3,
            PhysicalAspect.QUALITY: 0.5,
            PhysicalAspect.SAFETY: 0.8,
        },
        accidents=[
            Accident(
                "slip", ["material", "bystander"], 1500, 1
            )
        ],
    ),
    "pumping": PhysicalActivityDefinition(
        name="pumping",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: -0.15,
                    PlayerAttribute.ARM_STRENGTH: -0.2,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.AGILITY: 0.3,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.2,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.AGILITY: 0.1,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.4,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.5,
        },
        accidents=[
            Accident("slip", ["tool"], 3000, 0.5),
        ],
    ),
    "hauling": PhysicalActivityDefinition(
        name="hauling",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: -0.15,
                    PlayerAttribute.ARM_STRENGTH: -0.15,
                    PlayerAttribute.CORE_STRENGTH: -0.2,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.HEIGHT: 0.25,
                    PlayerAttribute.AGILITY: 0.1,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                    PlayerAttribute.EMOTIONAL_CAMOUFLAGE: -0.1,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.AGILITY: 0.1,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.15,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.1,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.5,
        },
        accidents=[
            Accident(
                "stumble",
                ["player_body", "material"],
                2500,
                1,
            ),
        ],
    ),
    "loading": PhysicalActivityDefinition(
        name="loading",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.CORE_STRENGTH: -0.1,
                    PlayerAttribute.ARM_STRENGTH: -0.1,
                    PlayerAttribute.WEIGHT: -0.2,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.1,
                    PlayerAttribute.AGILITY: 0.1,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.AGILITY: 0.1,
                    PlayerAttribute.CORE_STRENGTH: 0.1,
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.15,
                    PlayerAttribute.HEIGHT: -0.1,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.1,
            PhysicalAspect.EFFICIENCY: 0.3,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.6,
        },
        accidents=[
            Accident(
                "slip", ["material", "player_body"], 2000, 1
            )
        ],
    ),
    "precision_strike": PhysicalActivityDefinition(
        name="precision_strike",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.ARM_STRENGTH: -0.15,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.ARM_STRENGTH: 0.1,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.DEXTERITY: 0.5,
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.2,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                },
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.DEXTERITY: 0.3,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.1,
            PhysicalAspect.QUALITY: 0.8,
            PhysicalAspect.SAFETY: 0.7,
        },
        accidents=[
            Accident(
                "miss",
                ["material", "player_body"],
                700,
                0.7,
            ),
        ],
    ),
    "locomotion": PhysicalActivityDefinition(
        name="locomotion",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: 0.1,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.AGILITY: 0.3,
                    PlayerAttribute.HEIGHT: 0.1,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.15
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.1,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.3,
        },
        accidents=[
            Accident("stumble", ["player_body"], 3500, 1),
        ],
    ),
    "sprinting": PhysicalActivityDefinition(
        name="sprinting",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: 0.2,
                    PlayerAttribute.CORE_STRENGTH: -0.2,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.AGILITY: 0.3,
                    PlayerAttribute.HEIGHT: 0.2,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.1,
                    PlayerAttribute.AGILITY: 0.1,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.2,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.3,
        },
        accidents=[
            Accident("stumble", ["player_body"], 2000, 1),
        ],
    ),
    "jumping": PhysicalActivityDefinition(
        name="jumping",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.CORE_STRENGTH: -0.15,
                    PlayerAttribute.WEIGHT: 0.25,
                    PlayerAttribute.HEIGHT: -0.1,
                },
                PhysicalAspect.EFFICIENCY: {},
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.CORE_STRENGTH: 0.1,
                    PlayerAttribute.WEIGHT: -0.2,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.1,
            PhysicalAspect.EFFICIENCY: 0.0,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.1,
        },
        accidents=[
            Accident("slip", ["player_body"], 4500, 1)
        ],
    ),
    "climbing": PhysicalActivityDefinition(
        name="climbing",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.WEIGHT: 0.2,
                    PlayerAttribute.CORE_STRENGTH: -0.2,
                    PlayerAttribute.ARM_STRENGTH: -0.05,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.WEIGHT: -0.2,
                    PlayerAttribute.CORE_STRENGTH: 0.2,
                    PlayerAttribute.AGILITY: 0.3,
                },
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.3,
                    PlayerAttribute.CORE_STRENGTH: 0.1,
                    PlayerAttribute.AGILITY: 0.2,
                },
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.2,
            PhysicalAspect.QUALITY: 0.0,
            PhysicalAspect.SAFETY: 0.8,
        },
        accidents=[
            Accident("slip", ["player_body"], 1200, 1)
        ],
    ),
    "kneading": PhysicalActivityDefinition(
        name="kneading",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.ARM_STRENGTH: -0.15,
                },
                PhysicalAspect.EFFICIENCY: {
                    PlayerAttribute.AGILITY: 0.15,
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.2,
                },
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.EMOTIONAL_REGULATION: 0.15,
                    PlayerAttribute.HOLISTIC_THOUGHT: 0.1,
                },
                PhysicalAspect.SAFETY: {},
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: 0.0,
            PhysicalAspect.EFFICIENCY: 0.5,
            PhysicalAspect.QUALITY: 0.9,
            PhysicalAspect.SAFETY: 0.0,
        },
        accidents=[],
    ),
    "throwing": PhysicalActivityDefinition(
        name="throwing",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {
                    PlayerAttribute.ARM_STRENGTH: -0.2,
                    PlayerAttribute.AGILITY: -0.3,
                },
                PhysicalAspect.EFFICIENCY: {},
                PhysicalAspect.QUALITY: {
                    PlayerAttribute.DEXTERITY: 0.6,
                },
                PhysicalAspect.SAFETY: {},
            }
        ),
        exp_coeffs={
            PhysicalAspect.INTENSITY: -0.25,
            PhysicalAspect.EFFICIENCY: 0.0,
            PhysicalAspect.QUALITY: 0.7,
            PhysicalAspect.SAFETY: 0.0,
        },
        accidents=[Accident("miss", ["bystander"], 400, 1)],
    ),
}
"""
            gear=[
            "axe",
            "hammer",
            "pickaxe",
            "hoe",
            "machete",
            "scythe",
            "gloves",
            "plain",
            "apron",
            "saw",
        ],
            gear=[
            "tongs",
            "gloves",
            "drill",
            "shovel",
            "digger",
            "pitchfork",
            "apron",
        ],
        gear=[
            "sickle",
            "gloves",
            "knife",
            "shears",
            "fishing_rod",
            "paddle",
            "spindle",
            "needle",
            "thimble",
            "trowel",
            "jig",
            "gouge",
            "awl",
            "blowpipe",
            "brush",
            "broom",
            "rag",
            "mortar_and_pestle",
            "splint",
            "rope",
            "pole",
        ],
        gear=[
            "harness",
            "leash",
        ],
                gear=[
            "dart",
            "rock",
            "spear",
            "knife",
            "axe",
            "sling",
        ],
                gear=["board",],
                gear=[
            "boots",
            "pole",
        ],
                gear=[
            "boots",
        ],
                gear=[
            "boots",
            "pole",
        ],
                gear=[
            "bow",
            "chisel",
            "wedge",
            "nails",
            "axe",
            "cleaver",
            "hammer",
            "knife",
            "goggles",
            "awl",
            "gloves",
            "apron",
        ],
                gear=[
            "pole",
            "rope",
        ],
                gear=[
            "gloves",
            "boots",
            "basket",
            "bucket",
            "barrel",
        ],
                        gear=[
            "bucket",
        ],
        gear=["shovel"]
"""
