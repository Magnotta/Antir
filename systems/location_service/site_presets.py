from dataclasses import dataclass


@dataclass(frozen=True)
class SitePreset:
    """Ambient environmental values a Site can reference by name, via
    Site's preset-key field, instead of storing these numbers per-row.

    Frozen because presets are meant to be shared, read-only data -- many
    Site rows may point at the same preset key, so nothing should ever
    mutate an instance in place.
    """

    name: str
    rain_shelter: float
    sun_shelter: float
    ventilation: float
    base_temperature_offset: int


SITE_PRESETS_DICT = {}
