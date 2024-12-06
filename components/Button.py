from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

import os

from config.Style import Style
from config.Font import Font

class Button(QPushButton):
    def __init__(self, name="", size="normal", style="primary", icon_path=""):
        super().__init__()
        self._style_ = Style()

        if len(name) > 0:
            self.set_name(name)
        
        if len(icon_path) > 0:
            self.set_icon(icon_path)
        
        self.set_size(size)

        self.set_style(size, style)

        self.setCursor(Qt.PointingHandCursor)

    def set_name(self, name):
            self.setText(name)

    def set_icon(self, icon_path):
        if icon_path:
            path = os.path.join(os.getcwd(), "src/images", icon_path)
            
            icon = QIcon()
            icon.addFile(path, QSize(32, 32))

            self.setIcon(QIcon(path))

    def set_size(self, size):
        if size == 'normal':
            self.setFixedSize(QSize(115, 33))  
            self.setFont(Font().setFont(size=10, weight=600))
        elif size == 'small':
            self.setFixedSize(QSize(80, 30))
            self.setFont(Font().setFont(size=9, weight=400))
        elif size == 'large':
            self.setFixedSize(QSize(130, 40))
            self.setFont(Font().setFont(size=14, weight=700))
        elif size == 'icon':
            self.setFixedSize(QSize(35, 35))
            self.setFont(Font().setFont(size=0, weight=0))

    def set_style(self, size, style):
        btn_style = self._style_.get("btn-icon" if size == "icon" else "btn-default")

        if style == 'primary':
            btn_style += self._style_.get("btn-primary")
        elif style == 'secondary':
            btn_style += self._style_.get("btn-secondary")
        elif style == 'success':
            btn_style += self._style_.get("btn-success")
        elif style == 'error':
            btn_style += self._style_.get("btn-error")

        btn_style += "border-radius: 17.5px;" if size == "icon" else ""
        
        self.setStyleSheet(btn_style)