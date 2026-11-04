<<<<<<< HEAD
from enum import Enum
from dataclasses import dataclass
from core.defs.task import SkillTrack


class Interruptibility(str, Enum):
    FREE = "free"  # stop anytime, no penalty, resumes trivially
    RESUMABLE = "resumable"  # can pause, but resuming costs time/quality
    CRITICAL = "critical"  # interruption ruins progress entirely (smelting)


@dataclass(frozen=True)
class ParticipantAssignment:
    participant_id: int
    components: list[
        str
    ]  # which physical activities this participant performs
    equipped_tool_item_ids: dict[
        str, list[int]
    ]  # activity -> item_ids, per component they perform


@dataclass(frozen=True)
class Technicality:
    key: str
    explanation: str
    trigger_handle: str


@dataclass(frozen=True)
class TaskPreset:
    name: str
    skill_track: SkillTrack
    task_components: dict[str, float]
    exp_effect: tuple[float, float, float, float]
    metabolic_mult: float
    min_lighting: int
    technicalities: dict[str, Technicality]
    interruptibility: Interruptibility
=======
from .classes import SkillTrack, AspectVector


SKILLTRACK_EXP_COEFFS_DICT: dict[
    SkillTrack, AspectVector
] = {
    SkillTrack.WOODCUTTING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.MINING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.QUARRYING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FORAGING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.HERBALISM: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FISHING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.HUNTING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.TRAPPING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FARMING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.ANIMAL_HUSBANDRY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.MILKING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.SHEARING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BEEKEEPING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BUTCHERY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.COOKING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BAKING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BREWING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.PRESERVING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.SPINNING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.WEAVING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.TAILORING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.DYEING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.TANNING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.LEATHERWORKING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.CARPENTRY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.COOPERING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.MASONRY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.THATCHING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.WOODCARVING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.SMITHING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.SMELTING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BOWYER: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FLETCHING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.POTTERY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.BASKETRY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.GEM_CUTTING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.GLASS_BLOWING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.DOMESTIC_LABOR: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FIREMAKING: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.ATHLETICS: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.ACROBATICS: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.HERBLORE: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.FIRST_AID: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.MELEE_COMBAT: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.ARCHERY: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
    SkillTrack.UNARMED_COMBAT: AspectVector.from_tuple(
        (1, 3000, 3000, 3000)
    ),
}
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
