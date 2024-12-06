from PyQt5.QtWidgets import QLineEdit, QComboBox
from PyQt5.QtCore import Qt

from db.collections.ProductsCollection import ProductsCollection
from db.collections.CategoriesCollection import CategoriesCollection
from db.collections.SuppliersCollection import SuppliersCollection
from window.Alert import Alert


class WindProductsController:
    def __init__(self, this):
        self.this = this

        self._collection_ = ProductsCollection(self.this._db_)
    
    def create_product(self):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.create_product(self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to create category <b>{name}</b>""".format(name=self.form_values["product_name"]))
            else:
                Alert("error", """Faild to create category <b>{name}</b>, try again""".format(name=self.form_values["product_name"]))

    def update_product(self, query):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.update_product(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to edit category <b>{name}</b>""".format(name=self.form_values["product_name"]))
            else:
                Alert("error", """Faild to edit category <b>{name}</b>, try again""".format(name=self.form_values["product_name"]))

    def set_data(self, data):
        _vars_ = vars(self.this)
        
        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                field_name = widget.objectName()
                widget.setText(str(data[field_name]))
            
            elif isinstance(widget, QComboBox):
                field_name = widget.objectName()
                widget.setCurrentText(str(data[field_name]))
        
    def get_values_form(self):
        _vars_ = vars(self.this)

        self.form_values = {}

        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                self.form_values[widget.objectName()] = widget.text()
                    
            elif isinstance(widget, QComboBox):
                self.form_values[widget.objectName()] = widget.currentText()

    def is_valid(self):

        error_msg = ""
        error = False

        for field, val in self.form_values.items():
            if len(val) == 0:
                error_msg += f"<p><b>{field.replace('_', ' ').capitalize()}</b> is required</p>"
                error = True
        
        if error:
            Alert("error", error_msg)
            # print("error: ", error_msg)
        
        return not error
    
    def set_combo_items(self):
        self.set_items(self.this.category_name, CategoriesCollection(self.this._db_), "category_name")
        self.set_items(self.this.supplier_name, SuppliersCollection(self.this._db_), "lieferant_name")
    
    def set_items(self, combobox, collection, col_name):
        items = collection.read_all()

        for item in items:
            combobox._items.append(item[col_name])

        combobox.set_items()
        
        