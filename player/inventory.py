from db.repository import ItemRepository
# class Inventory:
#     def __init__(self, session, player_id: int):
#         self.session = session
#         self.player_id = player_id

#     def loose_items(self):
#         equipped_ids = (
#             select(EquipmentSlot.item_id)
#             .where(EquipmentSlot.item_id.isnot(None))
#         )

#         return (
#             self.session.query(Item)
#             .filter(Item.owner == self.player_id)
#             .filter(Item.container_item_id.is_(None))
#             .filter(~Item.id.in_(equipped_ids))
#             .all()
#         )
    
#     def equipped_items(self):
#         return (
#             self.session.query(EquipmentSlot)
#             .filter(EquipmentSlot.item_id.isnot(None))
#             .join(BodyNode)
#             .filter(BodyNode.owner == self.player_id)
#             .all()
#         )
    
#     def containers(self):
#         return (
#             self.session.query(Item)
#             .filter(Item.owner == self.player_id)
#             .filter(Item.contained_items.any())
#             .all()
#         )
    
#     def walk_container(self, item: Item, depth=0):
#         yield (depth, item)
#         for child in item.contained_items:
#             yield from self.walk_container(child, depth + 1)

#     def put_in_container(self, item: Item, container: Item):
#         item.container_item = container.id

#     def remove_from_container(self, item: Item):
#         item.container_item = None

#     def equip_item(self, item: Item, slot: EquipmentSlot):
#         if slot.item_id is not None:
#             raise ValueError("Slot already occupied")

#         item.container_item = None
#         slot.item_id = item.id

#     def unequip_item(self, slot: EquipmentSlot):
#         slot.item_id = None

class Inventory:
    def __init__(self, item_repo: ItemRepository, player_id: int):
        self.item_repo = item_repo
        self.player_id = player_id

    def loose_items(self):
        return self.item_repo.get_loose_items(self.player_id)

    def equipped_items(self):
        return self.item_repo.get_equipped_items(self.player_id)

    def containers(self):
        return self.item_repo.get_containers(self.player_id)