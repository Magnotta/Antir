from collections import defaultdict
from typing import Callable
from enum import Enum, auto


class Signal(Enum):
    inventory = auto()
    equipment = auto()
    stats = auto()
    minute = auto()
    hour = auto()
    day = auto()
    location = auto()


class SignalBus:
    def __init__(self):
        self._listeners: dict[Signal, list[Callable]] = (
            defaultdict(list)
        )
        self._stored_signals: set[Signal] = set()
        self.decision_paths: dict = {}

    def connect(self, signal: Signal, callback: Callable):
        self._listeners[signal].append(callback)

    def store(self, signals: list[Signal]):
        for signal in signals:
            self._stored_signals.add(signal)

    def notify(self):
        batch_callbacks = set()
        for signal in self._stored_signals:
            for cb in self._listeners.get(signal, []):
                batch_callbacks.add(cb)
        for cb in batch_callbacks:
            if cb is not None:
                cb()
        self._stored_signals = set()

    def create_decision_path(
        self, decision_type, callback: Callable
    ):
        self.decision_paths[decision_type] = callback

    def choice_required(self, pending):
        return self.decision_paths[pending.type](
            pending.payload
        )
