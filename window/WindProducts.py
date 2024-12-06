from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

from controllers.window.WindProductsController import WindProductsController
from config.Font import Font
from config.Static import Static
from components.ComboBox import ComboBox
from components.Button import Button

class WindProducts(QDialog):
    def __init__(self, db, data, action):
        super().__init__()
        
        self._db_ = db
        self._data_ = data
        self._action_ = action

        self._controller_ = WindProductsController(this=self)
        self._static_ = Static()
        self._font_ = Font()

        self.state = False

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(600)
        
        if self._action_ == "new":
            title = QLabel("Add new product")
            btn = Button(name="Add New", style="success")
            btn.clicked.connect(self.create_product)
        else:
            title = QLabel("Edit product")
            btn = Button(name="Edit", style="primary")
            btn.clicked.connect(self.update_product)

        title.setFont(self._font_.setFont(13, 500))
        title.setStyleSheet("text-align: center; width: 100%")

        title.setFont(self._font_.setFont(10, 500))
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
        
        self.product_name = QLineEdit()
        self.product_name.setFixedHeight(33)
        self.product_name.setObjectName("product_name")

        vbox_1.addWidget(label_product_name)
        vbox_1.addWidget(self.product_name)

        box_1.setLayout(vbox_1)

        hbox_1.addWidget(box_1)

        ctn_1.setLayout(hbox_1)

        ctn_2 = QWidget()
        hbox_2 = QHBoxLayout()
        hbox_2.setContentsMargins(0,0,0,0)

        box_3 = QWidget()
        vbox_3 = QVBoxLayout()
        vbox_3.setContentsMargins(0,0,0,0)

        label_quantity = QLabel("Quantity:")
        label_quantity.setFont(self._font_.setFont(10, 500))
        
        self.quantity = QLineEdit()
        self.quantity.setFixedHeight(33)
        self.quantity.setObjectName("quantity")

        vbox_3.addWidget(label_quantity)
        vbox_3.addWidget(self.quantity)

        box_3.setLayout(vbox_3)

        box_4 = QWidget()
        vbox_4 = QVBoxLayout()
        vbox_4.setContentsMargins(0,0,0,0)
        
        label_reorder_level = QLabel("Reorder level:")
        label_reorder_level.setFont(self._font_.setFont(10, 500))

        self.reorder_level  = QLineEdit()
        self.reorder_level .setFixedHeight(33)
        self.reorder_level .setObjectName("reorder_level ")

        vbox_4.addWidget(label_reorder_level)
        vbox_4.addWidget(self.reorder_level)

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

        label_category_name = QLabel("Category name:")
        label_category_name.setFont(self._font_.setFont(10, 500))
        
        self.category_name = ComboBox()
        self.category_name.setFixedHeight(33)
        self.category_name.setObjectName("category_name")

        vbox_5.addWidget(label_category_name)
        vbox_5.addWidget(self.category_name)

        box_5.setLayout(vbox_5)

        box_6 = QWidget()
        vbox_6 = QVBoxLayout()
        vbox_6.setContentsMargins(0,0,0,0)
        
        label_supplier_name = QLabel("lieferant_name:")
        label_supplier_name.setFont(self._font_.setFont(10, 500))

        self.supplier_name = ComboBox()
        self.supplier_name.setFixedHeight(33)
        self.supplier_name.setObjectName("lieferant_name")

        vbox_6.addWidget(label_supplier_name)
        vbox_6.addWidget(self.supplier_name)

        box_6.setLayout(vbox_6)

        hbox_3.addWidget(box_5)
        hbox_3.addWidget(box_6)

        ctn_3.setLayout(hbox_3)

        ctn_5 = QWidget()
        hbox_4 = QHBoxLayout()
        hbox_4.setContentsMargins(0,0,0,0)

        box_8 = QWidget()
        vbox_8 = QVBoxLayout()
        vbox_8.setContentsMargins(0,0,0,0)
        
        label_wholesale_price = QLabel("Wholesale price:")
        label_wholesale_price.setFont(self._font_.setFont(10, 500))

        self.wholesale_price = QLineEdit()
        self.wholesale_price.setFixedHeight(33)
        self.wholesale_price.setObjectName("wholesale_price")

        vbox_8.addWidget(label_wholesale_price)
        vbox_8.addWidget(self.wholesale_price)

        box_8.setLayout(vbox_8)
        
        box_9 = QWidget()
        vbox_9 = QVBoxLayout()
        vbox_9.setContentsMargins(0,0,0,0)
        
        label_selling_price = QLabel("Selling price:")
        label_selling_price.setFont(self._font_.setFont(10, 500))

        self.selling_price = QLineEdit()
        self.selling_price.setFixedHeight(33)
        self.selling_price.setObjectName("selling_price")

        vbox_9.addWidget(label_selling_price)
        vbox_9.addWidget(self.selling_price)

        box_9.setLayout(vbox_9)

        hbox_4.addWidget(box_8)
        hbox_4.addWidget(box_9)

        ctn_5.setLayout(hbox_4)


        ctn_4 = QWidget()
        vbox_7 = QVBoxLayout()
        vbox_7.setContentsMargins(0,0,0,0)
        btn.setFixedWidth(ctn_4.width() - 20) 
        vbox_7.addWidget(btn)
        ctn_4.setLayout(vbox_7)

        self.form.addRow(title)
        self.form.addRow(ctn_1)
        self.form.addRow(ctn_2)
        self.form.addRow(ctn_3)
        self.form.addRow(ctn_5)
        self.form.addRow(ctn_4)

        self.setLayout(self.form)

        self.set_combo_items()

        if self._data_ is not None:
            self.set_data()
        
    def create_product(self):
        self._controller_.create_product()

    def update_product(self):
        self._controller_.update_product(self._data_)

    def set_data(self):
        self._controller_.set_data(self._data_)

    def set_combo_items(self):
        self._controller_.set_combo_items()
