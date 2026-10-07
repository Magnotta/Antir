from systems.task_service.physical_activities import (
    PhysicalActivityDefinition,
    PhysicalAspect,
    PlayerAttribute,
)


def base_capability(
    activity: PhysicalActivityDefinition,
    aspect: PhysicalAspect,
    player_attrs: dict[PlayerAttribute, float],
    experience: int,  # 0.0 if skill track doesn't match
) -> int:
    score = 0
    for attr in PlayerAttribute:
        score += int(
            activity.attr_coeffs.get(attr, aspect)
            * player_attrs[attr]
        )
    score += int(activity.exp_coeffs[aspect] * experience)
    return score
