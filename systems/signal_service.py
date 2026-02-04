from collections import defaultdict
from typing import Callable
from enum import Enum, auto

SIGNALS = [
    "inventory",
    "equipment",
    "stats",
    "minute",
    "hour",
    "day",
    "location"
]



class SignalBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = defaultdict(list)
        self._stored_signals:set[str] = set()

    def connect(self, signal: str, callback: Callable):
        if signal not in SIGNALS:
            raise TypeError()
        self._listeners[signal].append(callback)

    def store(self, signals: str):
        for signal in signals.split():
            self._stored_signals.add(signal)

    def notify(self):
        batch_callbacks = set()
        for signal in self._stored_signals:
            for cb in self._listeners.get(signal, []):
                batch_callbacks.add(cb)
        self._stored_signals = set()
        for cb in batch_callbacks:
            if cb is not None:
                cb()
