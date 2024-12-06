from PyQt5.QtGui import QIcon
import os

class MainController:
    def __init__(self, this):
        self.this = this

    def resizeEvent(self, event):
        width = self.this.width()
        height = self.this.height()
        width_menu = self.this._static_.get("width_menu")

        self.this.ctn.setGeometry(0, 0, width, height)

        self.resizeWidget()

        layout = self.this.layout()
        layout.update()

        self.this.update()

    def resizeWidget(self):
        width_menu = self.this._static_.get("width_menu")
        width = self.this.width()
        height = self.this.height()

        self.this.side_menu.setGeometry(0, 0, width_menu, height)
        self.this.main_app.setGeometry(width_menu, 0, width - width_menu, height)

    def handle_side_menu(self, current_item_name):
        views = self.this.main_app.views

        if current_item_name in views:
            self.this.main_app._controller_.redirect_to(current_item_name)
    