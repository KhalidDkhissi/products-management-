from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit, QTableWidgetItem, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt

from db.collections.ProductsCollection import ProductsCollection
from db.collections.OrdersCollection import OrdersCollection
from components.CustomTable import CustomTable
from components.GroupFields import GroupFields
from components.ComboBox import ComboBox
from components.Field import Field
from components.Button import Button
from window.Alert import Alert

import functools
import time


class WindOrdersController:
    def __init__(self, this):
        self.this = this

        self.form_values = {}
        self.all_products = []
        self.products_selected = []

        self._collection_ = OrdersCollection(self.this._db_)
        self.collection_products = ProductsCollection(self.this._db_)

        self.init_model()

    def init_model(self):  
        self.all_products = self.collection_products.read_all()

    def create_order(self):
        data_order = {}

        data_customer = self.get_data(self.this.customer_fields, self.this.form_customer)
        data_discount = self.get_data(self.this.discount_fields, self.this.form_discount)
        data_products = self.get_data_table(self.this.table_products, self.this.data_table_products)
        data_total = self.get_data_table(self.this.table_total, self.this.data_table_total)
        data_note = self.get_data(self.this.field_note, self.this.form_note)
        
        if data_total and data_customer and data_discount and data_products:
            data_order.update(data_customer)
            data_order.update(data_discount)
            data_order.update(data_total[0])
            data_order.update(data_note)
            data_order["products"] = data_products

            print("data_order:", data_order)

            if self._collection_.create_order(data_order):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to create order of <b>{data_order['first_name']} {data_order['last_name']}</b>")
            else:
                Alert("error", f"Faild to create order of <b>{data_order['first_name']} {data_order['last_name']}</b>, try again")
        else:
            Alert("error", f"Please fill all fields when create an order and try again")

    def update_order(self, query):
        data_order = {}

        data_customer = self.get_data(self.this.customer_fields, self.this.form_customer)
        data_discount = self.get_data(self.this.discount_fields, self.this.form_discount)
        data_products = self.get_data_table(self.this.table_products, self.this.data_table_products)
        data_total = self.get_data_table(self.this.table_total, self.this.data_table_total)
        data_note = self.get_data(self.this.field_note, self.this.form_note)
        

        if data_total and data_customer and data_discount and data_products:
            data_order.update(data_customer)
            data_order.update(data_discount)
            data_order.update(data_total[0])
            data_order.update(data_note)
            data_order["products"] = data_products

            if self._collection_.update_order(query, data_order):
                self.this.state = True
                self.this.close()
                Alert("success", f"Success to update order of <b>{query['_id']}</b>")
                
        else:
            Alert("error", f"Please fill all fields when create an order and try again")

    def set_data(self, data):
        group_widgets = [self.this.customer_fields, self.this.discount_fields, self.this.field_note]
        forms_layout = [self.this.form_customer, self.this.form_discount, self.this.form_note]
        
        
        for idx in range(len(group_widgets)):
            self.binding_data_to_form(data, group_widgets[idx], forms_layout[idx])

        self.this.table_products.clearContents()
        
        rows = len(data["products"])

        for idx in range(rows):
            self.render_table_products(data["products"][idx], idx,"edit")
            print("\products= ", data["products"][idx])

        self.calc_total()
        
    def binding_data_to_form(self, data, group_widgets, form_layout):        
        for group in group_widgets:
            for field in group:
                field_name = field["name"]
                grp_widget = next((grp_widget for grp_widget in [form_layout.itemAt(i).widget() for i in range(form_layout.count())] if isinstance(grp_widget, GroupFields) and any(f["name"] == field_name for f in grp_widget._fields_)), None)
                if grp_widget:
                    field_widget = self.find_field_widget(grp_widget, field_name)
                    if field_widget:
                        if field_widget.type == "line":
                            field_widget.findChild(QLineEdit).setText(str(data[field_name].replace("%", "").replace("$", "")))
                        elif field_widget.type == "date":
                            field_widget.findChild(QDateEdit).setDate(QDate.fromString(str(data[field_name]), "yyyy-MM-dd"))
                        elif field_widget.type == "combobox":
                            index = field_widget.findChild(ComboBox).findText(str(data[field_name]))
                            if index != -1:
                                field_widget.findChild(ComboBox).setCurrentIndex(index)
    
    def set_combo_items(self):
        self.set_items(self.this.category_name, ProductsCollection(self.this._db_), "product_name")
    
    def set_items(self, combobox, collection, col_name):
        items = collection.read_all()

        for item in items:
            combobox._items.append(item[col_name])

        combobox.set_items()
        
    def render_table(self, table):
        thead = table["thead"]
        size_cols = table["size"]

        cols = len(thead)
        rows = 0

        table_widget = CustomTable(rows, cols)
        table_widget.setHorizontalHeaderLabels(thead)
        
        width = self.this.width()

        for col in range(cols):
            wid_col = int(size_cols[col] * width)
            table_widget.setColumnWidth(col, wid_col)
        
        return table_widget

    def get_data(self, group_widgets, form_layout):

        data = {}
        
        for group in group_widgets:
            for field in group:
                field_name = field["name"]
                grp_widget = next((grp_widget for grp_widget in [form_layout.itemAt(i).widget() for i in range(form_layout.count())] if isinstance(grp_widget, GroupFields) and any(f["name"] == field_name for f in grp_widget._fields_)), None)
                if grp_widget:
                    field_widget = self.find_field_widget(grp_widget, field_name)
                    if field_widget:
                        if field_widget.type == "line":
                            val = field_widget.findChild(QLineEdit).text()
                            
                            if (val != "") and (val is not None) and (field["is_digit"] == True):
                                val = float(val)
                                data[field_name] = format(val, ".2f")
                            else:
                                data[field_name] = val

                        elif field_widget.type == "date":
                            data[field_name] = field_widget.findChild(QDateEdit).date().toString("yyyy-MM-dd")

                        elif field_widget.type == "combobox":
                            data[field_name] = field_widget.findChild(ComboBox).currentText()

        return data

    def find_field_widget(self, parent, field_name):
        for child in parent.children():
            if isinstance(child, Field) and child.field_name == field_name:
                return child
            elif child.children():
                field_widget = self.find_field_widget(child, field_name)
                if field_widget:
                    return field_widget
        return None
    
    def get_data_table(self, table, data_table):
        data_thead = data_table["thead"].copy()

        if 'Actions' in data_thead:
            data_thead.remove('Actions')

        data = []

        for row in range(table.rowCount()):
            row_data = {}
            for col in range(len(data_thead)):
                item = table.item(row, col)
                
                if data_thead[col].lower() == "quantity":
                    field = table.cellWidget(row, col)
                    
                    if field:  # If there is a widget, get its value
                        if isinstance(field, QLineEdit):
                            row_data['quantity'] = field.text()
                    else:
                        if item is not None:
                            row_data['quantity'] = item.text()
                else:
                    if item is not None:
                        row_data[data_thead[col].lower().replace(" ", "_")] = item.text()

            data.append(row_data)

        return data
    
    def search_product(self):
        self.this.results_list.clear()
        self.this.msg_label_search.clear()

        query = self.this.search_field.text().strip().lower()

        matching_products = [product["product_name"] for product in self.all_products if query in product["product_name"].strip().lower()]

        if matching_products:
            self.this.results_list.addItems(matching_products)
        else:
            self.this.msg_label_search.setText("This product does not exist")

    def select_item_search(self):
        select_product = {}

        current_item = self.this.results_list.currentItem()
        
        item_search = current_item.text()

        self.this.search_field.setText(item_search.strip().capitalize())

        self.insert_product(item_search)
            
        self.this.results_list.clear()

    def insert_product(self, item_search):
        for product in self.all_products:
            if item_search.lower() in product["product_name"].lower():
                select_product = {
                    "product_name": product["product_name"], 
                    "price": product["selling_price"],
                    "quantity": "1",
                    "total": product["selling_price"]
                }
        
        if not select_product:
            return  # If no product is found, exit

        self.products_selected.append(select_product)

        rows = self.this.table_products.rowCount()
        
        self.render_table_products(select_product, rows)

        self.calc_total()

    def render_table_products(self, select_product, row, state="new"):
        thead = self.this.data_table_products["thead"]
        
        if state == "edit" and row < self.this.table_products.rowCount():
            self.this.table_products.setRowHeight(row, 30)
        else:
            self.this.table_products.insertRow(row)
            self.this.table_products.setRowHeight(row, 30)
    
        cols = len(thead)
        
        for col in range(cols):
            th = thead[col].lower().replace(" ", "_")

            if "quantity" == th:
                value = select_product[th] if state == "edit" and th in select_product else "1"
                quantity_field = QLineEdit()
                quantity_field.setObjectName(th)
                quantity_field.setText(value)
                quantity_field.textChanged.connect(functools.partial(self.handle_quantity, quantity_field, select_product["price"], row))

                self.this.table_products.setCellWidget(row, col, quantity_field)

            elif "actions" == th:
                hbox = QHBoxLayout()
                hbox.setContentsMargins(0,0,0,0)

                btn_delete = Button(size="icon", style="error", icon_path="actions/trash.png")
                btn_delete.clicked.connect(functools.partial(lambda: self.delete_row(row)))
                
                hbox.addWidget(btn_delete)
                
                ctn_actions = QWidget()
                ctn_actions.setLayout(hbox)

                self.this.table_products.setCellWidget(row, col, ctn_actions)

            else:
                if th in select_product:
                    self.this.table_products.setItem(row, col, QTableWidgetItem(select_product[th]))

        self.this.table_products.resizeRowsToContents()

    def handle_quantity(self, quantity, price, row):
        cell_total = 3
        txt = quantity.text()

        val_quatity = float(txt) if txt is not None and txt != "" else "1"

        total = float(val_quatity) * float(price)

        self.this.table_products.setItem(row, cell_total, QTableWidgetItem(format(total, ".2f")))

        self.calc_total()

    def delete_row(self, row):
        if self.this.table_products.rowCount() == 1:
            self.this.table_total.removeRow(0)
            row = 0

        self.this.table_products.removeRow(row)

        if row <= len(self.products_selected):
            self.products_selected.pop(row)
        
    def update_table(self):
        cols = self.this.table_products.rowCount()
        rows = self.this.table_products.rowCount()

        # remove all rows
        for row in reversed(range(cols)):
            self.this.table_products.removeRow(row)
        
        time.sleep(1)

        rows = rows - 1

        # add new rows
        for row in range(rows):
            self.table_widget.insertRow(row)

        for product in self.products_selected:
            self.render_table_products(product, rows)

    def add_event(self, group_widgets, form_layout):
        for group in group_widgets:
            for field in group:
                field_name = field["name"]
                grp_widget = next((grp_widget for grp_widget in [form_layout.itemAt(i).widget() for i in range(form_layout.count())] if isinstance(grp_widget, GroupFields) and any(f["name"] == field_name for f in grp_widget._fields_)), None)
                if grp_widget:
                    field_widget = self.find_field_widget(grp_widget, field_name)
                    if field_widget and (field["is_event"] == True):
                        if field_widget.type == "line":
                            field = field_widget.findChild(QLineEdit)
                            field.textChanged.connect(self.calc_total)
                        elif field_widget.type == "combobox":
                            field = field_widget.findChild(ComboBox)
                            field.currentIndexChanged.connect(self.calc_total)

    def redirect_fun(self, field, callback):
        if callback == "discount":
            self.handle_discount(field)
        elif callback == "discount_type":
            self.handle_discount_type(field)

    def handle_discount(self, field):
        self.calc_total()

    def handle_discount_type(self, field):
        self.calc_total()

    def calc_total(self):
        self.this.table_total.removeRow(0)

        data_total = {}
        
        vat_rate = 15.00 # Set VAT (assuming VAT rate is 15%)
        
        shipping_fee = 10.00  # You can make this dynamic based on conditions
        data_total["shipping_fee"] = f"{shipping_fee}$"

        data_discount = self.get_data(self.this.discount_fields, self.this.form_discount)
        data_products = self.get_data_table(self.this.table_products, self.this.data_table_products)

        subtotal = 0.00
        
        for data in data_products:
            subtotal += float(data["total"])

        data_total["subtotal"] = f"{format(subtotal, '.2f')}$"
        
        discount_type = data_discount["discount_type"]

        discount = float(data_discount['discount']) if data_discount["discount"] else 0.00

        vat = subtotal * (vat_rate / 100)    
        data_total["vat"] = f"{format(vat, '.2f')}$"

        if discount_type == "Percentage":
            data_total["discount"] = f"{format(discount, '.2f')}%"
            discount = format(discount / 100, ".2f")
            total = subtotal + shipping_fee + vat - subtotal * float(discount)
        else:
            data_total["discount"] = f"{format(discount, '.2f')}$"
            total = subtotal + shipping_fee + vat - float(discount)

        data_total["total"] = f"{format(total, '.2f')}$"

        thead = self.this.data_table_total["thead"]
        cols = len(thead)
        rows = self.this.table_total.rowCount()
        self.this.table_total.insertRow(rows)
        self.this.table_total.setRowHeight(rows, 30)
        cols = len(thead)

        print("\ndata_total: ", data_total)

        for col in range(cols):
            th = thead[col].lower().replace(" ", "_")
            self.this.table_total.setItem(rows, col, QTableWidgetItem(str(data_total[th])))