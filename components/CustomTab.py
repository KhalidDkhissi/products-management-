from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QLabel, QVBoxLayout

from config.Style import Style
from config.Font import Font

class CustomTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.style = Style()
        self._font = Font()

        self.init_ui()

    def init_ui(self):
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        # Set the initial tab index
        self.setCurrentIndex(0)

        self.setStyleSheet(self.style.get("tab_style"))
        self.setFont(self._font.setFont(size=10))

    def set_tab(self, tab_name, ctn_widget, state=True):
        if tab_name and ctn_widget:
            tab = QWidget()

            lyt_tab = QVBoxLayout()
            lyt_tab.setContentsMargins(0,0,0,0)

            lyt_tab.addWidget(ctn_widget)

            tab.setLayout(lyt_tab)

            self.addTab(tab, tab_name)

            if state:
                self.setCurrentIndex(self.indexOf(tab))