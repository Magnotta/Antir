from .context_gatherers import *


def base_thirst(ctx: ThirstContext) -> int:
    BASE_HOURLY_THIRST = 33
    SWEAT_DIVIDER_ON_THIRST = 1
    return (
        BASE_HOURLY_THIRST
        + ctx.sweat // SWEAT_DIVIDER_ON_THIRST
    )


def base_pneuma(ctx: PneumaContext) -> int:
    BASE_DAILY_PNEUMA = -50
    THIRST_DIVIDER_ON_PNEUMA = 5
    HUNGER_DIVIDER_ON_PNEUMA = 2
    return (
        BASE_DAILY_PNEUMA
        + ctx.hunger // HUNGER_DIVIDER_ON_PNEUMA
        + ctx.thirst // THIRST_DIVIDER_ON_PNEUMA
    )


def base_hunger() -> int:
    BASE_HUNGER_TICK = 100
    return BASE_HUNGER_TICK
