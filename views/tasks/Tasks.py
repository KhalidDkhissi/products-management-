from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from controllers.views.TasksController import TasksController
from components.CustomTab import CustomTab
from components.Button import Button
from config.Style import Style
from config.Font import Font

class Tasks(QWidget):
    def __init__(self, db):
        super().__init__()

        self._db_ = db

        self._controller_ = TasksController(this=self)

        self._style_ = Style()

        self._font_ = Font()

        self.tabs_id = {}

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(20,20,20,0)
        
        title_page = QLabel("Tasks")
        title_page.setFont(self._font_.setFont(size=16, weight=700))
        title_page.setContentsMargins(0, 0, 0, 0)

        ctn_actions = self.actions()

        self.tabs_table = CustomTab()

        layout_main.addWidget(title_page)
        layout_main.addWidget(ctn_actions)
        layout_main.addWidget(self.tabs_table)
        
        self.setLayout(layout_main)

        self.set_tabs()

    def actions(self):
        ctn_actions = QWidget()

        layout_actions = QHBoxLayout()
        layout_actions.setContentsMargins(0, 0, 0, 10)
        layout_actions.setSpacing(5)
        
        box = QWidget()
        
        btn_add_new = Button(name='New User', style='primary', icon_path="actions/add")
        btn_add_new.clicked.connect(self.create_user)
        
        btn_delete_all = Button(name='Delete', style='error', icon_path="actions/trash")
        btn_delete_all.clicked.connect(self.delete_users)

        layout_actions.addWidget(box)
        layout_actions.addWidget(btn_delete_all)
        layout_actions.addWidget(btn_add_new)
        layout_actions.setStretch(0, 2)

        ctn_actions.setLayout(layout_actions)

        return ctn_actions
    
    def create_user(self):
        self._controller_.create_user()
    
    def delete_users(self):
        self._controller_.delete_users()

    def set_tabs(self):
        self._controller_.set_tabs()