from uuid import uuid1, UUID

class Entity:
    def __init__(self, id=None):
        if(id is None):
            self.id = UUID(uuid1().hex)
        else:
            self.id = UUID(id)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self.id == __o.id

        return False
