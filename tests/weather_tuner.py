import matplotlib.pyplot as plt
from core.math_interface import calculate_weather_coeffs
from core.formulas.contexts import WeatherContext
from core.formulas.weather import step_weather
import numpy as np

TICKS_PER_YEAR = 525600

# ---------------------------------------------------------------------
# Simulation Loop
# ---------------------------------------------------------------------


def simulate_and_plot(
    total_ticks: int = TICKS_PER_YEAR * 2,
):
    # Initialize at tick 0 with neutral values.
    init_time = 1440 * 15

    times = []
    temps = []
    temp_mus = []
    winds = []
    latent_precip = []
    rain_intensity = []
    precip_mus = []
    clouds = []

    saved_temp = 0
    saved_precip = 0
    saved_wind = 0
    # We'll simulate every 5 ticks, but step by 5.
    # To keep the plot size manageable, we'll sample every 5 ticks (which matches the call frequency).
    steps = range(init_time, total_ticks + init_time, 5)

    for t in steps:
        # 1. Get coefficients for this exact sim_time.
        coeffs = calculate_weather_coeffs(t)

        # 2. Ensure the context has the correct sim_time for noise generation.
        ctx = WeatherContext(
            sim_time=t,
            temperature=saved_temp,
            wind_latent=saved_wind,
            precip_latent=saved_precip,
        )

        # 3. Step the weather.
        dict = step_weather(ctx, coeffs)

        saved_temp = dict["temperature"]
        saved_wind = dict["wind_latent"]
        saved_precip = dict["precip_latent"]

        # 4. Store data.
        times.append(t)
        temps.append(dict["temperature"])
        temp_mus.append(coeffs.temp_mu)
        winds.append(dict["wind_speed"])
        latent_precip.append(dict["precip_latent"])
        rain_intensity.append(max(0, dict["precipitation"]))
        precip_mus.append(coeffs.precip_mu)
        clouds.append(dict["cloud_coverage"])

    # --- Plotting ---
    times_days = np.array(times) / 1440.0
    fig, axes = plt.subplots(
        4, 1, figsize=(16, 12), sharex=True
    )

    # 1. Temperature
    axes[0].plot(
        times_days,
        temps,
        color='red',
        linewidth=1.0,
        label='Actual Temperature',
    )
    axes[0].plot(
        times_days,
        temp_mus,
        color='orange',
        linestyle='--',
        linewidth=1.5,
        label='Dynamic μ (Seasonal + Daily)',
    )
    axes[0].set_ylabel('Temperature (0..10000)')
    axes[0].set_title(
        'Temperature: Daily Oscillation (200x smaller) + Seasonal Cycle'
    )
    # axes[0].legend()
    axes[0].grid(alpha=0.3)

    # 2. Wind Speed
    axes[1].plot(
        times_days, winds, color='blue', linewidth=1.0
    )
    axes[1].axhline(
        y=coeffs.wind_mu,
        color='blue',
        linestyle='--',
        alpha=0.5,
        label='Wind μ (constant)',
    )
    axes[1].set_ylabel('Wind Speed (0..10000)')
    axes[1].set_title('Wind Speed')
    # axes[1].legend()
    axes[1].grid(alpha=0.3)

    # 3. Precipitation (Latent vs Rain)
    axes[2].plot(
        times_days,
        latent_precip,
        color='grey',
        linewidth=0.8,
        alpha=0.5,
        label='Latent State (can be negative)',
    )
    axes[2].fill_between(
        times_days,
        0,
        rain_intensity,
        color='deepskyblue',
        alpha=0.6,
        label='Rain Intensity (max(0, latent))',
    )
    # Plot the dynamic precip_mu to show rainy/dry seasons
    axes[2].plot(
        times_days,
        precip_mus,
        color='darkblue',
        linestyle=':',
        linewidth=1.5,
        label='Dynamic Precip μ',
    )
    axes[2].axhline(y=0, color='black', linewidth=0.5)
    axes[2].set_ylabel('Precipitation (0..10000)')
    axes[2].set_title(
        'Precipitation: Latent OU with Negative μ & Seasonal Shift'
    )
    # axes[2].legend()
    axes[2].grid(alpha=0.3)

    # 4. Sunlight
    axes[3].plot(
        times_days, clouds, color='gold', linewidth=1.0
    )
    axes[3].set_ylabel('Sunlight (0..10000)')
    axes[3].set_title('Clouds')
    axes[3].set_xlabel('Hours')
    axes[3].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------
# Run the Tuning Script
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Simulate 2 full years to see seasonal behavior.
    simulate_and_plot(1440 * 30 * 6)
