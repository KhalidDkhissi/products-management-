from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate

from db.collections.CandidatesCollection import CandidatesCollection
from db.collections.JobPostingsCollection import JobPostingsCollection
from window.Alert import Alert


class WindCandidatesController:
    def __init__(self, this):
        self.this = this

        self._collection_ = CandidatesCollection(self.this._db_)

    def create_candidate(self):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.create_candidate(self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to create candidate <b>{name}</b>""".format(name=self.form_values["candidate_name"]))
            else:
                Alert("error", """Faild to create candidate <b>{name}</b>, try again""".format(name=self.form_values["candidate_name"]))

    def update_candidate(self, query):
        self.get_values_form()

        if self.is_valid():

            if self._collection_.update_candidate(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", """Success to edit candidate <b>{name}</b>""".format(name=self.form_values["candidate_name"]))
            else:
                Alert("error", """Faild to edit candidate <b>{name}</b>, try again""".format(name=self.form_values["candidate_name"]))

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
    
    def set_combo_items(self):
        combobox = self.this.job_posting
        
        collection = JobPostingsCollection(self.this._db_)

        items = collection.read_all()

        for item in items:
            combobox._items.append(item["job_title"])

        combobox.set_items()