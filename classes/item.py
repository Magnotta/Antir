from .entity import Entity

class Item(Entity):
    def __init__(self, name, qty=1, isContainer=False):
        super().__init__()
        self.drblt: int = 100
        self.kgs: float = 0.0
        self.name: str = name
        self.qty: int = qty
        self.isContainer = isContainer
        self.storedItems = []
        
    def storeItem(self, item):
        if(not self.isContainer):
            print('Non container items cannot store other items!')
            return
        
        if(item.isContainer):
            print('Cannot store container item inside another container!')
            return
        
        self.storedItems.append(item)
