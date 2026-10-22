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
