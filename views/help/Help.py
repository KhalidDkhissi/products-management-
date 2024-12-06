from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QSettings, Qt

from config.Style import Style
from config.Static import Static
from config.Font import Font

class Help(QWidget):
    def __init__(self):
        super().__init__()

        self._style_ = Style()
        self._static_ = Static()
        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(20,20,20,20)
        
        title = QLabel("Help")
        title.setFont(self._font_.setFont(size=16, weight=700))
        title.setContentsMargins(0,0,0,30)

        intro = QLabel("Introduction:")
        intro.setFont(self._font_.setFont(size=13, weight=600))
        intro.setContentsMargins(0,0,0,5)

        dep_intro = QLabel(self._static_.get("intro"))
        dep_intro.setFont(self._font_.setFont(size=10, weight=400))
        dep_intro.setContentsMargins(0,0,0,10)
        
        inventory = QLabel("Inventory Management:")
        inventory.setFont(self._font_.setFont(size=13, weight=600))
        inventory.setContentsMargins(0,0,0,5)

        dep_inventory = QLabel(self._static_.get("inventory"))
        dep_inventory.setFont(self._font_.setFont(size=10, weight=400))
        dep_inventory.setContentsMargins(0,0,0,10)
        
        task = QLabel("Task Management:")
        task.setFont(self._font_.setFont(size=13, weight=600))
        task.setContentsMargins(0,0,0,5)

        dep_task = QLabel(self._static_.get("task"))
        dep_task.setFont(self._font_.setFont(size=10, weight=400))
        dep_task.setContentsMargins(0,0,0,10)
        
        recruitment = QLabel("HR Recruitment Management:")
        recruitment.setFont(self._font_.setFont(size=13, weight=600))
        recruitment.setContentsMargins(0,0,0,5)

        dep_recruitment = QLabel(self._static_.get("recruitment"))
        dep_recruitment.setFont(self._font_.setFont(size=10, weight=400))

        layout_main.addWidget(title)
        layout_main.addWidget(intro)
        layout_main.addWidget(dep_intro)
        layout_main.addWidget(inventory)
        layout_main.addWidget(dep_inventory)
        layout_main.addWidget(task)
        layout_main.addWidget(dep_task)
        layout_main.addWidget(recruitment)
        layout_main.addWidget(dep_recruitment)
        layout_main.setSpacing(0)

        
        self.setLayout(layout_main)