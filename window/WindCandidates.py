from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt, QDate

from controllers.window.WindCandidatesController import WindCandidatesController
from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button

class WindCandidates(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindCandidatesController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(400)

        if self._action_ == "new":
            title = QLabel("Add new job")
            btn = Button(name="Add New", style="success")
            btn.clicked.connect(self.create_candidate)
        else:
            title = QLabel("Edit job")
            btn = Button(name="Edit", style="primary")
            btn.clicked.connect(self.update_candidate)

        title.setFont(self._font_.setFont(13, 400))
        title.setStyleSheet("text-align: center; width: 100%")

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_candidate_name = QLabel("Candidate name:")
        label_candidate_name.setFont(self._font_.setFont(10, 400))
        
        self.candidate_name = QLineEdit()
        self.candidate_name.setFixedHeight(33)
        self.candidate_name.setObjectName("candidate_name")

        vbox_1.addWidget(label_candidate_name)
        vbox_1.addWidget(self.candidate_name)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_email = QLabel("email:")
        label_email.setFont(self._font_.setFont(10, 400))

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

        label_phone_number = QLabel("Phone number:")
        label_phone_number.setFont(self._font_.setFont(10, 400))
        
        self.phone_number = QLineEdit()
        self.phone_number.setFixedHeight(33)
        self.phone_number.setObjectName("phone_number")

        vbox_3.addWidget(label_phone_number)
        vbox_3.addWidget(self.phone_number)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_resume_link = QLabel("Resume link:")
        label_resume_link.setFont(self._font_.setFont(10, 400))

        self.resume_link = QLineEdit()
        self.resume_link.setFixedHeight(33)
        self.resume_link.setObjectName("resume_link")

        vbox_4.addWidget(label_resume_link)
        vbox_4.addWidget(self.resume_link)

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

        label_application_date = QLabel("Application date:")
        label_application_date.setFont(self._font_.setFont(10, 400))
        
        self.application_date = QDateEdit(self)
        self.application_date.setCalendarPopup(True)
        self.application_date.setDate(QDate.currentDate())
        self.application_date.setFixedHeight(33)
        self.application_date.setObjectName("application_date")

        vbox_5.addWidget(label_application_date)
        vbox_5.addWidget(self.application_date)

        box_5.setLayout(vbox_5)
        hbox_3.addWidget(box_5)
        
        box_6 = QWidget()
        vbox_6 = QVBoxLayout()
        vbox_6.setContentsMargins(0,0,0,0)

        label_status = QLabel("status:")
        label_status.setFont(self._font_.setFont(10, 400))
        
        self.status = ComboBox(self._static_.get("status_candidates"))
        self.status.setFixedHeight(33)
        self.status.setObjectName("status")

        vbox_6.addWidget(label_status)
        vbox_6.addWidget(self.status)

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

        label_job_posting = QLabel("Job posting:")
        label_job_posting.setFont(self._font_.setFont(10, 400))

        self.job_posting = ComboBox()
        self.job_posting.setFixedHeight(33)
        self.job_posting.setObjectName("job_posting")

        vbox_7.addWidget(label_job_posting)
        vbox_7.addWidget(self.job_posting)

        box_7.setLayout(vbox_7)
        hbox_4.addWidget(box_7)

        ctn_4.setLayout(hbox_4)

        ctn_5 = QWidget()
        hbox_5 = QHBoxLayout()
        hbox_5.setContentsMargins(10,0,0,10)
        
        btn.setFixedWidth(self.width() - 20) 
        hbox_5.addWidget(btn)

        ctn_5.setLayout(hbox_5)
        
        ctn_6 = QWidget()
        hbox_6 = QHBoxLayout()
        hbox_6.setContentsMargins(10,0,0,10)
        
        hbox_6.addWidget(title, alignment=Qt.AlignCenter)

        ctn_6.setLayout(hbox_6)

        self.form.addRow(ctn_6)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_3)
        self.form.addRow(ctn_4)
        self.form.addRow(ctn_5)

        self.form.setContentsMargins(10,0,10,0)

        self.setLayout(self.form)

        self.set_combo_items()

        if self._data_ is not None:
            self.set_data()
        
    def create_candidate(self):
        self._controller_.create_candidate()

    def update_candidate(self):
        self._controller_.update_candidate(self._data_)

    def set_data(self):
        self._controller_.set_data(self._data_)

    def set_combo_items(self):
        self._controller_.set_combo_items()
