from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate

from db.collections.TransactionsCollection import TransactionsCollection
from db.collections.ProductsCollection import ProductsCollection
from window.Alert import Alert


class WindTransactionsController:
    def __init__(self, this):
        self.this = this

        self._collection_ = TransactionsCollection(self.this._db_)

    def create_transaction(self):
        self.get_values_form()

        if self.is_valid():
            product_name = self.form_values["product_name"]
            if self._collection_.create_transaction(self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to create transaction <b>{product_name}</b>")
            else:
                Alert("error", f"Faild to create transaction <b>{product_name}</b>, try again")

    def update_transaction(self, query):
        self.get_values_form()

        if self.is_valid():
            product_name = self.form_values["product_name"]

            if self._collection_.update_transaction(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to edit transaction <b>{product_name}</b>")
            else:
                Alert("error", f"Faild to edit transaction <b>{product_name}</b>, try again")

    def set_data(self, data):
        _vars_ = vars(self.this)

        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                field_name = widget.objectName()
                widget.setText(str(data[field_name]))

            elif isinstance(widget, QDateEdit):
                field_name = widget.objectName()
                date_str = str(data[field_name])
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                widget.setDate(date)
            
            elif isinstance(widget, QComboBox):
                field_name = widget.objectName()
                widget.setCurrentText(str(data[field_name]))
                    
    def get_values_form(self):
        _vars_ = vars(self.this)

        self.form_values = {}

        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                self.form_values[widget.objectName()] = widget.text()

            elif isinstance(widget, QDateEdit):
                selected_date = widget.date()
                date_str = selected_date.toString('yyyy-MM-dd')
                self.form_values[widget.objectName()] = date_str
                    
            elif isinstance(widget, QComboBox):
                self.form_values[widget.objectName()] = widget.currentText()

    def set_combo_items(self):
        self.set_items(self.this.product_name, ProductsCollection(self.this._db_), "product_name")
    
    def set_items(self, combobox, collection, col_name):
        items = collection.read_all()

        for item in items:
            combobox._items.append(item[col_name])

        combobox.set_items()

    def is_valid(self):

        error_msg = ""
        error = False

        for field, val in self.form_values.items():
            if len(val) == 0:
                error_msg += f"<p><b>{field.replace('_', ' ').capitalize()}</b> is required</p>"
                error = True
        
        if error:
            Alert("error", error_msg)
        
        return not error