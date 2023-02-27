from .item import Item

class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.mat: str = None
        self.mode: str = 'blunt'

