from PyQt5.QtWidgets import QListWidgetItem, QMenu, QMenuBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from config.Static import Static
from config.Font import Font

import os

class SideMenuController:
    def __init__(self, this):
        self.this = this

        self._static_ = Static()
        self._font_ = Font()

        self.path = os.path.join(os.getcwd(), "src/images/side menu")

        # Track the expansion state of each main menu item
        self.expanded_items = {}

    def nav_items(self):
        items = self._static_.get("items_side_menu")

        for item_name in items:
            # Add the main menu item
            icon = QIcon(os.path.join(self.path, f"{item_name.lower()}.png"))
            main_item = QListWidgetItem(item_name.capitalize())
            main_item.setIcon(icon)
            main_item.setTextAlignment(Qt.AlignLeft)
            main_item.setData(Qt.UserRole, True)
            self.this.list_side_menu.addItem(main_item)

            # Initialize the expansion state as collapsed
            self.expanded_items[item_name] = False

    def toggle_sub_items(self, item):
        item_name = item.text().strip()

        # Ensure the item_name is capitalized to match the dictionary key
        item_name = item_name.capitalize()

        # Check if the item is a main menu item
        if item.data(Qt.UserRole):
            if self.expanded_items.get(item_name, False):
                # If expanded, collapse the sub-items
                self.collapse_sub_items(item)
                self.expanded_items[item_name] = False
            else:
                # If collapsed, expand the sub-items
                self.expand_sub_items(item)
                self.expanded_items[item_name] = True

    def expand_sub_items(self, main_item):
        items = self._static_.get("items_side_menu")

        for item_name in items:
            if item_name == main_item.text().strip().lower():
                sub_items = items[item_name]
                row = self.this.list_side_menu.row(main_item)

                # Insert sub-items under the main item
                for sub_item_name in sub_items:
                    icon = QIcon(os.path.join(self.path, f"{sub_item_name.lower()}.png"))
                    sub_item = QListWidgetItem("   " + sub_item_name.capitalize())
                    sub_item.setIcon(icon)
                    sub_item.setTextAlignment(Qt.AlignLeft)
                    sub_item.setData(Qt.UserRole, False)
                    self.this.list_side_menu.insertItem(row + 1, sub_item)
                    row += 1
                break

    def collapse_sub_items(self, main_item):
        row = self.this.list_side_menu.row(main_item) + 1

        # Remove sub-items until we hit another main item or the end of the list
        while row < self.this.list_side_menu.count():
            next_item = self.this.list_side_menu.item(row)
            if next_item.data(Qt.UserRole):  # If the next item is a main item, stop
                break
            self.this.list_side_menu.takeItem(row)