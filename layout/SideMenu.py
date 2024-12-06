from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import os

from config.Style import Style
from config.Font import Font
from components.Button import Button

from controllers.layout.SideMenuController import SideMenuController

class SideMenu(QWidget):
    def __init__(self, static):
        super().__init__()
        self._static_ = static

        self._controller_ = SideMenuController(this=self)
        
        self._font_ = Font()

        self.style = Style()

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        self.list_side_menu = QListWidget()
        self.list_side_menu.setStyleSheet(self.style.get("side_menu"))
        # self.list_side_menu.currentItem()
        self.nav_items()

        # Connect the item clicked signal to the toggle function
        self.list_side_menu.itemClicked.connect(self._controller_.toggle_sub_items)

        self.list_side_menu.setFont(self._font_.setFont(10, 600))

        layout_main.addWidget(self.list_side_menu)

        self.setLayout(layout_main)

    def nav_items(self):
        self._controller_.nav_items()
        print("nav items...")