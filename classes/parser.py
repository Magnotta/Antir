

class Parser:
    def __init__(self) -> None:
        self.description = ''
        self.ans = ''
        self.command = ''

    def parse(self, chars: str):
        self.command = chars.lower()
        depth = len(self.command)

        if not self.command:
            self.description = ''
        elif self.command[0] == 't':
            self.description = "Menu de tempo"
        elif self.command[0] == 'p':
            self.description = "Menu de personagem"
        elif self.command[0] == 'k':
            self.description = "Menu de combate"
        elif self.command[0] == 'e':
            self.description = "Menu de ambiente"
        elif self.command[0] == 'l':
            self.description = "Menu de local"
        else:
            self.description = ''

        if depth == 1:
            return
