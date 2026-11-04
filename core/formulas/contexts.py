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
    sim_time: int
    temperature: int
    wind_latent: int
    precip_latent: int


@dataclass(frozen=True)
class LightingContext:
    enclosure: float
    weather_sunlight: int
    active_sources: list[
        tuple[int, int]
    ]  # (light_output, fuel_remaining) per lit source


@dataclass(frozen=True)
class SiteContext:
    conditions: dict
    light: LightingContext


@dataclass(frozen=True)
class ToolContext:
    params: dict
    tool_name: str
    tool_exp: int


@dataclass(frozen=True)
class ParticipantContext:
    stats: dict
    attrs: dict
    skilltrack_exp: int
    tool_ctx: ToolContext


@dataclass(frozen=True)
class TaskContext:
    task_preset: str
    progress_frac: float
    site_context: SiteContext
