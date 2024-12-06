from PyQt5.QtWidgets import QTableWidgetItem, QHBoxLayout, QWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import QDate

from bson import ObjectId
import time
import functools
import pandas as pd
import openpyxl
import os


from components.Button import Button
from components.ComboBox import ComboBox
from db.collections.ProductsCollection import ProductsCollection
from db.collections.CategoriesCollection import CategoriesCollection
from db.collections.OrdersCollection import OrdersCollection
from db.collections.SuppliersCollection import SuppliersCollection
from db.collections.TasksCollection import TasksCollection
from db.collections.UsersCollection import UsersCollection
from db.collections.JobPostingsCollection import JobPostingsCollection
from db.collections.CandidatesCollection import CandidatesCollection
from db.collections.InterviewsCollection import InterviewsCollection
from db.collections.TransactionsCollection import TransactionsCollection
from window.WindProducts import WindProducts
from window.WindCategories import WindCategories
from window.WindSuppliers import WindSuppliers
from window.WindOrders import WindOrders
from window.WindTasks import WindTasks
from window.WindUsers import WindUsers
from window.WindCandidates import WindCandidates
from window.WindJobPostings import WindJobPostings
from window.WindInterviews import WindInterviews
from window.WindTransactions import WindTransactions
from components.CustomTable import CustomTable
from config.Invices import Invoices
from config.Static import Static
from window.Alert import Alert


