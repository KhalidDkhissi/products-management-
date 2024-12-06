from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate

from db.collections.TasksCollection import TasksCollection
from window.Alert import Alert


class WindTasksController:
    def __init__(self, this):
        self.this = this

        self._collection_ = TasksCollection(self.this._db_)

    def create_task(self):
        self.get_values_form()

        if self.is_valid():
            tabs_table = self.this._parent_.tabs_table
            current_tab_index = tabs_table.currentIndex()
            current_tab_name = tabs_table.tabText(current_tab_index)
            user_id = self.this._parent_.tabs_id[current_tab_name]
            self.form_values["user_id"] = user_id

            task = self._collection_.create_task(self.form_values)
            if task["_id"]:
                self.this.state = True
                self.this.task = task
                self.this.close()
                Alert("success", """Success to create task <b>{name}</b>""".format(name=self.form_values["task_name"]))
            else:
                Alert("error", """Faild to create task <b>{name}</b>, try again""".format(name=self.form_values["task_name"]))

    def update_task(self, query):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.update_task(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to edit task <b>{name}</b>""".format(name=self.form_values["task_name"]))
            else:
                Alert("error", """Faild to edit task <b>{name}</b>, try again""".format(name=self.form_values["task_name"]))

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

        print("...Done seting data ...")
        
    def get_values_form(self):
        _vars_ = vars(self.this)

        self.form_values = {}

        for attr, widget in _vars_.items():

            if isinstance(widget, QLineEdit):
                self.form_values[widget.objectName()] = widget.text()
                    
            elif isinstance(widget, QComboBox):
                self.form_values[widget.objectName()] = widget.currentText()
            
            elif isinstance(widget, QDateEdit):
                selected_date = widget.date()
                date_str = selected_date.toString('yyyy-MM-dd')
                self.form_values[widget.objectName()] = date_str

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