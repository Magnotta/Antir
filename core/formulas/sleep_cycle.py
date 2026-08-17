from numpy import pow
from .math import clamp
from .context_gatherers import *


def sleep_delay(ctx: SleepContext) -> int:
    """
    tiredness contribution is capped at 6300
    expects daily normal tiredness of around 1500
    sleepyness uncapped
    anxiety contribution is quadratic, capped at 3400

    Typical day:
    55 - 1250/70 - 2400/100 + 900²/80000 + 900/100
    55 - 18 - 24 + 10 + 9 = 32
    """
    BASE_DELAY = 55
    TIREDNESS_DIVIDER_ON_DELAY = 70
    TIREDNESS_CAP_ON_DELAY = 90
    SLEEPYNESS_DIVIDER_ON_DELAY = 100
    ANXIETY_DIVIDER_ON_DELAY_1 = 80000
    ANXIETY_DIVIDER_ON_DELAY_2 = 100
    ANXIETY_CAP_ON_DELAY = 180
    HEAT_DIVIDER_ON_DELAY = 40
    HEAT_CAP_ON_DELAY = 60
    return int(
        BASE_DELAY
        - clamp(
            ctx.tiredness // TIREDNESS_DIVIDER_ON_DELAY,
            0,
            TIREDNESS_CAP_ON_DELAY,
        )
        - ctx.sleepyness // SLEEPYNESS_DIVIDER_ON_DELAY
        + clamp(
            pow(ctx.anxiety, 2)
            // ANXIETY_DIVIDER_ON_DELAY_1
            + ctx.anxiety // ANXIETY_DIVIDER_ON_DELAY_2,
            0,
            ANXIETY_CAP_ON_DELAY,
        )
        + clamp(
            ctx.heat // HEAT_DIVIDER_ON_DELAY,
            1,
            HEAT_CAP_ON_DELAY,
        )
    )


def wakeup_thresholds(
    sleep_ctx: SleepContext,
) -> tuple[int, int, int, int, int]:
    """
    pee expects about 2000 pee per 8 hours
    """
    BASE_PEE_WAKEUP_THRESH = 600
    TIREDNESS_DIVIDER_ON_WAKEUP_THRESH = 5
    BASE_POO_WAKEUP_THRESH = 2500
    BASE_HEAT_WAKEUP_THRESH = 2000
    BASE_COLD_WAKEUP_THRESH = 1500
    pee = (
        BASE_PEE_WAKEUP_THRESH
        + sleep_ctx.tiredness
        // TIREDNESS_DIVIDER_ON_WAKEUP_THRESH
    )
    print(f"Pee wakeup threshold = {pee}")
    poo = BASE_POO_WAKEUP_THRESH
    print(f"Poo wakeup threshold = {poo}")
    heat = BASE_HEAT_WAKEUP_THRESH
    print(f"Heatwakeup threshold = {heat}")
    cold = BASE_COLD_WAKEUP_THRESH
    print(f"Cold wakeup threshold = {cold}")
    duration = clamp(
        pow(sleep_ctx.tiredness, 2) // 415000
        + sleep_ctx.tiredness // 50
        + 420,
        420,
        720,
    )
    print(f"Expected sleep duration = {duration}")
    return (pee, poo, heat, cold, duration)


def baseline_sleepyness() -> int:
    BASE_HOURLY_SLEEPYNESS = 150
    return BASE_HOURLY_SLEEPYNESS


def wakeup_replenish(
    sleeping_since: int,
    cur_time: int,
    ref_time: int,
    ctx: SleepContext,
) -> tuple[int, int, int]:
    """
    expects that 8 hours of sleep will restore 1500 tiredness
    """
    DELTA_DIVIDER_ON_SLEEPYNESS_REPLENISH = 50
    DELTA_MULTIPLIER_ON_SLEEPYNESS_REPLENISH = 2
    delta = abs(ref_time - cur_time)
    sleep_ref = ref_time - sleeping_since
    print(f"sleep delta: {delta}")
    sleepyness = clamp(
        pow(delta, 2)
        // DELTA_DIVIDER_ON_SLEEPYNESS_REPLENISH
        + delta * DELTA_MULTIPLIER_ON_SLEEPYNESS_REPLENISH,
        0,
        1000,
    )
    if delta < 30:
        tiredness = 0
    else:
        tiredness = ctx.tiredness * delta // sleep_ref
    anxiety = ctx.anxiety * 9 // 10
    return (sleepyness, tiredness, anxiety)