class GridController:
    def __init__(self, parent, this, table_name):

        self._parent_ = parent
        self.this = this
        self.table_name = table_name
        
        self.table_widget = None

        if table_name == "products":
            self._collection_ = ProductsCollection(self._parent_._db_)
        elif table_name == "categories":
            self._collection_ = CategoriesCollection(self._parent_._db_)
        elif table_name == "suppliers":
            self._collection_ = SuppliersCollection(self._parent_._db_)
        elif table_name == "tasks":
            self._collection_ = TasksCollection(self._parent_._db_)
        elif table_name == "users":
            self._collection_ = UsersCollection(self._parent_._db_)
        elif table_name == "job postings":
            self._collection_ = JobPostingsCollection(self._parent_._db_)
        elif table_name == "candidates":
            self._collection_ = CandidatesCollection(self._parent_._db_)
        elif table_name == "interviews":
            self._collection_ = InterviewsCollection(self._parent_._db_)
        elif table_name == "transactions":
            self._collection_ = TransactionsCollection(self._parent_._db_)
        elif table_name == "orders":
            self._collection_ = OrdersCollection(self._parent_._db_)

        self._static_ = Static()

    def call_wind(self, action, data=None):
        if self.table_name == "products":
            self._wind_ = WindProducts(self._parent_._db_, data, action)
        elif self.table_name == "categories":
            self._wind_ = WindCategories(self._parent_._db_, data, action)
        elif self.table_name == "suppliers":
            self._wind_ = WindSuppliers(self._parent_._db_, data, action)
        elif self.table_name == "tasks":
            self._wind_ = WindTasks(self._parent_, self._parent_._db_, data, action)
        elif self.table_name == "users":
            self._wind_ = WindUsers(self._parent_._db_, data, action)
        elif self.table_name == "job postings":
            self._wind_ = WindJobPostings(self._parent_._db_, data, action)
        elif self.table_name == "candidates":
            self._wind_ = WindCandidates(self._parent_._db_, data, action)
        elif self.table_name == "interviews":
            self._wind_ = WindInterviews(self._parent_._db_, data, action)
        elif self.table_name == "transactions":
            self._wind_ = WindTransactions(self._parent_._db_, data, action)
        elif self.table_name == "orders":
            self._wind_ = WindOrders(self._parent_._db_, data, action)
            
        self._wind_.exec_()

    def render_tables(self):
        data_tbody = self._collection_ .read_all()

        self.create_table(data_tbody)
    
    def render_tables_tab(self):
        tabs_table = self._parent_.tabs_table
        current_tab_index = tabs_table.currentIndex()
        current_tab_name = tabs_table.tabText(current_tab_index)
        user_id = self._parent_.tabs_id[current_tab_name]

        data_tbody = self._collection_.find_many({"user_id": user_id})

        self.create_table(list(data_tbody))
    
    def create_table(self, data_tbody):
        thead_tables = self._static_.get("thead_tables")

        data_thead = thead_tables[self.table_name]["thead"]

        cols = len(data_thead)
        
        if not isinstance(data_tbody, list):
            rows = data_tbody.collection.count_documents({})
        else:
            rows = len(data_tbody)

        if self.table_widget is None:
            self.table_widget = CustomTable(rows, cols)
            self.table_widget.setHorizontalHeaderLabels(data_thead)
            
            width = self._parent_.width()

            size_cols = thead_tables[self.table_name]["size"]

            for col in range(cols):
                wid_col = int(size_cols[col] * width)
                self.table_widget.setColumnWidth(col, wid_col)
        
        for row in range(rows):
                self.table_widget.setRowHeight(row, 38)

                data_row = data_tbody[row]

                for col in range(cols):
                    col_name = data_thead[col].replace(" ", "_").lower()
                    if col + 1 < cols:
                        if self.table_name == "orders":
                            if col_name == "payment_status" or col_name == "shipping_status":
                                combobox = ComboBox(items=self._static_.get(col_name))
                                combobox.setObjectName(col_name)
                                combobox.currentIndexChanged.connect(functools.partial(self.handle_status, combobox, data_row))
                                combobox.setCurrentText(data_row[col_name])
                                self.table_widget.setCellWidget(row, col, combobox)
                            
                            elif col_name == "customer_name":
                                value = f"{data_row['first_name']} {data_row['last_name']}"
                                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))
                                print(f"value= {value}")
                            
                            else:
                                value = data_row[col_name]
                                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

                        else:
                            value = data_row[col_name]
                            self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

                    else:

                        hbox = QHBoxLayout()
                        hbox.setContentsMargins(0,0,0,0)

                        box = QWidget()

                        btn_edit = Button(size="icon", style="success", icon_path="actions/pincel.png")
                        btn_edit.clicked.connect(functools.partial(self.edit_row, data_row))

                        btn_delete = Button(size="icon", style="error", icon_path="actions/trash.png")
                        btn_delete.clicked.connect(functools.partial(self.delete_row, data_row["_id"], data_row[data_thead[0].replace(" ", "_").lower()]))


                        hbox.addWidget(box, 2)
                        hbox.addWidget(btn_edit)
                        hbox.addWidget(btn_delete)

                        if self.table_name == "orders":
                            btn_invoice = Button(size="icon", style="primary", icon_path="actions/invoice.png")
                            btn_invoice.clicked.connect(functools.partial(self.download_invoice, data_row["_id"]))
                            hbox.addWidget(btn_invoice)

                        hbox.addWidget(box, 2)

                        ctn = QWidget()
                        ctn.setLayout(hbox)

                        self.table_widget.setCellWidget(row, col, ctn)
        
        self.this.layout().addWidget(self.table_widget)

    def update_table(self, action_type):
        cols = self.table_widget.rowCount()
        rows = self.table_widget.rowCount()

        # remove all rows
        for row in reversed(range(cols)):
            self.table_widget.removeRow(row)
        
        time.sleep(1)

        if action_type == "new":
            rows += 1
        elif action_type == "delete_one":
            rows -= 1
        elif action_type == "delete_all":
            rows = 0

        # add new rows
        for row in range(rows):
            self.table_widget.insertRow(row)

        if self.this._is_tab_:
            self.render_tables_tab()
        else:
            self.render_tables()

    def create_new(self):
        self.call_wind("new")
        
        if self._wind_.state:
            self.update_table("new")
            self._wind_.state = False

    def edit_row(self, data_row):
        # print("data_row: ", data_row)
        self.call_wind("edit",data_row)

        if self._wind_.state:
            self.update_table("")
            self._wind_.state = True
    
    def delete_row(self, _id, col_name):
        alert = Alert("confirmation", f"Are you sure you want to delete this <b>{col_name}</b>?")
        
        if alert.result() == QMessageBox.Yes:
            result = self._collection_.delete_one({"_id": ObjectId(_id)})

            self.update_table("delete_one")

            if result:
                Alert("success", f"Successful to delete category <b>{col_name}</b>")

    def delete_all(self):
        alert = Alert("confirmation", f"Are you sure you want to delete all?")
        
        if alert.result() == QMessageBox.Yes:
            query = {}

            if self.this._is_tab_:
                tabs_table = self._parent_.tabs_table
                current_tab_index = tabs_table.currentIndex()
                current_tab_name = tabs_table.tabText(current_tab_index)
                user_id = self._parent_.tabs_id[current_tab_name]
                query["user_id"] = user_id

            result = self._collection_.delete_all(query)

            self.update_table("delete_all")

            if result:
                Alert("success", f"All has been successfully deleted")

    def filter_table(self):
        search_text = self.this.search_bar.text().lower()

        cell = 2 if self.table_name == "orders" else 0
        
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, cell)  # Filter by First Column of Table
            self.table_widget.setRowHidden(row, not (search_text in item.text().lower() if item else False))

    def export_to_excel(self):
        try:
            thead_tables = self._static_.get("thead_tables")
            data_thead = thead_tables[self.table_name]["thead"]

            if 'Actions' in data_thead:
                data_thead.remove('Actions')

            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                
                for col in range(len(data_thead)):
                    
                    item = self.table_widget.item(row, col)
                    
                    if item is not None:
                        row_data.append(item.text())
                    
                    else:
                        field = self.table_widget.cellWidget(row, col)
                    
                        if field: 
                            if isinstance(field, QLineEdit):
                                row_data.append(field.text())
                            
                            elif isinstance(field, ComboBox):
                                row_data.append(field.currentText())
                        else:
                            if item is not None:
                                row_data.append(item.text())

                data.append(row_data)
            
            print("\ndata_thead: ", data_thead)
            print("\ndata: ", data)

            df = pd.DataFrame(data, columns=data_thead)

            today = QDate.currentDate().toString("yyyy-MM-dd")
            
            downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
            
            file_name = f"{self.table_name.capitalize()}-{today}.xlsx"
            file_path = os.path.join(downloads_folder, file_name)

            df.to_excel(file_path, index=False)

            Alert('success', f'Download successful: {file_name}')

        except  Exception as e:
            print("error -> ", e)
            Alert("error", 'Failed to download file')

    def handle_status(self, combobox, query):
        current_text = combobox.currentText()
        field_name = combobox.objectName()
        old_text = query[field_name]

        if (old_text is not None) and (old_text != current_text):
            update_data = {
                field_name: current_text,
            }

            new_query = {
                "_id": query["_id"],
                field_name: query[field_name],
            }

            result = self._collection_.update_order(new_query, update_data)

            if result.matched_count > 0:
                Alert("success", f"Success to update {field_name.replace('_', ' ').capitalize()}")
            else:
                Alert("error", f"Failed to update {field_name.replace('_', ' ').capitalize()}")

    def download_invoice(self, _id):
        Invoices(self._parent_._db_, _id)