from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit

from controllers.window.WindCategoriesController import WindCategoriesController
from config.Font import Font
from config.Static import Static
from components.Button import Button

class WindCategories(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindCategoriesController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(500)

        if self._action_ == "new":
            title = QLabel("Add new category")
            self.btn = Button(name="Add New", style="success")
            self.btn.clicked.connect(self.create_category)
        else:
            title = QLabel("Edit category")
            self.btn = Button(name="Edit", style="primary")
            self.btn.clicked.connect(self.update_category)

        title.setFont(self._font_.setFont(13, 500))
        title.setStyleSheet("text-align: center; width: 100%")

        self.form = QFormLayout()

        label_category_name = QLabel("Category name:")
        label_category_name.setFont(self._font_.setFont(10, 500))
        
        self.category_name = QLineEdit()
        self.category_name.setFixedHeight(33)
        self.category_name.setObjectName("category_name")
        
        label_description_name = QLabel("Description:")
        label_description_name.setFont(self._font_.setFont(10, 500))
        
        self.description_name = QLineEdit()
        self.description_name.setFixedHeight(33)
        self.description_name.setObjectName("description")

        self.btn.setFixedWidth(self.width()) 

        self.form.addRow(title)
        self.form.addRow(label_category_name)
        self.form.addRow(self.category_name)
        self.form.addRow(label_description_name)
        self.form.addRow(self.description_name)
        self.form.addRow(self.btn)

        self.form.setContentsMargins(10,0,10,0)

        self.setLayout(self.form)

        if self._data_ is not None:
            self.set_data()
        
    def create_category(self):
        self._controller_.create_category()

    def set_data(self):
        self._controller_.set_data(self._data_)

    def update_category(self, data):
        self._controller_.update_category(self._data_)
