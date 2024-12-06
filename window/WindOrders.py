from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QLineEdit,QVBoxLayout, QHBoxLayout, QWidget, QListWidget
from PyQt5.QtCore import Qt

import functools

from controllers.window.WindOrdersController import WindOrdersController
from config.Font import Font
from config.Static import Static
from components.Button import Button
from components.Field import Field
from components.GroupFields import GroupFields
from components.CustomTable import CustomTable

class WindOrders(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindOrdersController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.customer_fields = [
            [
                {
                    "type": "line",
                    "name": "first_name",
                    "is_digit": False
                },
                {
                    "type": "line",
                    "name": "last_name",
                    "is_digit": False
                },
                {
                    "type": "line",
                    "name": "email",
                    "is_digit": False
                },
            ],
            [
                {
                    "type": "line",
                    "name": "phone_number",
                    "is_digit": False
                },
                {
                    "type": "line",
                    "name": "city",
                    "is_digit": False
                },
                {
                    "type": "line",
                    "name": "country",
                    "is_digit": False
                },
            ]
        ]

        self.discount_fields = [
            [
                {
                    "type": "line",
                    "name": "discount",
                    "is_event": True,
                    "is_digit": True
                },
                {
                    "type": "combobox",
                    "name": "discount_type",
                    "items": ["Fixed Amount", "Percentage"],
                    "is_event": True,
                    "is_digit": False
                },
                {
                    "type": "line",
                    "name": "discount_reason",
                    "is_event": False,
                    "is_digit": False
                },
            ]
        ]
        
        self.field_note = [
            [
                {
                    "type": "line", 
                    "name": "note",
                    "is_digit": False
                }
            ]
        ]

        self.data_table_products = {
            "thead": ["Product Name", "Price", "Quantity", "Total", "Actions"],
            "size": [0.2, 0.1, 0.2, 0.2, 0.2]
        }
        
        self.data_table_total = {
            "thead": ["Subtotal", "Discount", "Shipping fee", "VAT", "Total"],
            "size": [0.2, 0.1, 0.2, 0.2, 0.2]
        }

        self.init_ui()

        self._controller_.add_event(self.discount_fields, self.form_discount)

    def init_ui(self):
        self.setFixedWidth(800)

        layout_main = QVBoxLayout()
        
        if self._action_ == "new":
            title = QLabel("Add new order")
            btn = Button(name="Add New Order", style="success")
            btn.clicked.connect(self.create_order)
        else:
            title = QLabel("Edit order")
            btn = Button(name="Edit Order", style="primary")
            btn.clicked.connect(self.update_order)

        lyt_title = QHBoxLayout()
        lyt_title.setContentsMargins(0,0,0, 15)

        title.setFont(self._font_.setFont(13, 500))
        
        lyt_title.addWidget(title, alignment=Qt.AlignCenter)
        ctn_title = QWidget()
        ctn_title.setLayout(lyt_title)

        label_customer = QLabel("Customer information:")
        label_customer.setFont(self._font_.setFont(11, 500))

        self.form_customer = QFormLayout()
        self.form_customer.setContentsMargins(0,0,0,0)
        
        for field in self.customer_fields:
            grp_widget = GroupFields(field)
            self.form_customer.addRow(grp_widget)

        ctn_customer = QWidget()
        ctn_customer.setLayout(self.form_customer)

        lyt_search = QVBoxLayout()
        lyt_search.setContentsMargins(0,0,0,0)

        self.search_field = QLineEdit()
        self.search_field.setObjectName("search_of_product")
        self.search_field.setFixedHeight(33)
        self.search_field.textChanged.connect(self.search_product)

        self.results_list = QListWidget()
        # self.results_list.currentItem().text()
        self.results_list.itemClicked.connect(self.select_item_search)
        self.msg_label_search = QLabel("", self)
        
        lyt_search.addWidget(self.search_field)
        lyt_search.addWidget(self.results_list)
        lyt_search.addWidget(self.msg_label_search)

        ctn_search = QWidget()
        ctn_search.setLayout(lyt_search)

        self.table_products = self.render_table(self.data_table_products)

        label_discount = QLabel("Discount:")
        label_discount.setFont(self._font_.setFont(11, 500))

        self.form_discount = QFormLayout()
        self.form_discount.setContentsMargins(0,0,0,0)
        
        for field in self.discount_fields:
            grp_widget = GroupFields(field)
            self.form_discount.addRow(grp_widget)

        ctn_discount = QWidget()
        ctn_discount.setLayout(self.form_discount)

        self.table_total   = self.render_table(self.data_table_total)
        # self.table_total.clear()

        self.form_note = QFormLayout()
        self.form_note.setContentsMargins(0,0,0,0)

        for field in self.field_note:
            grp_widget = GroupFields(field)
            self.form_note.addRow(grp_widget)
        
        ctn_note = QWidget()
        ctn_note.setLayout(self.form_note)

        lyt_btn = QHBoxLayout()
        lyt_btn.setContentsMargins(0,0,0,0)
        lyt_btn.addWidget(btn, alignment=Qt.AlignRight)
        ctn_btn = QWidget()
        ctn_btn.setLayout(lyt_btn)


        layout_main.addWidget(ctn_title)
        layout_main.addWidget(label_customer)
        layout_main.addWidget(ctn_customer)
        layout_main.addWidget(ctn_search)
        layout_main.addWidget(self.table_products)
        layout_main.addWidget(label_discount)
        layout_main.addWidget(ctn_discount)
        layout_main.addWidget(self.table_total)
        layout_main.addWidget(ctn_note)
        layout_main.addWidget(ctn_btn)

        self.setLayout(layout_main)

        if self._data_ is not None:
            self.set_data()
            
        print("done...")

    def render_table(self, thead):
        return self._controller_.render_table(thead)
        
    def create_order(self):
        self._controller_.create_order()

    def update_order(self):
        self._controller_.update_order(self._data_)

    def set_data(self):
        # print("\n _data_= ", self._data_)
        self._controller_.set_data(self._data_)

    def search_product(self):
        self._controller_.search_product()

    def select_item_search(self):
        self._controller_.select_item_search()