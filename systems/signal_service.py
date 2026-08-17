from dataclasses import dataclass, field
from typing import Any
from collections import defaultdict
from typing import Callable
from enum import Enum, auto
from .pending_decision import DecisonType, PendingDecision


class SignalType(Enum):
    inventory = auto()
    equipment = auto()
    stats = auto()
    anatomical = auto()
    minute = auto()
    hour = auto()
    day = auto()
    location = auto()
    summary = auto()
    sleep = auto()
    wake_up = auto()
    check = auto()


@dataclass
class Signal:
    type: SignalType
    payload: dict[str, Any] = field(default_factory=dict)


class SignalBus:
    def __init__(self):
        self._listeners: dict[Signal, list[Callable]] = (
            defaultdict(list)
        )
        self._stored_signals: list[Signal] = []
        self.decision_paths: dict[DecisonType, Callable] = (
            {}
        )

    def connect(
        self, signal_type: SignalType, callback: Callable
    ):
        self._listeners[signal_type].append(callback)

    def store(self, signals: list[Signal]):
        for signal in signals:
            self._stored_signals.append(signal)

    def notify(self):
        batch_callbacks = set()
        for signal in self._stored_signals:
            for cb in self._listeners.get(signal.type, []):
                batch_callbacks.add(cb)
        for cb in batch_callbacks:
            if cb is not None:
                cb()
        self._stored_signals = []

    def create_decision_path(
        self, decision_type: DecisonType, callback: Callable
    ):
        self.decision_paths[decision_type] = callback

    def choice_required(self, pending: PendingDecision):
        return self.decision_paths[pending.type](
            pending.payload
        )
