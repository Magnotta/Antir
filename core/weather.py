from core.formulas.coefficients import WeatherCoefficients
from core.formulas.weather import derive_weather
from core.math_interface import weather_ctx_from_snapshot
from db.models.weather_snapshot import WeatherSnapshot
from db.repository.weather import WeatherRepository


class Weather:
    def __init__(
        self,
        repo: WeatherRepository,
        coeffs: WeatherCoefficients,
    ):
        self.repo = repo
        self.apply(
            derive_weather(
                weather_ctx_from_snapshot(
                    self.repo.load_snapshot()
                ),
                coeffs,
            )
        )

    def apply(self, weather_dict) -> None:
        self.temperature = weather_dict["temperature"]
        self.wind_speed = weather_dict["wind_speed"]
        self.wind_latent = weather_dict["wind_latent"]
        self.precipitation = weather_dict["precipitation"]
        self.precip_latent = weather_dict["precip_latent"]
        self.sunlight = weather_dict["sunlight"]
        self.cloud_coverage = weather_dict["cloud_coverage"]

    def to_snapshot(self) -> WeatherSnapshot:
        return WeatherSnapshot(
            tick=self.sim_time,
            temperature=self.temperature,
            wind_latent=self.wind_latent,
            precip_latent=self.precip_latent,
        )
