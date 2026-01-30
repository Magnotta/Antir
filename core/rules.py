class Rule:
    listens_to: set[str] = set()
    name = 'rulebase'

    def applies(self, event, state) -> bool:
        """Should this rule run?"""
        return False

    def execute(self, event, state) -> list:
        """Return new events"""
        return []
