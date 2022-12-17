from pathlib import Path

from groceries.io import items_from_csv
from groceries.grocer_list import GroceryList
from groceries.gui import GUI

DATABASE = Path(__file__).parent / "data" / "grocery_list.csv"
OUTPATH = DATABASE.parent / "test_list.csv"


def main():
    """Main function."""
    grocer_items = items_from_csv(DATABASE)
    grocer_list = GroceryList(item_list=grocer_items, outpath=OUTPATH)
    gui = GUI(grocer_list)
    gui.mainloop()


if __name__ == "__main__":
    main()
