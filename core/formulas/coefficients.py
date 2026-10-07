from dataclasses import dataclass
from core.time import Time


@dataclass(frozen=True)
class SleepDelayCoefficients:
    base_delay: int = 55  # c_11
    tiredness_divider: int = 70  # c_12
    tiredness_cap: int = 90  # c_13
    sleepyness_divider: int = 100  # c_14
    anxiety_divider_1: int = 80_000  # c_15
    anxiety_divider_2: int = 100  # c_16
    anxiety_cap: int = 180  # c_17
    heat_divider: int = 40  # c_18
    heat_cap: int = 60  # c_19


@dataclass(frozen=True)
class WakeupThreshCoefficients:
    base_pee: int = 600  # c_1
    tiredness_divider_1: int = 5  # c_2
    tiredness_divider_2: int = 415_000  # c_6
    tiredness_divider_3: int = 50  # c_7
    base_duration: int = 0  # c_8
    duration_cap: int = 720  # c_9
    base_poo: int = 2500  # c_3
    base_heat: int = 2000  # c_4
    base_cold: int = 1500  # c_5


@dataclass(frozen=True)
class WeatherCoefficients:
    dt: float = 5.0

    sunlight_duration: int = 720
    sunlight_divider: int = 13
    sunlight_offset: int = (
        Time.TICKS_PER_DAY - sunlight_duration
    ) // 2

    temp_mu: float = 0000.0  # Long-term average
    temp_theta: float = (
        0.0035  # Speed of reversion (higher = faster return to average)
    )
    temp_sigma: float = (
        60.0  # Volatility (magnitude of random swings)
    )

    wind_mu: float = 1000.0
    wind_theta: float = 0.001
    wind_sigma: float = 25.0

    precip_mu: float = -4000.0  # Average intensity
    precip_theta: float = (
        0.0004  # Reversion speed for moisture
    )
    precip_sigma: float = (
        70.0  # High volatility allows sudden storms
    )
