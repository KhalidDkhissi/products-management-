from PyQt5.QtWidgets import QWidget, QVBoxLayout

from controllers.views.TransactionsController import TransactionsController
from components.Grid import Grid
from config.Style import Style
from config.Font import Font

class Transactions(QWidget):
    def __init__(self, db):
        super().__init__()

        self._db_ = db

        self._controller_ = TransactionsController(this=self)

        self._style_ = Style()
        
        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0,0,0,0)

        self.setLayout(layout_main)

        self._grid_ = Grid(parent=self, table_name="transactions")

        layout_main.addWidget(self._grid_)
    