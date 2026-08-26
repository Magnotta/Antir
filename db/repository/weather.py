from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models.weather_snapshot import WeatherSnapshot


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_snapshot(self, snap: WeatherSnapshot):
        self.session.add(snap)

    def load_snapshot(self) -> WeatherSnapshot:
        stmt = (
            select(WeatherSnapshot)
            .order_by(WeatherSnapshot.tick.desc())
            .limit(1)
        )
        latest = self.session.execute(
            stmt
        ).scalar_one_or_none()

        if latest is not None:
            return latest

        # No snapshot exists – create a new one with all zeros
        return WeatherSnapshot(
            tick=0,
            temperature=0,
            wind_latent=0,
            precip_latent=0,
        )
