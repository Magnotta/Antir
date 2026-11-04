from .classes import (
    PhysicalActivityDefinition,
    PhysicalActivityName,
    CoefficientMatrix,
    PhysicalAspect,
    Accident,
)
from core.defs.player import PlayerAttribute


PHYSICAL_ACTIVITIES_DICT: dict[
    str, PhysicalActivityDefinition
] = {
    PhysicalActivityName.HEAVY_TOOL_SWING: PhysicalActivityDefinition(
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
    PhysicalActivityName.HEAVY_TOOL_USE: PhysicalActivityDefinition(
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
        accidents=[
            Accident("slip", ["material"], 5000, 1),
        ],
    ),
    PhysicalActivityName.LIGHT_TOOL_USE: PhysicalActivityDefinition(
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
        accidents=[
            Accident("pinch", ["player_body"], 2000, 0.6),
            Accident("slip", ["material"], 3000, 0.1),
        ],
    ),
    PhysicalActivityName.WORKSTATION_USE: PhysicalActivityDefinition(
        name="workstation_use",
        attr_coeffs=CoefficientMatrix.sparse(
            {
                PhysicalAspect.INTENSITY: {},
                PhysicalAspect.EFFICIENCY: {},
                PhysicalAspect.QUALITY: {},
                PhysicalAspect.SAFETY: {},
            }
        ),
        accidents=[],
    ),
    PhysicalActivityName.ANIMAL_HANDLING: PhysicalActivityDefinition(
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
        accidents=[
            Accident(
                "slip", ["material", "bystander"], 1500, 1
            )
        ],
    ),
    PhysicalActivityName.PUMPING: PhysicalActivityDefinition(
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
        accidents=[
            Accident("slip", ["tool"], 3000, 0.5),
        ],
    ),
    PhysicalActivityName.HAULING: PhysicalActivityDefinition(
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
        accidents=[
            Accident(
                "stumble",
                ["player_body", "material"],
                2500,
                1,
            ),
        ],
    ),
    PhysicalActivityName.LOADING: PhysicalActivityDefinition(
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
        accidents=[
            Accident(
                "slip", ["material", "player_body"], 2000, 1
            )
        ],
    ),
    PhysicalActivityName.PRECISION_STRIKE: PhysicalActivityDefinition(
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
        accidents=[
            Accident(
                "miss",
                ["material", "player_body"],
                700,
                0.7,
            ),
        ],
    ),
    PhysicalActivityName.LOCOMOTION: PhysicalActivityDefinition(
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
        accidents=[
            Accident("stumble", ["player_body"], 3500, 1),
        ],
    ),
    PhysicalActivityName.SPRINTING: PhysicalActivityDefinition(
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
        accidents=[
            Accident("stumble", ["player_body"], 2000, 1),
        ],
    ),
    PhysicalActivityName.JUMPING: PhysicalActivityDefinition(
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
        accidents=[
            Accident("slip", ["player_body"], 4500, 1)
        ],
    ),
    PhysicalActivityName.CLIMBING: PhysicalActivityDefinition(
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
        accidents=[
            Accident("slip", ["player_body"], 1200, 1)
        ],
    ),
    PhysicalActivityName.KNEADING: PhysicalActivityDefinition(
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
        accidents=[],
    ),
    PhysicalActivityName.THROWING: PhysicalActivityDefinition(
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
        accidents=[Accident("miss", ["bystander"], 400, 1)],
    ),
}
