from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from db.collections.UsersCollection import UsersCollection
from window.Alert import Alert


class WindDelUsersController:
    def __init__(self, this, parent):
        self.this = this

        self._parent_ = parent

        self._collection_ = UsersCollection(self.this._db_)

        self._items_ = {
            "All": 0
        }

    def set_items(self):
        combobox = self.this.user_name

        items = self._collection_.read_all()
        
        combobox._items.append("All")
        
        for item in items:
            user_name = item["full_name"]
            combobox._items.append(user_name)
            self._items_[user_name] = item["_id"]

        combobox.set_items()

        print("items: ", self._items_)

    def delete_users(self):
        combobox = self.this.user_name
        value = combobox.currentText()

        alert = Alert("confirmation", f"Are you sure you want to delete {value}?")
        
        if alert.result() == QMessageBox.Yes:

            tab_widget = self._parent_.tabs_table

            if value.lower() == "all":
                result = self._collection_.delete_all()

                if result:
                    Alert("success", "All users have been successfully deleted")

                    while tab_widget.count() > 0:
                        widget = tab_widget.widget(0)
                        tab_widget.removeTab(0)
                        widget.deleteLater()

                    self.this.close()
            else:
                result = self._collection_.delete_one({"_id": self._items_[value]})
                
                if result:
                    Alert("success", f"User <b>{value}</b> has been successfully deleted")
                    for i in range(tab_widget.count()):
                        if tab_widget.tabText(i) == value:
                            widget = tab_widget.widget(i)
                            tab_widget.removeTab(i)
                            widget.deleteLater()
                            break
                    
                    self.this.close()
        