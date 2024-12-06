from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt

from controllers.views.SettingsController import SettingsController
from components.Button import Button
from components.GroupFields import GroupFields
from config.Style import Style
from config.Font import Font

class Settings(QWidget):
    def __init__(self, db):
        super().__init__()

        self._db_ = db

        self._controller_ = SettingsController(this=self)

        self._style_ = Style()
        
        self._font_ = Font()

        self._data_ = None

        self.group_widgets = [
            [
                {
                    "type": "line",
                    "name": "first_name"
                },
                {
                    "type": "line",
                    "name": "last_name"
                },
                {
                    "type": "line",
                    "name": "age"
                },
            ],
            [
                {
                    "type": "line",
                    "name": "job"
                },
                {
                    "type": "line",
                    "name": "email"
                },
                {
                    "type": "line",
                    "name": "phone_number"
                },
            ],
            [
                {
                    "type": "line",
                    "name": "address"
                },
                {
                    "type": "line",
                    "name": "city"
                },
                {
                    "type": "line",
                    "name": "country"
                },
            ],
        ]

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0,0,0,0)
        
        title = QLabel("Settings")
        title.setFont(self._font_.setFont(size=16, weight=700))

        ctn_info_admin = QWidget()
        self.form = QFormLayout()

        info = QLabel("information of Admin:")
        info.setFont(self._font_.setFont(12, 500))
        info.setContentsMargins(0,0,0, 20)
        self.form.addRow(info)

        for group in self.group_widgets:
            grp_widget = GroupFields(group)
            self.form.addRow(grp_widget)

        ctn_btn = QWidget()
        lyt_btn = QHBoxLayout()
        lyt_btn.setContentsMargins(0,0,0,0)
        
        btn = Button(name="Save", style="primary")
        btn.setFixedWidth(100) 
        btn.clicked.connect(self.update_admin)
        
        lyt_btn.addWidget(btn, alignment=Qt.AlignRight)
        ctn_btn.setLayout(lyt_btn)
        self.form.addRow(ctn_btn)

        self.form.setContentsMargins(10,10,10,10)

        ctn_info_admin.setLayout(self.form)

        box_spacing = QWidget()

        layout_main.addWidget(title)
        layout_main.addWidget(ctn_info_admin)
        layout_main.addWidget(box_spacing)

        layout_main.setStretch(0, 1)
        layout_main.setStretch(1, 1)
        layout_main.setStretch(2, 2)

        self.setLayout(layout_main)

        self.init_model()

    def init_model(self):
        self._controller_.init_model()  
              
    def update_admin(self):
        self._controller_.update_admin()        