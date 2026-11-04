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
<<<<<<< HEAD
    sim_time: int = 0
    temperature: int = 0
    wind_latent: int = 0
    precip_latent: int = 0


@dataclass
=======
    sim_time: int
    temperature: int
    wind_latent: int
    precip_latent: int


@dataclass(frozen=True)
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
class LightingContext:
    enclosure: float
    weather_sunlight: int
    active_sources: list[
        tuple[int, int]
    ]  # (light_output, fuel_remaining) per lit source
<<<<<<< HEAD
=======


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
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
