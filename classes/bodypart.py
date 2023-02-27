from .entity import Entity

class BodyPart:
    def __init__(self):
        self.health = 100
        self.cover: Cover = None
        self.status: str = 'normal'
