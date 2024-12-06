from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QSettings, Qt

from config.Style import Style
from config.Font import Font
from views.dashboard.components.Box import Box
from charts.ChartProducts import ChartProducts
from controllers.views.DashboardController import DashboardController

class Dashboard(QWidget):
    def __init__(self, db):
        super().__init__()

        self._db_ = db

        self._data_ = {}

        self._controller_ = DashboardController(this=self, db=db)

        self._style_ = Style()

        self._font_ = Font()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,10,0,0)
        
        title = QLabel("Dashboard")
        title.setFont(self._font_.setFont(16, 700))

        tbar = QWidget()
        tbar.setStyleSheet("background: transparent")
        
        layout_tbar = QHBoxLayout()
        layout_tbar.setSpacing(20)

        for key,val in self._data_.items():
            widget = Box(key, int(val))
            layout_tbar.addWidget(widget)

        tbar.setLayout(layout_tbar)

        main = QWidget()
        main.setStyleSheet("background: transparent;")
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0,0,0,0)

        ctn_products = QWidget()
        ctn_products.setStyleSheet("background: transparent;")
        
        layout_products = QHBoxLayout()
        layout_products.setContentsMargins(0,0,0,0)

        plot_sales_chart = ChartProducts(self._db_, "line")
        # plot_sales_chart.setStyleSheet("background: blue;")

        plot_pie_chart = ChartProducts(self._db_, "pie")
        # plot_pie_chart.setStyleSheet("background: red;")

        layout_products.addWidget(plot_sales_chart)
        layout_products.addWidget(plot_pie_chart)
        layout_products.setStretch(0, 7)
        layout_products.setStretch(1, 6)
        layout_products.setSpacing(20)

        ctn_products.setLayout(layout_products)

        layout_main.addWidget(ctn_products)

        main.setLayout(layout_main)

        layout.addWidget(title)
        layout.addWidget(tbar)
        layout.addWidget(main)

        self.setLayout(layout)