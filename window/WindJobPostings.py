from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt, QDate

from controllers.window.WindJobPostingsController import WindJobPostingsController
from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button

class WindJobPostings(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindJobPostingsController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(500)

        if self._action_ == "new":
            title = QLabel("Add new job")
            btn = Button(name="Add New", style="success")
            btn.clicked.connect(self.create_job_posting)
        else:
            title = QLabel("Edit job")
            btn = Button(name="Edit", style="primary")
            btn.clicked.connect(self.update_job_posting)

        title.setFont(self._font_.setFont(13, 500))
        title.setStyleSheet("text-align: center; width: 100%")

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_job_title = QLabel("Job title:")
        label_job_title.setFont(self._font_.setFont(10, 500))
        
        self.job_title = QLineEdit()
        self.job_title.setFixedHeight(33)
        self.job_title.setObjectName("job_title")

        vbox_1.addWidget(label_job_title)
        vbox_1.addWidget(self.job_title)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_department = QLabel("Department:")
        label_department.setFont(self._font_.setFont(10, 500))

        self.department = QLineEdit()
        self.department.setFixedHeight(33)
        self.department.setObjectName("department")

        vbox_2.addWidget(label_department)
        vbox_2.addWidget(self.department)

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

        label_job_description = QLabel("Job description:")
        label_job_description.setFont(self._font_.setFont(10, 500))
        
        self.job_description = QLineEdit()
        self.job_description.setFixedHeight(33)
        self.job_description.setObjectName("job_description")

        vbox_3.addWidget(label_job_description)
        vbox_3.addWidget(self.job_description)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_requirements = QLabel("Requirements:")
        label_requirements.setFont(self._font_.setFont(10, 500))

        self.requirements = QLineEdit()
        self.requirements.setFixedHeight(33)
        self.requirements.setObjectName("requirements")

        vbox_4.addWidget(label_requirements)
        vbox_4.addWidget(self.requirements)

        box_4.setLayout(vbox_4)

        hbox_2.addWidget(box_3)
        hbox_2.addWidget(box_4)

        ctn_2.setLayout(hbox_2)
        


        ctn_3 = QWidget()
        hbox_3 = QHBoxLayout()
        hbox_3.setContentsMargins(0,0,0,0)

        box_5 = QWidget()
        vbox_5 = QVBoxLayout()
        vbox_5.setContentsMargins(0,0,0,0)

        label_posted_date = QLabel("Posted date:")
        label_posted_date.setFont(self._font_.setFont(10, 500))
        
        self.posted_date = QDateEdit(self)
        self.posted_date.setCalendarPopup(True)
        self.posted_date.setDate(QDate.currentDate())
        self.posted_date.setFixedHeight(33)
        self.posted_date.setObjectName("posted_date")

        vbox_5.addWidget(label_posted_date)
        vbox_5.addWidget(self.posted_date)

        box_5.setLayout(vbox_5)
        hbox_3.addWidget(box_5)
        
        box_6 = QWidget()
        vbox_6 = QVBoxLayout()
        vbox_6.setContentsMargins(0,0,0,0)

        label_closing_date = QLabel("Closing date:")
        label_closing_date.setFont(self._font_.setFont(10, 500))
        
        self.closing_date = QDateEdit(self)
        self.closing_date.setCalendarPopup(True)
        self.closing_date.setDate(QDate.currentDate())
        self.closing_date.setFixedHeight(33)
        self.closing_date.setFixedHeight(33)
        self.closing_date.setObjectName("closing_date")

        vbox_6.addWidget(label_closing_date)
        vbox_6.addWidget(self.closing_date)

        box_6.setLayout(vbox_6)

        hbox_3.addWidget(box_5)
        hbox_3.addWidget(box_6)
        
        ctn_3.setLayout(hbox_3)


        ctn_4 = QWidget()
        hbox_4 = QHBoxLayout()
        hbox_4.setContentsMargins(0,0,0,0)

        box_7 = QWidget()
        vbox_7 = QVBoxLayout()
        vbox_7.setContentsMargins(0,0,0,0)

        label_status = QLabel("status:")
        label_status.setFont(self._font_.setFont(10, 500))
        
        self.status = ComboBox(self._static_.get("status_jobs"))
        self.status.setFixedHeight(33)
        self.status.setObjectName("status")

        vbox_7.addWidget(label_status)
        vbox_7.addWidget(self.status)

        box_7.setLayout(vbox_7)
        hbox_4.addWidget(box_7)

        ctn_4.setLayout(hbox_4)

        ctn_5 = QWidget()
        hbox_5 = QHBoxLayout()
        hbox_5.setContentsMargins(0,0,0,0)
        
        btn.setFixedWidth(self.width() - 20) 
        hbox_5.addWidget(btn)

        ctn_5.setLayout(hbox_5)

        self.form.addRow(title)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_3)
        self.form.addRow(ctn_4)
        self.form.addRow(ctn_5)

        self.form.setContentsMargins(10,0,10,0)

        self.setLayout(self.form)

        if self._data_ is not None:
            self.set_data()
        
    def create_job_posting(self):
        self._controller_.create_job_posting()

    def update_job_posting(self):
        self._controller_.update_job_posting(self._data_)

    def set_data(self):
        self._controller_.set_data(self._data_)

