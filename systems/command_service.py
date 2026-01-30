from systems.commands import CommandParser
    


class CommandService:
    def __init__(self, engine):
        self.engine = engine
        self.parser = CommandParser()

    def execute(self, text: str) -> list[str]:
        try:
            spec, targets, args = self.parser.parse(text)

            if targets is not None:
                spec.handler(self.engine, targets, *args)
            else:
                spec.handler(self.engine, *args)

            return ["✔ Command executed"]

        except Exception as e:
            return [f"✖ {e}"]
