from dataclasses import dataclass
from player.domain import Player


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

    @classmethod
    def calculate(cls, player: Player):
        return cls()


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

    @classmethod
    def calculate(cls, player: Player):
        base_dur = (
            450 - player.stats.get_attr("vitality") // 167
        )
        print(f"base sleep duration = {base_dur}")
        return cls(base_duration=base_dur)
