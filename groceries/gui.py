import tkinter as tk
import tkinter.font as tkf
from functools import partial

from groceries.constants import EMPTY
from groceries.grocer_list import GroceryList
from groceries.io import items_to_csv
from groceries.item import GrocerArea, Item, KitchenArea, Priority, Supply

NAME_TEXT: str = "Name"
PRICE_TEXT: str = "Price"
PRIORITY_TEXT: str = "Priority"
SUPPLY_TEXT: str = "Supply"
KITCHEN_TEXT: str = "Kitchen Location"
GROCER_TEXT: str = "Grocery Location"

# GUI CONSTANTS
TITLE: str = "Grocery"
WIDTH_PX: int = 1450
HEIGHT_PX: int = 700
WIDTH_LIST: int = 400

ITEM_LIST_LABEL: str = "Items:"
LIST_ENTRY_WIDTH: int = 20
LIST_ENTRY_HEIGHT: int = 2
LIST_ENTRY_FONT: int = 20

MAIN_LABEL_FONT: int = 20
OPTION_LABEL_FONT: int = 15
MAIN_BUTTON_WIDTH: int = 20
MAIN_BUTTON_HEIGHT: int = 2
MAIN_BUTTON_FONT: int = 20
ADD_BUTTON_PROMPT: str = "Add Item"
EXPORT_BUTTON_PROMPT: str = "Export to CSV"

MENU_LABEL_FONT: int = 40
MENU_BUTTON_WIDTH: int = 20
MENU_BUTTON_HEIGHT: int = 2
MENU_BUTTON_FONT: int = 40
DONE_BUTTON_PROMPT: str = "Add Item"
DELETE_BUTTON_PROMPT: str = "Delete Item"
BACK_BUTTON_PROMPT: str = "Back"

FILTER_BUTTON_WIDTH: int = 20
FILTER_BUTTON_HEIGHT: int = 2
FILTER_BUTTON_FONT: int = 20
APPLY_BUTTON_PROMPT: str = "Apply Filters"
CLEAR_BUTTON_PROMPT: str = "Clear Filters"


