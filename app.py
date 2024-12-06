from PyQt5.QtWidgets import QApplication
import sys

from layout.Main import MainWindow
from db.DBConnect import DBConnection
from window.Loader import Loader
from window.Alert import Alert

def app():
    app = QApplication(sys.argv)
    
    db_connection = DBConnection()
    # loader = Loader()
    db_connection.connect()

    if db_connection.client:
        # loader.close()

        win = MainWindow(db_connection.db)
        win.showMaximized()

        sys.exit(app.exec_())

    

if __name__ == "__main__":
    app()