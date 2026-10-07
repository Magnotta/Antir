from enum import Enum
from dataclasses import dataclass, field
from core.time import Time
from core.defs import SkillTrack


class Interruptibility(str, Enum):
    FREE = "free"  # stop anytime, no penalty, resumes trivially
    RESUMABLE = "resumable"  # can pause, but resuming costs time/quality
    CRITICAL = "critical"  # interruption ruins progress entirely (smelting)


@dataclass(frozen=True)
class RiskEntry:
    risk_type: str
    base_probability_per_tick: (
        float  # rolled against by TaskProgressCheck
    )
    severity_range: tuple[
        float, float
    ]  # min/max severity if it triggers


@dataclass(frozen=True)
class RepetitionSpec:
    rep_count: int = 0
    rep_target: int = 1
    per_rep_strain_scalar: float = (
        1.0  # lets reps drive duration instead of a flat number
    )


@dataclass(frozen=True)
class TaskOutput:
    mold_id: int
    quantity_range: tuple[int, int]
    quality_dependent: bool = (
        True  # does TaskInstance.quality gate yield grade?
    )


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
    type: str
    explanation: str
    threshold: float
    weight: float


@dataclass(frozen=True)
class TaskPreset:
    name: str
    skill_track: SkillTrack
    task_components: dict[str, float]
    exp_effect: tuple[float, float, float, float]
    metabolic_mult: float
    notes: str
    technicalities: dict[str, Technicality] = field(
        default_factory=dict
    )
    interruptibility: Interruptibility = (
        Interruptibility.FREE
    )
    min_lighting: int = 0


@dataclass(frozen=True)
class TaskSpec:
    task_preset: str
    total_workload: int
    repetition: RepetitionSpec = field(
        default_factory=lambda: RepetitionSpec()
    )
    output: TaskOutput | None = None
    workstation_id: int | None = None
    duration_override_ticks: int | None = None
    technicalities: dict[str, Technicality] = field(
        default_factory=dict
    )
    notes: str = ""


@dataclass(frozen=True)
class TaskInstance:
    task_preset: str
    task_group_id: int
    started_at: Time
    duration: Time  # same value across all participants in a group
    strain_per_tick: int  # personal — computed from only *this* participant's components
    quality_coefficient: float
    safety_coefficient: float
    remaining_reps: int | None
    interrupted: bool = False
    risk_profile: list[RiskEntry] = field(
        default_factory=list
    )
