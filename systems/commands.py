from dataclasses import dataclass
from typing import Callable, Sequence

@dataclass(frozen=True)
class CommandSpec:
    key: str
    target_type: str | None
    arg_types: Sequence[type]
    description: str
    handler: Callable



def advance_time(engine, minutes: int):
    for i in range(minutes):
        engine.step()



COMMANDS = [
    CommandSpec(
        key="tm",
        target_type=None,
        arg_types=[int],
        description="Advance time (minutes)",
        handler=advance_time
    ),
    CommandSpec(
        key="ph",
        target_type="Player",
        arg_types=[int],
        description="Increase hunger",
        handler=None
    ),
]



class CommandParser:
    def __init__(self):
        self.commands = {c.key: c for c in COMMANDS}

    

    def tokenize(self, text: str) -> list[str]:
        return [t for t in text.strip().split() if t]
    


    def parse_targets(self, target_type: str, token: str) -> list[int]:
        if target_type == "Player":
            if token == "*":
                return list(range(6))
            return [int(c) for c in token if c.isdigit()]
        
        elif target_type is None:
            return []

        raise ValueError(f"Unknown target type: {target_type}")
    


    def parse_arg(self, arg_type: type, token: str):
        try:
            return arg_type(token)
        except Exception:
            raise ValueError(f"Invalid value for {arg_type.__name__}: {token}")



    def parse(self, text: str):
        tokens = self.tokenize(text)
        if not tokens:
            return None

        key = tokens[0]
        if key not in self.commands:
            raise ValueError(f"Unknown command '{key}'")

        spec = self.commands[key]
        idx = 1

        targets = None
        if spec.target_type:
            if len(tokens) <= idx:
                raise ValueError("Missing targets")
            targets = self.parse_targets(spec.target_type, tokens[idx])
            idx += 1

        args = []
        for arg_type in spec.arg_types:
            if len(tokens) <= idx:
                raise ValueError("Missing arguments")
            args.append(self.parse_arg(arg_type, tokens[idx]))
            idx += 1

        return spec, targets, args