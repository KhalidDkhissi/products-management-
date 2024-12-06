from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QDateEdit, QLabel
from PyQt5.QtCore import QDate
from components.ComboBox import ComboBox
from config.Style import Style
from config.Font import Font


class Field(QWidget):
    def __init__(self, type, field_name, items=None):
        super().__init__()

        self.type = type

        self.field_name = field_name

        self.items = items

        self._style_ = Style()

        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        label = QLabel(self.field_name.replace("_", " ").capitalize())
        label.setFont(self._font_.setFont(10, 500))

        if self.type == "line":
            field = QLineEdit()

        elif self.type == "date":
            field = QDateEdit()
            field.setDate(QDate.currentDate())
            field.setCalendarPopup(True)
            
        elif self.type == "combobox":
            field = ComboBox(items=self.items, current_index=1)

        field.setFixedHeight(33)
        field.setObjectName(self.field_name)

        layout.addWidget(label)
        layout.addWidget(field)

        self.setLayout(layout)