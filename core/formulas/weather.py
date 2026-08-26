import math
import numpy as np
from core.formulas.math import clamp
from core.formulas.coefficients import WeatherCoefficients
from core.formulas.contexts import WeatherContext


def weather_noise(step: int) -> tuple[float, float, float]:
    temp_noise = np.random.Generator(
        np.random.Philox(
            seed=0x123456789ABCDEF0, counter=step
        )
    ).standard_normal()
    wind_noise = np.random.Generator(
        np.random.Philox(
            seed=0xFEDCBA9876543210, counter=step
        )
    ).standard_normal()
    precip_noise = np.random.Generator(
        np.random.Philox(
            seed=0x5555555555555555, counter=step
        )
    ).standard_normal()

    return (temp_noise, wind_noise, precip_noise)


def ou_advance(
    x: float,
    mu: float,
    theta: float,
    sigma: float,
    dt: float,
    z: float,
) -> float:
    """Exact OU transition - zero discretization error for any dt.
    z is a standard normal sample, e.g. rng.gauss(0, 1).
    Works identically for a single tick (dt=1) or a multi-day skip (dt=4320).
    """
    decay = math.exp(-theta * dt)
    mean = mu + (x - mu) * decay
    variance = (sigma**2) * (1 - decay**2) / (2 * theta)
    return mean + math.sqrt(variance) * z


def derive_weather(
    ctx: WeatherContext, coeffs: WeatherCoefficients
):
    sim_time = ctx.sim_time
    day_time = sim_time % 1440
    intensity = (
        (day_time - coeffs.sunlight_offset)
        * coeffs.sunlight_duration
        - pow(day_time - coeffs.sunlight_offset, 2)
    ) // coeffs.sunlight_divider
    intensity = clamp(intensity, 0, 10_000)
    temp = ctx.temperature
    wind_latent = ctx.wind_latent
    precip_latent = ctx.precip_latent
    precip = int(max(precip_latent, 0))
    clouds = precip_latent - coeffs.precip_mu
    wind = clamp(wind_latent + precip / 2, 0, 10_000)
    return {
        "temperature": temp,
        "wind_speed": wind,
        "wind_latent": wind_latent,
        "precipitation": precip,
        "precip_latent": precip_latent,
        "sunlight": intensity,
        "cloud_coverage": clouds,
    }


def step_weather(
    ctx: WeatherContext, coeffs: WeatherCoefficients
):
    dt = coeffs.dt

    noise_temp, noise_wind, noise_precip = weather_noise(
        ctx.sim_time
    )

    temp = (
        ctx.temperature
        + coeffs.temp_theta
        * (coeffs.temp_mu - ctx.temperature)
        * dt
        + coeffs.temp_sigma * math.sqrt(dt) * noise_temp
    )
    temp = clamp(temp, -10_000, 10_000)

    precip_latent = (
        ctx.precip_latent
        + coeffs.precip_theta
        * (coeffs.precip_mu - ctx.precip_latent)
        * dt
        + coeffs.precip_sigma * math.sqrt(dt) * noise_precip
    )
    precip_latent = clamp(precip_latent, -10_000, 10_000)

    wind_latent = (
        ctx.wind_latent
        + coeffs.wind_theta
        * (coeffs.wind_mu - ctx.wind_latent)
        * dt
        + coeffs.wind_sigma * math.sqrt(dt) * noise_wind
    )
    wind_latent = clamp(wind_latent, -10_000, 10_000)

    weather_dict = derive_weather(
        WeatherContext(
            sim_time=ctx.sim_time,
            temperature=temp,
            precip_latent=precip_latent,
            wind_latent=wind_latent,
        ),
        coeffs,
    )

    return weather_dict
