from PyQt5.QtWidgets import QTableWidget, QAbstractItemView,QApplication
from PyQt5.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt5 import QtGui

from config.Static import Static
from config.Style import Style
from config.Font import Font

class CustomTable(QTableWidget):
    def __init__(self, num_rows, num_cols, parent=None):
        super().__init__(num_rows, num_cols, parent)

        self.static = Static()
        self._style_ = Style()
        self._font_ = Font()

        self.init_ui()

    def init_ui(self):

        # Set default properties
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)

        self.horizontalHeader().setStyleSheet(self._style_.get("thead"))
        self.setStyleSheet(self._style_.get("tbody"))

        self.horizontalHeader().setFont(self._font_.setFont(size=10, weight=700))
        self.setFont(self._font_.setFont(size=10))

        # set row height
        self.verticalHeader().setDefaultSectionSize(30)
        
        # Deselect row header when a row is selected
        selection_model = self.selectionModel()
        selection_model.select(QItemSelection(), QItemSelectionModel.Deselect)

    def on_selection_changed(self, selected, deselected):
        # Get the first selected row index
        index = selected.indexes()[0]
        if index.row() >= 0:
            # Deselect all sections in the row header
            self.verticalHeader().setSectionsSelected(Qt.NoSection | Qt.All, False)
            # Select the section corresponding to the selected row
            self.verticalHeader().setSectionSelected(index.column(), True)