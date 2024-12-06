from PyQt5.QtWidgets import QMessageBox

class Alert(QMessageBox):
    def __init__(self, alert_type, message, parent=None):
        super().__init__(parent)

        self.alert_type = alert_type
        self.message = message

        self.init_ui()

    def init_ui(self):
        if self.alert_type.lower() == 'success':
            icon = QMessageBox.Information
        elif self.alert_type.lower() == 'error':
            icon = QMessageBox.Critical
        elif self.alert_type.lower() == 'warning':
            icon = QMessageBox.Warning
        elif self.alert_type.lower() == 'confirmation':
            icon = QMessageBox.Question
            self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        else:
            self.alert_type = "Error"
            icon = QMessageBox.Warning

        self.setWindowTitle(self.alert_type)
        self.setText(self.message)
        self.setIcon(icon)

        # Set the default button to "OK"
        # self.setStandardButtons(QMessageBox.Ok)

        self.show_alert()


    def show_alert(self):
        self.exec_()