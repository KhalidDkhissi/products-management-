from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import QSettings, Qt 

from components.Button import Button
from controllers.components.GridController import GridController

from config.Font import Font

class Grid(QWidget):
    def __init__(self, parent, table_name, is_tab=False, state=True, is_export=False):
        super().__init__()

        self._state_ = state

        self._is_tab_ = is_tab

        self._is_export_ = is_export

        self.table_name = table_name

        self._font_ = Font()

        self._controller_ =  GridController(parent=parent, this=self, table_name=table_name)

        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0,0,0,0)
        
        self.setLayout(layout_main)


        ctn_actions = self.actions()

        if self._state_:
            title = QLabel(self.table_name.capitalize())
            title.setFont(self._font_.setFont(16, 700))
            title.setContentsMargins(0, 0, 0, 0)
            
            # ctn_border = QWidget()
            # ctn_border.setStyleSheet("background: #93abc5;")
            # ctn_border.setFixedHeight(1)

            layout_main.addWidget(title)
            layout_main.addWidget(ctn_actions)
            # layout_main.addWidget(ctn_border)
        else:
            layout_main.addWidget(ctn_actions)
            
        if self._is_tab_ == False:
            self._controller_.render_tables()

    def render_tables_tab(self):
        self._controller_.render_tables_tab()

    def actions(self):
        ctn_actions = QWidget()

        layout_actions = QHBoxLayout()

        if self._state_:
            layout_actions.setContentsMargins(0, 20, 0, 20)

        layout_actions.setSpacing(10)

        ctn_btns = QWidget()
        
        lyt_ctn_btns = QHBoxLayout()
        lyt_ctn_btns.setContentsMargins(0,0,0,0)

        box = QWidget()
        
        btn_add_new = Button(name='Add new', style='primary')
        btn_add_new.clicked.connect(self.create_new)
        
        btn_delete_all = Button(name='Delete all', style='error')
        btn_delete_all.clicked.connect(self.delete_all)


        if self._is_export_ == True:
            btn_export = Button(name='Export Excel', style='success')
            btn_export.clicked.connect(self.export_to_excel)
            lyt_ctn_btns.addWidget(btn_export)

        # lyt_ctn_btns.addWidget(box)
        lyt_ctn_btns.addWidget(btn_add_new)
        lyt_ctn_btns.addWidget(btn_delete_all)
        # lyt_ctn_btns.setStretch(0, 2)



        ctn_btns.setLayout(lyt_ctn_btns)

        ctn_search = QWidget()
        
        lyt_ctn_search = QHBoxLayout()
        lyt_ctn_search.setContentsMargins(0,0,0,0)

        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedHeight(33)
        self.search_bar.setPlaceholderText(f"Search {self.table_name}...")
        self.search_bar.textChanged.connect(self.filter_table)

        lyt_ctn_search.addWidget(self.search_bar)

        ctn_search.setLayout(lyt_ctn_search)

        layout_actions.addWidget(ctn_search)
        layout_actions.addWidget(ctn_btns)
        layout_actions.setStretch(0, 2)

        ctn_actions.setLayout(layout_actions)

        return ctn_actions

        
    def filter_table(self):
        self._controller_.filter_table()

    def export_to_excel(self):
        self._controller_.export_to_excel()

    def create_new(self):
        self._controller_.create_new()
    
    def delete_all(self):
        self._controller_.delete_all()