from systems.task_service.classes import (
    AspectVector,
    PhysicalAspect,
)
from .classes import (
    ItemParamName,
    ToolName,
    ToolModality,
    CoefficientRule,
)


TOOL_EXP_COEFFS_DICT: dict[ToolName, AspectVector] = {
    ToolName.AXE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.HAMMER: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.PICKAXE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.HOE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.MACHETE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SCYTHE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.GLOVES: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.PLAIN: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.APRON: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SAW: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.TONGS: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.DRILL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SHOVEL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.DIGGER: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.PITCHFORK: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SICKLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.KNIFE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SHEARS: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.FISHING_ROD: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.PADDLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SPINDLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.NEEDLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.THIMBLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.TROWEL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.JIG: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.GOUGE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.AWL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BLOWPIPE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BRUSH: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BROOM: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.RAG: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.MORTAR_AND_PESTLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SPLINT: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.ROPE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.POLE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.HARNESS: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.LEASH: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.DART: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.ROCK: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SPEAR: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.SLING: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BOARD: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BOOTS: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BOW: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.CHISEL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.WEDGE: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.NAILS: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.CLEAVER: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.GOGGLES: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BASKET: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BUCKET: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
    ToolName.BARREL: AspectVector.from_tuple(
        (1, 500, 1000, 1500)
    ),
}


TOOL_MODALITY_RULES_DICT: dict[
    ToolModality,
    dict[PhysicalAspect, list[CoefficientRule]],
] = {
    ToolModality.CHOPPING: {
        PhysicalAspect.INTENSITY: [
            CoefficientRule(
                0.95, 1.1, ItemParamName.BALANCE, 1.5
            ),
        ],
        PhysicalAspect.EFFICIENCY: [
            CoefficientRule(
                0.85, 1.5, ItemParamName.SHARPNESS, 2.0
            ),
            CoefficientRule(
                0.95, 1.2, ItemParamName.BALANCE, 1.0
            ),
        ],
        PhysicalAspect.QUALITY: [
            CoefficientRule(
                0.7, 2.0, ItemParamName.SHARPNESS, 2.5
            ),
        ],
        PhysicalAspect.SAFETY: [
            CoefficientRule(
                0.2, 1.5, ItemParamName.DURABILITY, 0.5
            ),
        ],
    }
}
