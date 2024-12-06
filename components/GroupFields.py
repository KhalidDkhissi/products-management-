from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from components.Field import Field

class GroupFields(QWidget):
    def __init__(self, fields):
        super().__init__()

        self._fields_ = fields

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)

        box = QWidget()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)

        for field in self._fields_:
            _type_  = field["type"]
            _name_  = field["name"]
            _items_ = field["items"] if "items" in field else None

            widget = Field(_type_, _name_, _items_)
            hbox.addWidget(widget, 1)

        box.setLayout(hbox)

        vbox.addWidget(box)

        self.setLayout(vbox)

