from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit,QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

import functools

from controllers.window.WindSuppliersController import WindSuppliersController
from config.Font import Font
from config.Static import Static
from components.Button import Button

class WindSuppliers(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindSuppliersController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(500)
        
        if self._action_ == "new":
            title = QLabel("Add new supplier")
            self.btn = Button(name="Add New", style="success")
            self.btn.clicked.connect(self.create_supplier)
        else:
            title = QLabel("Edit supplier")
            self.btn = Button(name="Edit", style="primary")
            self.btn.clicked.connect(self.update_supplier)

        title.setFont(self._font_.setFont(13, 500))
        title.setStyleSheet("text-align: center; width: 100%")

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_supplier_name = QLabel("Supplier name:")
        label_supplier_name.setFont(self._font_.setFont(10, 500))
        
        self.supplier_name = QLineEdit()
        self.supplier_name.setFixedHeight(33)
        self.supplier_name.setObjectName("supplier_name")

        vbox_1.addWidget(label_supplier_name)
        vbox_1.addWidget(self.supplier_name)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_contact_person = QLabel("Contact person:")
        label_contact_person.setFont(self._font_.setFont(10, 500))

        self.contact_person = QLineEdit()
        self.contact_person.setFixedHeight(33)
        self.contact_person.setObjectName("contact_person")

        vbox_2.addWidget(label_contact_person)
        vbox_2.addWidget(self.contact_person)

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

        label_email = QLabel("Email:")
        label_email.setFont(self._font_.setFont(10, 500))
        
        self.email = QLineEdit()
        self.email.setFixedHeight(33)
        self.email.setObjectName("email")

        vbox_3.addWidget(label_email)
        vbox_3.addWidget(self.email)

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
        hbox_3 = QHBoxLayout()
        hbox_3.setContentsMargins(0,0,0,0)

        box_5 = QWidget()
        vbox_5 = QVBoxLayout()
        vbox_5.setContentsMargins(0,0,0,0)

        label_address = QLabel("Address:")
        label_address.setFont(self._font_.setFont(10, 500))
        
        self.address = QLineEdit()
        self.address.setFixedHeight(33)
        self.address.setObjectName("address")

        vbox_5.addWidget(label_address)
        vbox_5.addWidget(self.address)

        box_5.setLayout(vbox_5)
        hbox_3.addWidget(box_5)
        ctn_3.setLayout(hbox_3)

        self.btn.setFixedWidth(self.width()) 
        self.btn.setContentsMargins(0,20,20,0)

        self.form.addRow(title)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_3)
        self.form.addRow(self.btn)

        self.form.setContentsMargins(10,0,10,0)

        self.setLayout(self.form)

        if self._data_ is not None:
            self.set_data()
            
        print("done...")
        
    def create_supplier(self):
        self._controller_.create_supplier()

    def update_supplier(self):
        self._controller_.update_supplier(self._data_)

    def set_data(self):
        self._controller_.set_data(self._data_)

