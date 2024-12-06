from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

import functools

from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button
from controllers.window.WindDelUsersController import WindDelUsersController


class WindDelUsers(QDialog):
    def __init__(self, parent, db):
        super().__init__()

        self._db_ = db

        self._controller_ = WindDelUsersController(this=self, parent=parent)

        self._static_ = Static()

        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(350)

        self.form = QFormLayout()

        title = QLabel("Select what you want to delete:")
        title.setFont(self._font_.setFont(10, 400))

        self.user_name = ComboBox()
        self.user_name.setFixedHeight(33)
        self.user_name.setObjectName("user_name")

        ctn_btn = QWidget()
        vbox_btn = QVBoxLayout()
        vbox_btn.setContentsMargins(0,0,0,0)
        btn = Button(name="Delete", style="error", icon_path="actions/trash")
        btn.clicked.connect(self.delete_users)
        btn.setFixedWidth(self.width())
        vbox_btn.addWidget(btn)
        ctn_btn.setLayout(vbox_btn)

        self.form.addRow(title)
        self.form.addRow(self.user_name)
        self.form.addRow(ctn_btn)

        self.setLayout(self.form)

        self.set_items()

    def set_items(self):
        self._controller_.set_items()
    
    def delete_users(self):
        self._controller_.delete_users()
