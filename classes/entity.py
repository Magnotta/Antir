class Entity:
    ids = []

    def __init__(self, id:int=None):
        if id is None:
            self.id = Entity.new_id()
        else:
            self.id = id
        if self.id in Entity.ids:
            raise ValueError(f'Non unique Entity ID: {self.id}')
        Entity.ids.append(self.id)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __repr__(self) -> str:
        return f'{self.id:x}'

    def __del__(self):
        try:
            Entity.ids.remove(self.id)
        except ValueError:
            raise ValueError(f'Remove ID not in list: {self.id}')

    @classmethod
    def new_id(cls) -> int:
        if not Entity.ids:
            return 0
        elif len(Entity.ids) == 1:
            if 0 in Entity.ids:
                return 1
            else:
                return 0

        previous_id = Entity.ids[0]
        for id in Entity.ids[1:]:
            if not id == previous_id + 1:
                return previous_id + 1
            previous_id += 1

        return Entity.ids[-1] + 1

class ItemEntity(Entity):
    pass

class CharacterEntity(Entity):
    pass