from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

import os


from config.Font import Font
from config.Static import Static

class Box(QWidget):
    def __init__(self, title, number):
        super().__init__()

        self.title = title
        self.number = number

        self._static_ = Static()

        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        ctn = QWidget()

        layout_ctn = QHBoxLayout()
        layout_ctn.setContentsMargins(0,0,0,0)


        box_icon = QWidget()
        vbox_icon = QVBoxLayout()
        vbox_icon.setContentsMargins(0,0,0,0)
        
        path = os.getcwd()
        path_src_img = os.path.join(path, "src/images")
        path_icon = os.path.join(path_src_img,f"dash/{self.title.lower()}.png")

        icon = QLabel()
        icon.setPixmap(QPixmap(path_icon).scaled(40, 40))

        vbox_icon.addWidget(icon, alignment=Qt.AlignCenter)

        box_icon.setLayout(vbox_icon)
        box_icon.setStyleSheet("border-radius: 10px; background: #B774FE;")
        box_icon.setFixedWidth(60)
        box_icon.setFixedHeight(60)

        box_ctn = QWidget()
        vbox_ctn = QVBoxLayout()
        vbox_ctn.setContentsMargins(0,0,0,0)

        number = QLabel(str(self.number))
        number.setFont(self._font_.setFont(15, 700))
        
        title = QLabel(self.title)
        title.setFont(self._font_.setFont(11, 400))
        title.setStyleSheet("color: #585858;")

        vbox_ctn.addWidget(number)
        vbox_ctn.addWidget(title)

        box_ctn.setLayout(vbox_ctn)

        layout_ctn.addWidget(box_icon)
        layout_ctn.addWidget(box_ctn)
        layout_ctn.setSpacing(10)

        ctn.setLayout(layout_ctn)
        # ctn.setStyleSheet("background: #F5F4F3; border-radius: 20px;")

        layout.addWidget(ctn)

        self.setLayout(layout)
        