from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

import functools

from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button
from controllers.window.WindUsersController import WindUsersController

class WindUsers(QDialog):
    def __init__(self, db, action):
        super().__init__()

        self._db_ = db

        self._action_ = action

        self._controller_ = WindUsersController(this=self)

        self._static_ = Static()

        self._font_ = Font()

        self.state = False

        self.user = None

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(500)

        if self._action_ == "new":
            title = QLabel("Add new user")
            self.btn = Button(name="Add New", style="success")
            self.btn.clicked.connect(self.create_user)
        else:
            title = QLabel("Edit user")
            self.btn = Button(name="Edit", style="primary")
            # self.btn.clicked.connect(self.update_category)

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_full_name = QLabel("Full name:")
        label_full_name.setFont(self._font_.setFont(10, 500))
        
        self.full_name = QLineEdit()
        self.full_name.setFixedHeight(33)
        self.full_name.setObjectName("full_name")

        vbox_1.addWidget(label_full_name)
        vbox_1.addWidget(self.full_name)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_email = QLabel("Email:")
        label_email.setFont(self._font_.setFont(10, 500))

        self.email = QLineEdit()
        self.email.setFixedHeight(33)
        self.email.setObjectName("email")

        vbox_2.addWidget(label_email)
        vbox_2.addWidget(self.email)

        box_2.setLayout(vbox_2)

        hbox_1.addWidget(box_1)
        hbox_1.addWidget(box_2)

        ctn_1.setLayout(hbox_1)

        ctn_2 = QWidget()
        hbox_2 = QHBoxLayout()
        hbox_2.setContentsMargins(0,0,0,0)

        box_3 = QWidget()
        vbox_3 = QVBoxLayout()
        vbox_3.setContentsMargins(0,0,0,0)

        label_role = QLabel("Role:")
        label_role.setFont(self._font_.setFont(10, 500))
        
        self.role = ComboBox(self._static_.get("role_users"))
        self.role.setFixedHeight(33)
        self.role.setObjectName("role")

        vbox_3.addWidget(label_role)
        vbox_3.addWidget(self.role)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_phone_number = QLabel("Phone:")
        label_phone_number.setFont(self._font_.setFont(10, 500))

        self.phone_number = QLineEdit()
        self.phone_number.setFixedHeight(33)
        self.phone_number.setObjectName("phone_number")

        vbox_4.addWidget(label_phone_number)
        vbox_4.addWidget(self.phone_number)

        box_4.setLayout(vbox_4)

        hbox_2.addWidget(box_3)
        hbox_2.addWidget(box_4)

        ctn_2.setLayout(hbox_2)        

        ctn_3 = QWidget()
        vbox_5 = QVBoxLayout()
        vbox_5.setContentsMargins(0,0,0,0)
        title.setFont(self._font_.setFont(size=13, weight=700))
        vbox_5.addWidget(title, alignment=Qt.AlignCenter)
        ctn_3.setLayout(vbox_5)
        
        ctn_4 = QWidget()
        vbox_6 = QVBoxLayout()
        vbox_6.setContentsMargins(0,0,0,0)
        vbox_6.addWidget(self.btn)
        ctn_4.setLayout(vbox_6)

        self.btn.setFixedWidth(self.width()) 

        self.form.addRow(ctn_3)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_4)

        self.form.setContentsMargins(10,10,10,10)

        self.setLayout(self.form)

    def create_user(self):
        self._controller_.create_user()