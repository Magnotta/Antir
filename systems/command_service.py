import shlex
from systems.commands import COMMANDS


class CommandParser:
    def __init__(self):
        self.commands = {c.key: c for c in COMMANDS}

    def tokenize(self, text: str) -> list[str]:
        return shlex.split(text)

    def parse_target(
        self, target_type: str, token: str
    ) -> int:
        if target_type == "Player":
            return int(token)
        elif target_type == "Item":
            return int(token)
        elif target_type is None:
            return
        raise ValueError(
            f"Unknown target type: {target_type}"
        )

    def parse_arg(self, arg_type: type, token: str):
        try:
            return arg_type(token)
        except Exception:
            raise ValueError(
                "Invalid value for"
                f"{arg_type.__name__}:{token}"
            )

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
            targets = self.parse_target(
                spec.target_type, tokens[idx]
            )
            idx += 1
        args = []
        for arg_type in spec.arg_types:
            if len(tokens) <= idx:
                raise ValueError("Missing arguments")
            args.append(
                self.parse_arg(arg_type, tokens[idx])
            )
            idx += 1
        kwargs = {}
        if idx < len(tokens):
            trailing = tokens[idx]
            kwargs["message"] = trailing
        return spec, targets, args, kwargs


class CommandService:
    def __init__(self, engine):
        self.engine = engine
        self.parser = CommandParser()

    def execute(self, text: str) -> list[str]:
        try:
            spec, target, args, kwargs = self.parser.parse(
                text
            )
            if target is not None:
                spec.handler(
                    self.engine, target, *args, **kwargs
                )
            else:
                spec.handler(self.engine, *args, **kwargs)
            return ["✔ Command executed"]
        except Exception as e:
            return [f"✖ {e}"]
