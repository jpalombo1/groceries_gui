from dataclasses import dataclass
from groceries.constants import EMPTY
from enum import Enum


class Priority(Enum):
    """How often to get groceries."""

    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    LESS_OFTEN = "LESS_OFTEN"
    NOT_NEEDED = "NOT_NEEDED"


class Supply(Enum):
    """How much of grocery possesed."""

    NEEDED = "NEEDED"
    RUNNING_LOW = "RUNNING_LOW"
    SUPPLIED = "SUPPLIED"
    EXTRA = "EXTRA"


class KitchenArea(Enum):
    """Where in kitchen grocery is put away."""

    FREEZER = "FREEZER"
    FRIDGE = "FRIDGE"
    PANTRY = "PANTRY"
    SNACK = "SNACK"
    BAKING = "BAKING"
    SPICE = "SPICE"


class GrocerArea(Enum):
    """Where in grocery store item is found."""

    AISLE = "AISLE"
    DAIRY = "DAIRY"
    DELI = "DELI"
    MEAT = "MEAT"
    FROZEN = "FROZEN"
    PRODUCE = "PRODUCE"


@dataclass
class Item:
    """Class object for single grocery item."""

    name: str = EMPTY
    price: float = 0.0
    priority: Priority = Priority.NOT_NEEDED
    supply: Supply = Supply.NEEDED
    grocer_area: GrocerArea = GrocerArea.AISLE
    kitchen_area: KitchenArea = KitchenArea.PANTRY

    def __eq__(self, item: object) -> bool:
        """Item is the same as another if contaisn the same name only."""
        if not isinstance(item, Item):
            return NotImplemented
        return self.name == item.name
