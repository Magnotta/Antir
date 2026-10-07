from dataclasses import dataclass
from db.models.world import Site


@dataclass
class LightingContext:
    enclosure: float
    weather_sunlight: int  # 0-10_000
    active_sources: list[
        tuple[int, int]
    ]  # (light_output, fuel_remaining) per lit source


def gather_lighting_context(
    env: Site, weather, light_repo
) -> LightingContext:
    sources = light_repo.get_lit_sources_with_fuel(env.id)
    return LightingContext(
        enclosure=env.enclosure,
        weather_sunlight=weather.sunlight,
        active_sources=sources,
    )


def calculate_local_light(ctx: LightingContext) -> int:
    sunlight_contribution = ctx.weather_sunlight * (
        1.0 - ctx.enclosure
    )
    artificial_contribution = sum(
        output
        for output, fuel in ctx.active_sources
        if fuel > 0
    )
    return round(
        sunlight_contribution + artificial_contribution
    )
