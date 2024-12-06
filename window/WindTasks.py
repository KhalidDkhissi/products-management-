from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QDateEdit
from PyQt5.QtCore import Qt, QDate

import functools

from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button
from controllers.window.WindTasksController import WindTasksController

class WindTasks(QDialog):
    def __init__(self, parent, db, data, action):
        super().__init__()

        self._db_ = db
        self._data_ = data
        self._action_ = action
        self._parent_ = parent

        self._controller_ = WindTasksController(this=self)

        self._static_ = Static()

        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(400)

        if self._action_ == "new":
            title = QLabel("Add new task")
            self.btn = Button(name="Add New", style="success")
            self.btn.clicked.connect(self.create_task)
        else:
            title = QLabel("Edit task")
            self.btn = Button(name="Edit", style="primary")
            self.btn.clicked.connect(self.update_task)

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_task_name = QLabel("Task name:")
        label_task_name.setFont(self._font_.setFont(10, 400))
        
        self.task_name = QLineEdit()
        self.task_name.setFixedHeight(33)
        self.task_name.setObjectName("task_name")

        vbox_1.addWidget(label_task_name)
        vbox_1.addWidget(self.task_name)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_description = QLabel("Description:")
        label_description.setFont(self._font_.setFont(10, 400))

        self.description = QLineEdit()
        self.description.setFixedHeight(33)
        self.description.setObjectName("description")

        vbox_2.addWidget(label_description)
        vbox_2.addWidget(self.description)

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

        label_priority = QLabel("Priority:")
        label_priority.setFont(self._font_.setFont(10, 400))
        
        self.priority  = ComboBox(self._static_.get("priority"))
        self.priority.setFixedHeight(33)
        self.priority.setObjectName("priority")

        vbox_3.addWidget(label_priority)
        vbox_3.addWidget(self.priority)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_status = QLabel("Status:")
        label_status.setFont(self._font_.setFont(10, 400))

        self.status = ComboBox(self._static_.get("status"))
        self.status.setFixedHeight(33)
        self.status.setObjectName("status")

        vbox_4.addWidget(label_status)
        vbox_4.addWidget(self.status)

        box_4.setLayout(vbox_4)

        hbox_2.addWidget(box_3)
        hbox_2.addWidget(box_4)

        ctn_2.setLayout(hbox_2)        

        ctn_5 = QWidget()
        hbox_7 = QHBoxLayout()
        hbox_7.setContentsMargins(0,0,0,0)

        box_9 = QWidget()
        vbox_8 = QVBoxLayout()
        vbox_8.setContentsMargins(0,0,0,0)

        label_due_date = QLabel("Due date:")
        label_due_date.setFont(self._font_.setFont(10, 400))
        
        self.due_date = QDateEdit(self)
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate())
        self.due_date.setFixedHeight(33)
        self.due_date.setObjectName("due_date")
        # self.due_date.setFixedWidth(box_2.width())

        vbox_8.addWidget(label_due_date)
        vbox_8.addWidget(self.due_date)
        box_9.setLayout(vbox_8)
        
        # box_10 = QWidget()
        # vbox_9 = QVBoxLayout()
        # vbox_9.setContentsMargins(0,0,0,0)

        # label_due_date = QLabel("Due date:")
        # label_due_date.setFont(self._font_.setFont(10, 400))
        
        # self.due_date = QDateEdit(self)
        # self.due_date.setCalendarPopup(True)
        # self.due_date.setDate(QDate.currentDate())
        # self.due_date.setFixedHeight(33)
        # self.due_date.setFixedWidth(box_2.width())
        # self.due_date.setObjectName("due_date")

        # vbox_9.addWidget(label_due_date)
        # vbox_9.addWidget(self.due_date)
        # box_10.setLayout(vbox_9)

        hbox_7.addWidget(box_9)
        # hbox_7.addWidget(box_10)
        ctn_5.setLayout(hbox_7)



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
        self.form.addRow(ctn_5)
        self.form.addRow(ctn_4)

        self.form.setContentsMargins(10,10,10,10)

        self.setLayout(self.form)

        if self._data_ is not None:
            self.set_data()

    def create_task(self):
        self._controller_.create_task()

    def update_task(self):
        self._controller_.update_task(self._data_)
    
    def set_data(self):
        self._controller_.set_data(self._data_)