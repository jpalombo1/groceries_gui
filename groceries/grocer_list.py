from dataclasses import dataclass
from pathlib import Path

from groceries.item import GrocerArea, Item, KitchenArea, Priority, Supply


@dataclass
class GroceryList:
    item_list: list[Item]
    outpath: Path

    def add(self, item: Item) -> None:
        """Add item to grocery list."""
        self.item_list.append(item)

    def delete(self, item: Item) -> None:
        """Remove item from grocery list."""
        self.item_list = [new_item for new_item in self.item_list if new_item != item]

    def update(self, item: Item) -> None:
        """Update item on grocery list by deleting item of same name, then adding it."""
        self.delete(item)
        self.add(item)

    def filter_priorities(
        self, item_list: list[Item], filters: list[Priority]
    ) -> list[Item]:
        """Filter grocery list by only includign items with given priority(s)"""
        return [item for item in item_list if item.priority in filters]

    def filter_supplies(
        self, item_list: list[Item], filters: list[Supply]
    ) -> list[Item]:
        """Filter grocery list by only including items with given supplies(s)"""
        return [item for item in item_list if item.supply in filters]

    def filter_kitchen(
        self, item_list: list[Item], filters: list[KitchenArea]
    ) -> list[Item]:
        """Filter grocery list by only includign items with given kitchen area(s)"""
        return [item for item in item_list if item.kitchen_area in filters]

    def filter_grocer(
        self, item_list: list[Item], filters: list[GrocerArea]
    ) -> list[Item]:
        """Filter grocery list by only includign items with given grocer area(s)"""
        return [item for item in item_list if item.grocer_area in filters]
