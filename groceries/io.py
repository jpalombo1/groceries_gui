from enum import Enum
from pathlib import Path
from typing import Any, Union

import pandas as pd

from groceries.item import GrocerArea, Item, KitchenArea, Priority, Supply

VAL_ENUM_MAP = {
    "priority": Priority,
    "supply": Supply,
    "grocer_area": GrocerArea,
    "kitchen_area": KitchenArea,
}


def items_from_csv(path: Path) -> list[Item]:
    """Import input csv of grocery items as grocery item list.
    Mapping column feature to Enum and value in csv at column to that Enum's value.

    Then construct item class using unpacked dictionary mapping.
    """
    pd_csv = pd.read_csv(path)
    grocer_list = []
    for _, row in pd_csv.iterrows():
        row_dict: dict[str, Any] = dict(row)
        dataclass_dir = {
            key: VAL_ENUM_MAP[key][value.upper()] if key in VAL_ENUM_MAP else value
            for key, value in row_dict.items()
        }
        grocer_list.append(Item(**dataclass_dir))
    return grocer_list


def items_to_csv(item_list: list[Item], path: Path) -> pd.DataFrame:
    """Import input csv of grocery items as grocery item list.
    If value is part of enums, get string value and lowercase. If string value, just lowercase, anything else just equal value like price."""
    df = pd.DataFrame(columns=list(Item.__annotations__.keys()))
    for item in item_list:
        item_dict = item.__dict__
        df_dict: dict[str, Union[str, float]] = {
            key: value.value.lower()
            if isinstance(value, Enum)
            else value.lower()
            if type(value) == str
            else value
            for key, value in item_dict.items()
        }
        df = df.append(df_dict, ignore_index=True)
    df.to_csv(path, index=False)
    return df
