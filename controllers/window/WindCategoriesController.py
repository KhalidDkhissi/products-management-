from PyQt5.QtWidgets import QLineEdit, QComboBox

from db.collections.CategoriesCollection import CategoriesCollection
from window.Alert import Alert


class WindCategoriesController:
    def __init__(self, this):
        self.this = this

        self._collection_ = CategoriesCollection(self.this._db_)

    def create_category(self):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.create_category(self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to create category <b>{name}</b>""".format(name=self.form_values["category_name"]))
            else:
                Alert("error", """Faild to create category <b>{name}</b>, try again""".format(name=self.form_values["category_name"]))

    def update_category(self, query):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.update_category(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to edit category <b>{name}</b>""".format(name=self.form_values["category_name"]))
            else:
                Alert("error", """Faild to edit category <b>{name}</b>, try again""".format(name=self.form_values["category_name"]))

    def set_data(self, data):
        _vars_ = vars(self.this)

        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                field_name = widget.objectName()
                widget.setText(str(data[field_name]))
                    
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
        
        return not error