from .item import Item

class Cover(Item):
    def __init__(self):
        super().__init__()
        self.mat: str = None

