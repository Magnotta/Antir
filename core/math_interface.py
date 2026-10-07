from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player.domain import Player
    from core.game_state import GameState
    from db.models.weather_snapshot import WeatherSnapshot
import math
from core.formulas.contexts import *
from core.formulas.coefficients import *
from core.time import Time


def gather_sleep_context(player: Player) -> SleepContext:
    return SleepContext(
        tiredness=player.stats.get("tiredness"),
        sleepyness=player.stats.get("sleepyness"),
        anxiety=player.stats.get("anxiety"),
        heat=player.stats.get("heat"),
    )


def gather_asleep_context(
    state: GameState, player: Player
) -> AsleepContext:
    return AsleepContext(
        tiredness=player.stats.get("tiredness"),
        sleepyness=player.stats.get("sleepyness"),
        anxiety=player.stats.get("anxiety"),
        heat=player.stats.get("heat"),
        sleeping_since=player.sleeping_since.tick,
        sleep_until=player.sleep_ref.tick,
        sim_time=state.time.tick,
    )


def gather_thirst_context(player: Player) -> ThirstContext:
    return ThirstContext(sweat=player.stats.get("sweat"))


def gather_pneuma_context(player: Player) -> PneumaContext:
    return PneumaContext(
        hunger=player.stats.get("hunger"),
        thirst=player.stats.get("thirst"),
    )


def gather_weather_context(
    state: GameState,
) -> WeatherContext:
    return WeatherContext(
        sim_time=state.time.tick,
        temperature=state.weather.temperature,
        wind_latent=state.weather.wind_latent,
        precip_latent=state.weather.precip_latent,
    )


def calculate_wakeupthresh_coeffs(
    player: Player,
) -> WakeupThreshCoefficients:
    base_dur = (
        450 - player.stats.get_attr("vitality") // 167
    )
    print(f"base sleep duration = {base_dur}")
    return WakeupThreshCoefficients(base_duration=base_dur)


def calculate_sleepdedlay_coeffs(
    player: Player,
) -> SleepDelayCoefficients:
    return SleepDelayCoefficients()


def calculate_weather_coeffs(
    sim_time: int,
) -> WeatherCoefficients:
    """
    Builds coefficients for a specific sim_time.
    Override any parameter (e.g., temp_theta) via keyword arguments
    to create different biomes.
    """
    base_temp = 1000.0  # Base comfortable temperature

    annual_temp_ampl = (
        1800.0  # Annual temperature oscillation
    )
    annual_temp_phase = 0.0

    daily_temp_ampl = (
        2100.0  # Daily temperature oscillation
    )
    daily_temp_phase = (
        -math.pi / 2  # Daily temperature oscillation
    )

    temp_mu = (
        base_temp
        + annual_temp_ampl
        * math.sin(
            2
            * math.pi
            * (sim_time + annual_temp_phase)
            / Time.TICKS_PER_YEAR
        )
        + daily_temp_ampl
        * math.sin(
            daily_temp_phase
            + 2 * math.pi * sim_time / Time.TICKS_PER_DAY
        )
    )

    base_precip_mu = (
        -3100.0
    )  # Baseline negative so it stays dry most of the time
    annual_precip_ampl = (
        1800.0  # Annual precipitation oscillation
    )
    annual_precip_phase = (
        math.pi / 4
    )  # Annual precipitation oscillation

    precip_mu = (
        base_precip_mu
        + annual_precip_ampl
        * math.sin(
            2 * math.pi * sim_time / Time.TICKS_PER_YEAR
            + annual_precip_phase
        )
    )

    return WeatherCoefficients(
        temp_mu=temp_mu, precip_mu=precip_mu
    )


def weather_ctx_from_snapshot(
    snap: WeatherSnapshot,
) -> WeatherContext:
    return WeatherContext(
        sim_time=snap.tick,
        temperature=snap.temperature,
        wind_latent=snap.wind_latent,
        precip_latent=snap.precip_latent,
    )
