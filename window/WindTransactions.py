from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QDateEdit
from PyQt5.QtCore import Qt, QDate

from controllers.window.WindTransactionsController import WindTransactionsController
from config.Font import Font
from config.Static import Static
from components.Button import Button
from components.ComboBox import ComboBox

class WindTransactions(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindTransactionsController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(500)

        if self._action_ == "new":
            title = QLabel("Add new transaction")
            btn = Button(name="Add New", style="success")
            btn.clicked.connect(self.create_transaction)
        else:
            title = QLabel("Edit transaction")
            btn = Button(name="Edit", style="primary")
            btn.clicked.connect(self.update_transaction)

        title.setFont(self._font_.setFont(13, 500))
        title.setStyleSheet("text-align: center; width: 100%")

        self.form = QFormLayout()

        ctn_1 = QWidget()
        hbox_1 = QHBoxLayout()
        hbox_1.setContentsMargins(0,0,0,0)

        box_1 = QWidget()
        vbox_1 = QVBoxLayout()
        vbox_1.setContentsMargins(0,0,0,0)

        label_product_name = QLabel("Product name:")
        label_product_name.setFont(self._font_.setFont(10, 500))
        
        self.product_name = ComboBox()
        self.product_name.setFixedHeight(33)
        self.product_name.setFixedWidth(int(self.width() / 2 - 13))
        self.product_name.setObjectName("product_name")

        vbox_1.addWidget(label_product_name)
        vbox_1.addWidget(self.product_name)

        box_1.setLayout(vbox_1)

        box_2 = QWidget()
        vbox_2 = QVBoxLayout()
        vbox_2.setContentsMargins(0,0,0,0)
        
        label_quantity = QLabel("Qunatity:")
        label_quantity.setFont(self._font_.setFont(10, 500))

        self.quantity = QLineEdit()
        self.quantity.setFixedHeight(33)
        self.quantity.setFixedWidth(int(self.width() / 2 - 13))
        self.quantity.setObjectName("quantity")

        vbox_2.addWidget(label_quantity)
        vbox_2.addWidget(self.quantity)

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

        label_transactions_type = QLabel("Transactions type:")
        label_transactions_type.setFont(self._font_.setFont(10, 500))
        
        self.transactions_type = ComboBox(self._static_.get("transactions_type"))
        self.transactions_type.setFixedHeight(33)
        self.transactions_type.setObjectName("transactions_type")

        vbox_3.addWidget(label_transactions_type)
        vbox_3.addWidget(self.transactions_type)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_transactions_date = QLabel("Transactions date:")
        label_transactions_date.setFont(self._font_.setFont(10, 500))

        self.transactions_date = QDateEdit()
        self.transactions_date.setCalendarPopup(True)
        self.transactions_date.setDate(QDate.currentDate())
        self.transactions_date.setFixedHeight(33)
        self.transactions_date.setObjectName("transactions_date")

        vbox_4.addWidget(label_transactions_date)
        vbox_4.addWidget(self.transactions_date)

        box_4.setLayout(vbox_4)

        hbox_2.addWidget(box_3)
        hbox_2.addWidget(box_4)

        ctn_2.setLayout(hbox_2)

        ctn_3 = QWidget()
        vbox_5 = QVBoxLayout()
        vbox_5.setContentsMargins(0,0,0,0)
        vbox_5.addWidget(title, alignment=Qt.AlignCenter)
        ctn_3.setLayout(vbox_5)
        
        ctn_4 = QWidget()
        vbox_6 = QVBoxLayout()
        vbox_6.setContentsMargins(0,0,0,0)
        btn.setFixedWidth(self.width() - 22) 
        vbox_6.addWidget(btn)
        ctn_4.setLayout(vbox_6)

        self.form.addRow(ctn_3)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_4)

        self.form.setContentsMargins(10,10,10,10)

        self.setLayout(self.form)
        
        self.set_combo_items()

        if self._data_ is not None:
            self.set_data()
        
    def create_transaction(self):
        self._controller_.create_transaction()

    def update_transaction(self):
        self._controller_.update_transaction(self._data_)

    def set_data(self):
        self._controller_.set_data(self._data_)

    def set_combo_items(self):
        self._controller_.set_combo_items()

