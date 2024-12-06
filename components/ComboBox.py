from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QSize

from config.Style import Style
from config.Font import Font

class ComboBox(QComboBox):
    def __init__(self,items=None, parent=None, current_index=0):
        super(ComboBox, self).__init__(parent)

        self._style_ = Style()
        self._font_ = Font()

        self._items = items or []

        self._current_index = current_index

        self.init_ui()

    def init_ui(self):
        if len(self._items) > 0:
            self.set_items()

        self.setStyleSheet(self._style_.get("combobox"))

        # self.setFixedSize(QSize(180, 33))  
        
        self.setFont(self._font_.setFont(size=10, weight=600))
        
        # self.setCurrentIndex(-1)  # Set the current index to -1 to deselect the first item

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, value):
        self._current_index = value
        self.setCurrentIndex(value)

    def clear_selection(self):
        self.setCurrentIndex(-1)

    @property
    def items(self):
        return self._items

    

    def set_items(self):
        
        if self._items:
            self.clear()
            self.addItem("")
            for item in self._items:
                self.addItem(item)
        # self.item