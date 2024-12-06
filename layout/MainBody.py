from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from views.dashboard.Dashboard import Dashboard
from views.inventory.Products import Products
from views.inventory.Categories import Categories
from views.inventory.Suppliers import Suppliers
from views.inventory.Orders import Orders
from views.inventory.Transactions import Transactions
from views.tasks.Tasks import Tasks
from views.recruitment.JobPostings import JobPostings
from views.recruitment.Candidates import Candidates
from views.recruitment.Interviews import Interviews
from views.settings.Settings import Settings
from views.help.Help import Help

from config.Style import Style
from config.Static import Static

from controllers.layout.MainBodyController import MainBodyController

class MainBody(QWidget):
    def __init__(self, db):
        super().__init__()
        self._static_ = Static()

        self._db_ = db

        self._controller_ = MainBodyController(this=self)

        self.style = Style()

        self.views = {
            "dashboard": Dashboard(db),
            "products": Products(db),
            "categories": Categories(db),
            "suppliers": Suppliers(db),
            "orders": Orders(db),
            "transactions": Transactions(db),
            "tasks": Tasks(db),
            "job postings": JobPostings(db),
            "candidates": Candidates(db),
            "interviews": Interviews(db),
            "settings": Settings(db),
            "help": Help(),
        }
        
        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        self.stack_widget = QStackedWidget()

        for view in self.views:
            self.stack_widget.addWidget(self.views[view])

        self.redirect_to()
        
        layout_main.addWidget(self.stack_widget)

        self.setLayout(layout_main)

    def redirect_to(self):
        self._controller_.redirect_to(self._static_.get("current_view"))