class GUI(tk.Tk):
    def __init__(self, grocery: GroceryList) -> None:
        super().__init__()
        self.grocery = grocery
        self.list_items: list[tk.Button] = []
        self.filter_list: list[Item] = [item for item in self.grocery.item_list]
        self.search_term = tk.StringVar()

        # TK Entry Values
        self.itemname = tk.StringVar()
        self.itemprice = tk.StringVar()
        self.itemsupply = tk.StringVar()
        self.itempriority = tk.StringVar()
        self.itemkitchen = tk.StringVar()
        self.itemgrocer = tk.StringVar()

        # TK Checkbox Values
        self.filterprior = {mem: tk.IntVar() for mem in Priority}
        self.filtersupply = {mem: tk.IntVar() for mem in Supply}
        self.filterkitchen = {mem: tk.IntVar() for mem in KitchenArea}
        self.filtergrocer = {mem: tk.IntVar() for mem in GrocerArea}

        self.make_gui()

    def make_gui(self) -> None:
        """Constructor does Tkinter initialization then sets up GUI components.
        Starts with main window of given size. Main frame contains grocery list, add button, filters subframes.
        Menu frame consists of form and its buttons.
        """
        # Main Window
        self.title(TITLE)
        self.geometry(f"{WIDTH_PX}x{HEIGHT_PX}")

        # Main Page
        self.main_frame = tk.Frame(self)
        self.current_frame: tk.Frame = self.main_frame
        self.main_frame.pack()

        # Item Add/Update Menu
        self.menu_grid_frame = tk.Frame(self)
        self._make_menu(Item())

        # Add Button SubFrame for new entries.
        self.button_frame = tk.Frame(self.main_frame)
        self._make_buttons()

        # List SubFrame
        self.list_frame = tk.Frame(self.main_frame, height=HEIGHT_PX, width=WIDTH_LIST)
        self.item_label = tk.Label(
            self.list_frame, text="Items", font=tkf.Font(size=MAIN_LABEL_FONT)
        )
        self.canvas = tk.Canvas(self.list_frame)
        self.list_subframe = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(
            self.list_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.item_label.pack(side=tk.TOP)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.create_window(0.0, 0.0, window=self.list_subframe)
        self.list_subframe.bind("<Configure>", self.scroll_canvas)
        self._make_list()

        # Filter SubFrame
        self.filter_frame = tk.Frame(self.main_frame)
        self.filter_button_frame = tk.Frame(self.main_frame)
        self._clear_filters()
        self._make_filter_checkboxes()
        self._make_filter_buttons()

        self.button_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.list_frame.grid(row=0, column=2, rowspan=2, columnspan=5)
        self.filter_frame.grid(row=0, column=7, rowspan=1, columnspan=3)
        self.filter_button_frame.grid(row=1, column=7, rowspan=1, columnspan=3)

    def scroll_canvas(self, _) -> None:
        """Function called to move canvas when scrolling to change view."""
        self.canvas.configure(
            scrollregion=self.canvas.bbox(tk.ALL),
            width=WIDTH_LIST,
            height=HEIGHT_PX,
        )

    def _make_buttons(self) -> None:
        """Make add item and export buttons."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.search_label = tk.Label(
            self.button_frame,
            text="Search By Name",
            font=tkf.Font(size=MAIN_LABEL_FONT),
        )
        self.search_box = tk.Entry(self.button_frame, textvariable=self.search_term)
        self.search_button = tk.Button(
            self.button_frame,
            width=MAIN_BUTTON_WIDTH,
            height=MAIN_BUTTON_HEIGHT,
            font=tkf.Font(size=MAIN_BUTTON_FONT),
            text="Search",
            command=self._make_list,
        )
        self.add_button = tk.Button(
            self.button_frame,
            width=MAIN_BUTTON_WIDTH,
            height=MAIN_BUTTON_HEIGHT,
            font=tkf.Font(size=MAIN_BUTTON_FONT),
            text=ADD_BUTTON_PROMPT,
            command=self._add,
        )
        self.export_button = tk.Button(
            self.button_frame,
            width=MAIN_BUTTON_WIDTH,
            height=MAIN_BUTTON_HEIGHT,
            font=tkf.Font(size=MAIN_BUTTON_FONT),
            text=EXPORT_BUTTON_PROMPT,
            command=lambda: items_to_csv(self.grocery.item_list, self.grocery.outpath),
        )
        self.search_label.pack(side=tk.TOP)
        self.search_box.pack(side=tk.TOP)
        self.search_button.pack(side=tk.TOP)
        self.add_button.pack(side=tk.TOP)
        self.export_button.pack(side=tk.TOP)

    def _make_menu(self, item: Item) -> None:
        """Function to make item menu buttons for done and delete and make item menu form"""
        for widget in self.menu_grid_frame.winfo_children():
            widget.destroy()
        self.done_button = tk.Button(
            self.menu_grid_frame,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            font=tkf.Font(size=MENU_BUTTON_FONT),
            text=DONE_BUTTON_PROMPT,
            command=partial(self._update_done, item),
        )
        self.done_button.pack(side=tk.BOTTOM)
        self.delete_button = tk.Button(
            self.menu_grid_frame,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            font=tkf.Font(size=MENU_BUTTON_FONT),
            text=DELETE_BUTTON_PROMPT,
            command=partial(self._delete_done, item),
        )
        self.delete_button.pack(side=tk.BOTTOM)
        self.back_button = tk.Button(
            self.menu_grid_frame,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            font=tkf.Font(size=MENU_BUTTON_FONT),
            text=BACK_BUTTON_PROMPT,
            command=self.go_home,
        )
        self.back_button.pack(side=tk.BOTTOM)
        self._make_menu_form(item)

    def _make_menu_form(self, item: Item) -> None:
        """Construct Form and Done Button for Item Update or Addition.
        For item update, add item existing fields to default fill ins.
        """
        self.menu_form = tk.Frame(self.menu_grid_frame)
        self.itemname.set(f"{item.name}")
        self.itemprice.set(f"{item.price}")
        self.itempriority.set(f"{item.priority.value}")
        self.itemsupply.set(f"{item.supply.value}")
        self.itemkitchen.set(f"{item.kitchen_area.value}")
        self.itemgrocer.set(f"{item.grocer_area.value}")

        self.name_label = tk.Label(
            self.menu_form, text=NAME_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.name_entry = tk.Entry(
            self.menu_form,
            textvariable=self.itemname,
            font=tkf.Font(size=MENU_BUTTON_FONT),
        )
        self.price_label = tk.Label(
            self.menu_form, text=PRICE_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.price_entry = tk.Entry(
            self.menu_form,
            textvariable=self.itemprice,
            font=tkf.Font(size=MENU_BUTTON_FONT),
        )
        self.priority_label = tk.Label(
            self.menu_form, text=PRIORITY_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.priority_dropdown = tk.OptionMenu(
            self.menu_form, self.itempriority, *[opt.value for opt in Priority]
        )
        self.supply_label = tk.Label(
            self.menu_form, text=SUPPLY_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.supply_dropdown = tk.OptionMenu(
            self.menu_form, self.itemsupply, *[opt.value for opt in Supply]
        )
        self.kitchen_label = tk.Label(
            self.menu_form, text=KITCHEN_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.kitchen_dropdown = tk.OptionMenu(
            self.menu_form, self.itemkitchen, *[opt.value for opt in KitchenArea]
        )
        self.grocer_label = tk.Label(
            self.menu_form, text=GROCER_TEXT, font=tkf.Font(size=MENU_LABEL_FONT)
        )
        self.grocer_dropdown = tk.OptionMenu(
            self.menu_form, self.itemgrocer, *[opt.value for opt in GrocerArea]
        )

        self.name_label.grid(column=0, row=0)
        self.name_entry.grid(column=1, row=0)
        self.price_label.grid(column=0, row=1)
        self.price_entry.grid(column=1, row=1)
        self.priority_label.grid(column=0, row=2)
        self.priority_dropdown.grid(column=1, row=2)
        self.supply_label.grid(column=0, row=3)
        self.supply_dropdown.grid(column=1, row=3)
        self.kitchen_label.grid(column=0, row=4)
        self.kitchen_dropdown.grid(column=1, row=4)
        self.grocer_label.grid(column=0, row=5)
        self.grocer_dropdown.grid(column=1, row=5)
        self.menu_form.pack()

    def _make_list(self) -> None:
        """Function to make list of grocery items based on grocery item list.

        Grocery item list is list after applied filters and also reduced by search query.
        Forgets old buttons and makes new ones. Each button calls update to go to its item menu with itself as item arg.
        """
        for widget in self.list_subframe.winfo_children():
            widget.destroy()

        show_list = [
            item for item in self.filter_list if self.search_term.get() in item.name
        ]

        self.list_items = [
            tk.Button(
                self.list_subframe,
                width=LIST_ENTRY_WIDTH,
                height=LIST_ENTRY_HEIGHT,
                font=tkf.Font(size=LIST_ENTRY_FONT),
                text=item.name,
                command=partial(self._update, item),
            )
            for item in show_list
        ]

        for btn in self.list_items:
            btn.pack()

    def _make_filter_checkboxes(self) -> None:
        """Function to make filter form with checkboxes for each type of filter and value."""
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        self.priority_label = tk.Label(
            self.filter_frame, text=PRIORITY_TEXT, font=tkf.Font(size=MAIN_LABEL_FONT)
        )
        self.priority_boxes = [
            tk.Checkbutton(
                self.filter_frame,
                text=mem.value,
                variable=self.filterprior[mem],
                font=tkf.Font(size=OPTION_LABEL_FONT),
            )
            for mem in Priority
        ]
        self.supply_label = tk.Label(
            self.filter_frame, text=SUPPLY_TEXT, font=tkf.Font(size=MAIN_LABEL_FONT)
        )
        self.supply_boxes = [
            tk.Checkbutton(
                self.filter_frame,
                text=mem.value,
                variable=self.filtersupply[mem],
                font=tkf.Font(size=OPTION_LABEL_FONT),
            )
            for mem in Supply
        ]
        self.kitchen_label = tk.Label(
            self.filter_frame, text=KITCHEN_TEXT, font=tkf.Font(size=MAIN_LABEL_FONT)
        )
        self.kitchen_boxes = [
            tk.Checkbutton(
                self.filter_frame,
                text=mem.value,
                variable=self.filterkitchen[mem],
                font=tkf.Font(size=OPTION_LABEL_FONT),
            )
            for mem in KitchenArea
        ]
        self.grocer_label = tk.Label(
            self.filter_frame, text=GROCER_TEXT, font=tkf.Font(size=MAIN_LABEL_FONT)
        )
        self.grocer_boxes = [
            tk.Checkbutton(
                self.filter_frame,
                text=mem.value,
                variable=self.filtergrocer[mem],
                font=tkf.Font(size=OPTION_LABEL_FONT),
            )
            for mem in GrocerArea
        ]

        self.priority_label.pack(side=tk.TOP)
        for cbox in self.priority_boxes:
            cbox.pack(side=tk.TOP)
        self.supply_label.pack(side=tk.TOP)
        for cbox in self.supply_boxes:
            cbox.pack(side=tk.TOP)
        self.kitchen_label.pack(side=tk.TOP)
        for cbox in self.kitchen_boxes:
            cbox.pack(side=tk.TOP)
        self.grocer_label.pack(side=tk.TOP)
        for cbox in self.grocer_boxes:
            cbox.pack(side=tk.TOP)

    def _make_filter_buttons(self):
        """Functions to populate the buttons for applying/clearing filters."""
        for widget in self.filter_button_frame.winfo_children():
            widget.destroy()
        self.apply_button = tk.Button(
            self.filter_button_frame,
            width=FILTER_BUTTON_WIDTH,
            height=FILTER_BUTTON_HEIGHT,
            font=tkf.Font(size=FILTER_BUTTON_FONT),
            text=APPLY_BUTTON_PROMPT,
            command=self._apply_filters,
        )
        self.clear_button = tk.Button(
            self.filter_button_frame,
            width=FILTER_BUTTON_WIDTH,
            height=FILTER_BUTTON_HEIGHT,
            font=tkf.Font(size=FILTER_BUTTON_FONT),
            text=CLEAR_BUTTON_PROMPT,
            command=self._clear_filters,
        )

        self.apply_button.pack(side=tk.TOP)
        self.clear_button.pack(side=tk.TOP)

    def _add(self) -> None:
        """Callback for add item button, set old item to empty item, and go to item menu."""
        self.old_item = Item()
        self.go_menu(self.old_item)

    def _update(self, old_item: Item) -> None:
        """Callback for updating item clicking on grocery item, set old item to current item, and go to item menu."""
        self.old_item = old_item
        self.go_menu(old_item)

    def go_menu(self, incoming_item: Item) -> None:
        """Function to switch frames so item menu in scope and make menu based on current item."""
        self.main_frame.pack_forget()
        self._make_menu(incoming_item)
        self.menu_grid_frame.pack()

    def go_home(self):
        """Function to switch frames from item menu to main menu, remove default entry values, repopulate grocery list."""
        self.itemname.set(EMPTY)
        self.itemprice.set(EMPTY)
        self.itempriority.set(EMPTY)
        self.itemsupply.set(EMPTY)
        self.itemkitchen.set(EMPTY)
        self.itemgrocer.set(EMPTY)
        self.search_term.set(EMPTY)

        self.menu_grid_frame.pack_forget()
        self.main_frame.pack()
        self._make_buttons()
        self._apply_filters()
        self._make_filter_checkboxes()
        self._make_list()

    def _update_done(self, new_item: Item):
        """When done with update, set new item and add to grocery list, deleting old item if any..

        Set new item fields based on dropdown/entry fields in item menu, modify grocery list, call switch frames.
        """
        new_item.name = self.itemname.get()
        new_item.price = float(self.itemprice.get())
        new_item.priority = Priority[self.itempriority.get()]
        new_item.supply = Supply[self.itemsupply.get()]
        new_item.kitchen_area = KitchenArea[self.itemkitchen.get()]
        new_item.grocer_area = GrocerArea[self.itemgrocer.get()]

        self.grocery.delete(self.old_item)
        self.grocery.add(new_item)
        self.go_home()

    def _delete_done(self, del_item: Item):
        """When done with deletion of item in item menu, delete old item.

        Delete item, call switch frames to main menu.
        """
        self.grocery.delete(del_item)
        self.go_home()

    def _clear_filters(self):
        """For all the filter maps of tk values for checkboxes, set to 1 so nothing filtered, update check boxes."""
        for map in [
            self.filterprior,
            self.filtersupply,
            self.filterkitchen,
            self.filtergrocer,
        ]:
            for value in map.values():
                value.set(1)
        self._make_filter_checkboxes()
        self._apply_filters()

    def _apply_filters(self):
        """Based on values in checkbox maps in each type of filter, find appropriate filters, then apply them to filtere items.

        Keep applying filters until list fully reduced and reload grocery list.
        """
        self.filter_list = [item for item in self.grocery.item_list]
        prior_filters = [mem for mem, flag in self.filterprior.items() if flag.get()]
        self.filter_list = self.grocery.filter_priorities(
            self.grocery.item_list, prior_filters
        )
        supply_filters = [mem for mem, flag in self.filtersupply.items() if flag.get()]
        self.filter_list = self.grocery.filter_supplies(
            self.filter_list, supply_filters
        )
        kitchen_filters = [
            mem for mem, flag in self.filterkitchen.items() if flag.get()
        ]
        self.filter_list = self.grocery.filter_kitchen(
            self.filter_list, kitchen_filters
        )
        grocer_filters = [mem for mem, flag in self.filtergrocer.items() if flag.get()]
        self.filter_list = self.grocery.filter_grocer(self.filter_list, grocer_filters)
        self._make_list()
