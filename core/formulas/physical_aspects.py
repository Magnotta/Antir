import math
from systems.task_service.task import (
    SKILLTRACK_EXP_COEFFS_DICT,
    AspectVector,
)
from systems.task_service.physical_activities import (
    PHYSICAL_ACTIVITIES_DICT,
)
from systems.task_service.presets import TASK_PRESETS_DICT
from core.defs.player import PLAYER_ATTRIBUTE_MAX
from core.formulas.math import expm
from core.formulas.contexts import (
    TaskContext,
    ParticipantContext,
)
from systems.item_service.tools import (
    TOOL_EXP_COEFFS_DICT,
    TOOL_MODALITY_RULES_DICT,
    ToolName,
)


SKILLTRANSFER = 0.2


def aggregate_aspects(
    task_ctx: TaskContext,
    participant_ctx: ParticipantContext,
) -> AspectVector:
    preset = TASK_PRESETS_DICT[task_ctx.task_preset]
    activity = PHYSICAL_ACTIVITIES_DICT[preset.activity]
    skilltrack_exp_vec = SKILLTRACK_EXP_COEFFS_DICT[
        preset.skill_track
    ]
    tool_rules_dict = TOOL_MODALITY_RULES_DICT[
        preset.tool_mode
    ]
    aggregated = []
    for aspect in AspectVector.ASPECT_ORDER:
        skill_exp_coeff = expm(
            participant_ctx.skilltrack_exp,
            int(skilltrack_exp_vec[aspect]),
        )
        attr_coeff = math.fsum(
            pre_coeff
            * participant_ctx.attrs[attr]
            / PLAYER_ATTRIBUTE_MAX
            for attr, pre_coeff in activity.attr_coeffs.row(
                aspect
            ).items()
        )
        base_coeff = math.fsum(
            (1.0, attr_coeff, skill_exp_coeff)
        )
        tool_exp_coeff = expm(
            max(
                participant_ctx.tool_ctx.tool_exp,
                int(
                    participant_ctx.skilltrack_exp
                    * SKILLTRANSFER
                ),
            ),
            int(
                TOOL_EXP_COEFFS_DICT[
                    ToolName(
                        participant_ctx.tool_ctx.tool_name
                    )
                ][aspect]
            ),
        )
        tool_coeff = math.prod(
            rule.value(
                participant_ctx.tool_ctx.params,
                tool_exp_coeff,
            )
            for rule in tool_rules_dict.get(aspect, [])
        )
        aggregated.append(base_coeff * tool_coeff)
    return AspectVector.from_tuple(aggregated)
