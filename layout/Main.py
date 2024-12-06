from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
import os


from config.Static import Static
from config.Style import Style

from controllers.layout.MainController import MainController

from layout.MainBody import MainBody
from layout.SideMenu import SideMenu


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self._static_ = Static()

        self.style = Style()

        self._db_ = db

        self._controller_ = MainController(this=self)

        self.setWindowTitle(self._static_.get("app_name"))

        path_logo = os.path.join(os.getcwd(), "src\\images", "icon.png")
        self.setWindowIcon(QIcon(path_logo))

        self.init_ui()

    def init_ui(self):
        self.ctn = QWidget(self)

        self.layout_main = QHBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        self.side_menu = SideMenu(self._static_)
        self.side_menu.move(0, 0)
        # self.main_menu = MainMenu(self)

        self.main_app = MainBody(self._db_)
        self.main_app.move(self._static_.get("width_menu"), 0)

        self.list_nav_bar = self.side_menu.list_side_menu

        if self.list_nav_bar:
            self.list_nav_bar.clicked.connect(lambda: self.handle_side_menu(self.list_nav_bar.currentItem().text().strip().lower()))

        self.layout_main.addWidget(self.side_menu)
        self.layout_main.addWidget(self.main_app)

        self.layout_main.setStretch(0, 2)
        self.layout_main.setStretch(1, 11)

        self.ctn.setLayout(self.layout_main)

        self.setCentralWidget(self.ctn)

        self.setStyleSheet(self.style.get("bg_white"))
    
    def resizeEvent(self, event):
        self._controller_.resizeEvent(event)

        super().resizeEvent(event)
    
    def handle_side_menu(self, current):
        self._controller_.handle_side_menu(current)