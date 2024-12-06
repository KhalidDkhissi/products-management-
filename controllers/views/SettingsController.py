from PyQt5.QtWidgets import QLineEdit, QDateEdit
from PyQt5.QtCore import QDate
from db.collections.AdminsCollection import AdminsCollection
from components.Field import Field
from components.ComboBox import ComboBox
from components.GroupFields import GroupFields
from db.collections.AdminsCollection import AdminsCollection
from window.Alert import Alert

class SettingsController:
    def __init__(self, this):
        self.this = this

        self._admin_ = AdminsCollection(self.this._db_)

    def init_model(self):
        data = self._admin_.collection.find_one()
        
        self.this._data_ = data

        self.set_data(data)
        

    def get_data(self):
        form_layout = self.this.form

        data = {}
        
        for group in self.this.group_widgets:
            for field in group:
                field_name = field["name"]
                grp_widget = next((grp_widget for grp_widget in [form_layout.itemAt(i).widget() for i in range(form_layout.count())] if isinstance(grp_widget, GroupFields) and any(f["name"] == field_name for f in grp_widget._fields_)), None)
                if grp_widget:
                    field_widget = self.find_field_widget(grp_widget, field_name)
                    if field_widget:
                        if field_widget.type == "line":
                            data[field_name] = field_widget.findChild(QLineEdit).text()
                        elif field_widget.type == "date":
                            data[field_name] = field_widget.findChild(QDateEdit).date().toString("yyyy-MM-dd")
                        elif field_widget.type == "combobox":
                            data[field_name] = field_widget.findChild(ComboBox).currentText()
        return data

    def set_data(self, data):
        form_layout = self.this.form

        for group in self.this.group_widgets:
            for field in group:
                field_name = field["name"]
                grp_widget = next((grp_widget for grp_widget in [form_layout.itemAt(i).widget() for i in range(form_layout.count())] if isinstance(grp_widget, GroupFields) and any(f["name"] == field_name for f in grp_widget._fields_)), None)
                if grp_widget:
                    field_widget = self.find_field_widget(grp_widget, field_name)
                    if field_widget:
                        if field_widget.type == "line":
                            field_widget.findChild(QLineEdit).setText(str(data[field_name]))
                        elif field_widget.type == "date":
                            field_widget.findChild(QDateEdit).setDate(QDate.fromString(str(data[field_name]), "yyyy-MM-dd"))
                        elif field_widget.type == "combobox":
                            index = field_widget.findChild(ComboBox).findText(str(data[field_name]))
                            if index != -1:
                                field_widget.findChild(ComboBox).setCurrentIndex(index)

    def find_field_widget(self, parent, field_name):
        for child in parent.children():
            if isinstance(child, Field) and child.field_name == field_name:
                return child
            elif child.children():
                field_widget = self.find_field_widget(child, field_name)
                if field_widget:
                    return field_widget
        return None
    
    def update_admin(self):
        update_data = self.get_data()
        old_data = self.this._data_

        if old_data and update_data:
            result = self._admin_.update_admin(old_data, update_data)

            if result:
                Alert("success", f"Success to update information of admin <b>{update_data['first_name']} {update_data['last_name']}</b>")
                self.set_data(update_data)