from typing import Protocol, Any
from core.game_state import GameState
from systems.signal_service import SignalBus
from systems.summary_service import Summarizer


class EngineProtocol(Protocol):
    state: GameState
    signals: SignalBus
    summarizer: Summarizer

    def schedule(self, event: Any, org: str) -> None: ...
    def step(self) -> None: ...
