from PyQt5.QtWidgets import QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph import PlotWidget, PlotItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from components.ComboBox import ComboBox

class ChartProducts(QWidget):
    def __init__(self, db, chart_type):
        super().__init__()

        self._chart_type_ = chart_type

        if chart_type == "line":
            self.collection = db['Transactions']
            self.init_line_chart_ui()
        elif chart_type == "pie":
            self.collection = db['Products']
            self.init_pie_chart_ui()

        
    def init_line_chart_ui(self):
        layout = QVBoxLayout()

        self.combo_box = ComboBox(items=["Days", "Weeks", "Months", "Years"],current_index=1)
        self.combo_box.setCurrentIndex(1)
        self.combo_box.currentIndexChanged.connect(self.update_chart)
        self.combo_box.setFixedHeight(33)
        self.combo_box.setFixedWidth(100)

        layout.addWidget(self.combo_box)
        
        self.chart_widget = PlotWidget(background="#ffffff")
        layout.addWidget(self.chart_widget)

        self.setLayout(layout)
        
        self.update_chart()
    
    def init_pie_chart_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 20px;
            padding: 20px;
        """)

        # Convert string prices to floats during aggregation
        total_wholesale_price = self.collection.aggregate([{
            "$group": {
                "_id": None,
                "total_wholesale": {"$sum": {"$toDouble": "$wholesale_price"}}
            }
        }])
        total_selling_price = self.collection.aggregate([{
            "$group": {
                "_id": None,
                "total_selling": {"$sum": {"$toDouble": "$selling_price"}}
            }
        }])

        # Get results as lists
        total_wholesale = list(total_wholesale_price)
        total_selling = list(total_selling_price)

        # Handle cases where no results are found
        if not total_wholesale or not total_selling:
            print("No data found for the pie chart")
            return

        total_wholesale = total_wholesale[0]['total_wholesale']
        total_selling = total_selling[0]['total_selling']
        profit_margin = total_selling - total_wholesale

        # Check for zero values to avoid NaN issues in the pie chart
        if total_wholesale == 0 and total_selling == 0 and profit_margin == 0:
            print("No meaningful data to display in the pie chart")
            return

        labels = ['Wholesale Price', 'Selling Price', 'Profit Margin']
        sizes = [total_wholesale, total_selling, profit_margin]
        colors = ['#e9223f', '#42105c', '#9681FA']

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            wedgeprops={'edgecolor': '#ffffff'}
        )
        ax.axis('equal')
        ax.set_title('Product Pricing Breakdown', color='#42105c')

        # Set the color of the pie chart text (labels and percentages)
        for text in texts:
            text.set_color('#585858')
        for autotext in autotexts:
            autotext.set_color('#ffffff')

        # Embed the pie chart into the widget
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        self.setLayout(layout)
        canvas.draw()

    def update_chart(self):
        period = self.combo_box.currentText().lower()
        self.chart_widget.clear()
        
        if period == 'days' or period == "":
            self.plot_sales_chart(group_by='day', x_label='Days')
        elif period == 'weeks':
            self.plot_sales_chart(group_by='week', x_label='Weeks')
        elif period == 'months':
            self.plot_sales_chart(group_by='month', x_label='Months')
        elif period == 'years':
            self.plot_sales_chart(group_by='year', x_label='Years')
    
    def plot_sales_chart(self, group_by, x_label):
        first_transaction = self.collection.find_one({"transactions_type": "OUT"}, sort=[("transactions_date", 1)])
        last_transaction = self.collection.find_one({"transactions_type": "OUT"}, sort=[("transactions_date", -1)])
        
        if not first_transaction or not last_transaction:
            return
        
        start_date = first_transaction['transactions_date']
        end_date = last_transaction['transactions_date']

        if group_by == 'day':
            date_format = "%Y-%m-%d"
        elif group_by == 'week':
            date_format = "%Y-%U"
        elif group_by == 'month':
            date_format = "%Y-%m"
        elif group_by == 'year':
            date_format = "%Y"
        
        pipeline = [
            {
                "$match": {
                    "transactions_type": "OUT",
                    "transactions_date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$addFields": {
                    "transactions_date_obj": {
                        "$dateFromString": {
                            "dateString": "$transactions_date",
                            "format": "%Y-%m-%d"
                        }
                    },
                    "quantity_int": {"$toInt": "$quantity"}  # Convert quantity to integer
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": date_format, "date": "$transactions_date_obj"}},
                    "total_sales": {"$sum": "$quantity_int"}  # Sum the converted integer quantities
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        dates = [r['_id'] for r in results]
        sales = [r['total_sales'] for r in results]

        plot_item: PlotItem = self.chart_widget.getPlotItem()
        plot_item.getAxis('left').setPen(pg.mkPen('#585858'))
        plot_item.getAxis('bottom').setPen(pg.mkPen('#585858'))
        plot_item.getAxis('left').setTextPen(pg.mkPen('#585858'))
        plot_item.getAxis('bottom').setTextPen(pg.mkPen('#585858'))

        plot_item.getAxis('left').setStyle(tickTextOffset=10)
        plot_item.getAxis('bottom').setStyle(tickTextOffset=10)

        plot_item.getViewBox().setBackgroundColor('#ffffff')

        self.chart_widget.plot(list(range(len(dates))), sales, pen=pg.mkPen('#B774FE', width=3))

        plot_item.getAxis('bottom').setTicks([list(enumerate(dates))])
        plot_item.setLabel('left', 'Number of Sales', color='#585858')
        plot_item.setLabel('bottom', x_label, color='#585858')

        plot_item.setTitle('Sales Over Time', color='#42105c', size='14pt')
        plot_item.setContentsMargins(20, 20, 20, 20)

    def plot_pie_chart(self):
        layout = self.layout()
        
        # Create pie chart for total wholesale price, total selling price, and profit margin
        total_wholesale_price = self.collection.aggregate([{"$group": {"_id": None, "total_wholesale": {"$sum": "$wholesale_price"}}}])
        total_selling_price = self.collection.aggregate([{"$group": {"_id": None, "total_selling": {"$sum": "$selling_price"}}}])
        
        total_wholesale = list(total_wholesale_price)[0]['total_wholesale']
        total_selling = list(total_selling_price)[0]['total_selling']
        profit_margin = total_selling - total_wholesale
        
        labels = ['Wholesale Price', 'Selling Price', 'Profit Margin']
        sizes = [total_wholesale, total_selling, profit_margin]
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        ax.set_title('Product Pricing Breakdown')
        
        # Embed the pie chart into the widget
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Ensure the canvas is displayed properly
        canvas.draw()