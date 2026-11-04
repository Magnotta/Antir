from dataclasses import dataclass
from enum import Enum


class ItemParamName(str, Enum):
    DURABILITY = "durability"
    QUALITY = "quality"
    WET = "wet"
    FILL = "fill"
    LEGIBILITY = "legibility"
    PURITY = "purity"
    QUANTITY = "count"
    VOLUME = "volume"
    ROT = "rot"
    CONDITION = "condition"
    AROMA = "aroma"
    FLAVOR = "flavor"
    CHARM = "charm"
    SMELL = "smell"
    BALANCE = "balance"
    INTEGRATION = "integration"
    MASS = "mass"
    SHARPNESS = "sharpness"
    ROUGHNESS = "roughness"
    WIELDINESS = "wieldiness"
    POINTINESS = "pointiness"
    HARDNESS = "hardness"
    CLEANLINESS = "cleanliness"
    POWER = "power"
    SATURATION = "saturation"
    NUTRITION = "nutrition"
    RETENTION = "retention"
    FORMALITY = "formality"
    INSULATION = "insulation"
    ANCHOR = "anchor"
    DELAY = "delay"
    HEALTH = "health"


class ToolName(str, Enum):
    AXE = "axe"
    HAMMER = "hammer"
    PICKAXE = "pickaxe"
    HOE = "hoe"
    MACHETE = "machete"
    SCYTHE = "scythe"
    GLOVES = "gloves"
    PLAIN = "plain"
    APRON = "apron"
    SAW = "saw"
    TONGS = "tongs"
    DRILL = "drill"
    SHOVEL = "shovel"
    DIGGER = "digger"
    PITCHFORK = "pitchfork"
    SICKLE = "sickle"
    KNIFE = "knife"
    SHEARS = "shears"
    FISHING_ROD = "fishing_rod"
    PADDLE = "paddle"
    SPINDLE = "spindle"
    NEEDLE = "needle"
    THIMBLE = "thimble"
    TROWEL = "trowel"
    JIG = "jig"
    GOUGE = "gouge"
    AWL = "awl"
    BLOWPIPE = "blowpipe"
    BRUSH = "brush"
    BROOM = "broom"
    RAG = "rag"
    MORTAR_AND_PESTLE = "mortar_and_pestle"
    SPLINT = "splint"
    ROPE = "rope"
    POLE = "pole"
    HARNESS = "harness"
    LEASH = "leash"
    DART = "dart"
    ROCK = "rock"
    SPEAR = "spear"
    SLING = "sling"
    BOARD = "board"
    BOOTS = "boots"
    BOW = "bow"
    CHISEL = "chisel"
    WEDGE = "wedge"
    NAILS = "nails"
    CLEAVER = "cleaver"
    GOGGLES = "goggles"
    BASKET = "basket"
    BUCKET = "bucket"
    BARREL = "barrel"


class ToolModality(str, Enum):
    CHOPPING = "chopping"


@dataclass(frozen=True)
class CoefficientRule:
    at_min: float  # multiplier when the driver is at its window minimum
    at_max: float  # multiplier when the driver is at its window maximum
    driver: ItemParamName  # item param name

    # <1: the effect holds up until the param is quite low, then falls
    # fast. >1: only near-maximum values give the full effect.
    exponent: float = 1.0

    # Raw-unit window for the driver. Defaults to 0..ITEM_PARAM_MAXES.
    low: int | None = None
    high: int | None = None

    def __post_init__(self):
        if self.driver not in ItemParamName:
            raise ValueError(
                f"unknown item param {self.driver!r}"
            )
        if self.at_min >= self.at_max:
            raise ValueError(
                f"Tool coefficient rule of {self.driver}: at_min must be < at_max"
            )
        if self.exponent <= 0:
            raise ValueError("exponent must be > 0")

    def value(
        self,
        params: dict[ItemParamName, int],
        exp_coeff: float,
    ) -> float:
        return self.at_min + exp_coeff * (
            self.at_max - self.at_min
        ) * (
            (params[self.driver] / 1000.0) ** self.exponent
        )

    def to_json(self) -> dict:
        return {
            "at_min": self.at_min,
            "at_max": self.at_max,
            "driver": self.driver,
            "exponent": self.exponent,
            "low": self.low,
            "high": self.high,
        }

    @classmethod
    def from_json(cls, data: dict) -> "CoefficientRule":
        return cls(
            at_min=data["at_min"],
            at_max=data["at_max"],
            driver=data["driver"],
            exponent=data["exponent"],
            low=data["low"],
            high=data["high"],
        )
