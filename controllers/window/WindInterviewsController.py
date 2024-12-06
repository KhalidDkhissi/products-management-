from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate


from db.collections.JobPostingsCollection import JobPostingsCollection
from db.collections.CandidatesCollection import CandidatesCollection
from db.collections.InterviewsCollection import InterviewsCollection
from window.Alert import Alert


class WindInterviewsController:
    def __init__(self, this):
        self.this = this

        self._collection_ = InterviewsCollection(self.this._db_)

    def create_interview(self):
        self.get_values_form()

        if self.is_valid():
            candidate_name = self.form_values['candidate_name']
            if self._collection_.create_interview(self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to create interview <b>{candidate_name}</b>")
            else:
                Alert("error", f"Faild to create interview <b>{candidate_name}</b>, try again")

    def update_interview(self, query):
        self.get_values_form()

        if self.is_valid():
            candidate_name = self.form_values['candidate_name']
            if self._collection_.update_interview(query, self.form_values):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to edit interview <b>{candidate_name}</b>")
            else:
                Alert("error", f"Faild to edit interview <b>{candidate_name}</b>, try again")

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
        self.set_items(self.this.candidate_name, CandidatesCollection(self.this._db_), "candidate_name")
        self.set_items(self.this.job_posting, JobPostingsCollection(self.this._db_), "job_title")
    
    def set_items(self, combobox, collection, col_name):
        items = collection.read_all()

        for item in items:
            combobox._items.append(item[col_name])

        combobox.set_items()

