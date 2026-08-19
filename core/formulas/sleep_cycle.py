from numpy import pow
from .math import clamp
from .context_gatherers import *
from .coefficients import *


def sleep_delay(
    ctx: SleepContext,
    coeffs: SleepDelayCoefficients = SleepDelayCoefficients(),
) -> int:
    """
    tiredness contribution is capped at 6300
    expects daily normal tiredness of around 1500
    sleepyness uncapped
    anxiety contribution is quadratic, capped at 3400

    Typical day:
    55 - 1250/70 - 2400/100 + 900²/80000 + 900/100
    55 - 18 - 24 + 10 + 9 = 32
    """
    return int(
        coeffs.base_delay
        - clamp(
            ctx.tiredness // coeffs.tiredness_divider,
            0,
            coeffs.tiredness_cap,
        )
        - ctx.sleepyness // coeffs.sleepyness_divider
        + clamp(
            pow(ctx.anxiety, 2) // coeffs.anxiety_divider_1
            + ctx.anxiety // coeffs.anxiety_divider_2,
            0,
            coeffs.anxiety_cap,
        )
        + clamp(
            ctx.heat // coeffs.heat_divider,
            1,
            coeffs.heat_cap,
        )
    )


def wakeup_thresholds(
    sleep_ctx: SleepContext,
    coeffs: WakeupThreshCoefficients,
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
        coeffs.base_pee
        + sleep_ctx.tiredness // coeffs.tiredness_divider_1
    )
    print(f"Pee wakeup threshold = {pee}")
    poo = coeffs.base_poo
    print(f"Poo wakeup threshold = {poo}")
    heat = coeffs.base_heat
    print(f"Heatwakeup threshold = {heat}")
    cold = coeffs.base_cold
    print(f"Cold wakeup threshold = {cold}")
    duration = int(
        min(
            pow(sleep_ctx.tiredness, 2)
            // coeffs.tiredness_divider_2
            + sleep_ctx.tiredness
            // coeffs.tiredness_divider_3
            + coeffs.base_duration,
            coeffs.duration_cap,
        )
    )
    print(f"Expected sleep duration = {duration}")
    return (pee, poo, heat, cold, duration)


def baseline_sleepyness() -> int:
    BASE_HOURLY_SLEEPYNESS = 150
    return BASE_HOURLY_SLEEPYNESS


def wakeup_replenish(
    ctx: AsleepContext,
) -> tuple[int, int, int]:
    """
    expects that 8 hours of sleep will restore 1500 tiredness
    """
    DELTA_DIVIDER_ON_SLEEPYNESS_REPLENISH = 50
    DELTA_MULTIPLIER_ON_SLEEPYNESS_REPLENISH = 2
    delta = abs(ctx.sleep_until - ctx.time_now)
    sleep_ref = ctx.sleep_until - ctx.sleeping_since
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
