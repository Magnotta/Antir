from dataclasses import dataclass


@dataclass(frozen=True)
class SleepContext:
    tiredness: int
    sleepyness: int
    anxiety: int
    heat: int


@dataclass(frozen=True)
class AsleepContext:
    tiredness: int
    sleepyness: int
    anxiety: int
    heat: int
    sleeping_since: int
    sleep_until: int
    sim_time: int


@dataclass(frozen=True)
class ThirstContext:
    sweat: int


@dataclass(frozen=True)
class PneumaContext:
    hunger: int
    thirst: int


@dataclass(frozen=True)
class WeatherContext:
    sim_time: int = 0
    temperature: int = 0
    wind_latent: int = 0
    precip_latent: int = 0
