from classes.item import Item

class Inventory:
    def __init__(self, owner: int) -> None:
        self.owner_id = owner
        self.items: list[Item] = []

    def add(self, i: Item):
        self.items.append(i)

    def drop(self, item_id: int):
        removed = False
        for i in self.items:
            if i.id == item_id:
                self.items.remove(i)
                removed = True
                break

        if not removed:
            raise ValueError(f'Remove item not in p{self.owner_id}inventory: ID={item_id}')

    