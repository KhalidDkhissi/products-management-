from PyQt5.QtWidgets import QLabel, QProgressBar, QDialog, QVBoxLayout, QApplication, QWidget
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QIcon, QPixmap
import os

from config.Static import Static
from config.Style import Style
from config.Font import Font

class Loader(QDialog):
    def __init__(self):
        super().__init__()

        self._static_ = Static()
        self._style_ = Style()
        self._font_ = Font()
    
        self.init_ui()

    def init_ui(self):
        width_wind = 500
        print("runing........")

        self.setFixedWidth(width_wind)

        path = os.getcwd()
        path_imgs = os.path.join(path, "src/images")
        path_icon_wind = os.path.join(path_imgs, "icon.png")
        path_img_bg = os.path.join(path_imgs,"template/bg-loading.png")

        self.setWindowIcon(QIcon(path_icon_wind))
        self.setWindowTitle(self._static_.get("app_name"))

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        layout_cnt = QVBoxLayout()
        layout_cnt.setContentsMargins(10, 20, 10, 20)
        layout_cnt.setSpacing(10)

        container = QWidget()
        container.setLayout(layout_cnt)

        self.label_wait = QLabel("Wait to load App...")
        self.label_wait.setFont(self._font_.setFont(size=8))
        self.label_wait.setStyleSheet(self._style_.get("label_file_name"))
        
        self.label_scoor = QLabel("0%")
        self.label_scoor.setFont(self._font_.setFont(size=9))
        self.label_scoor.setStyleSheet(self._style_.get("label_scoor"))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(self._style_.get("progress_bar"))
        
        bg = QLabel()
        bg.setPixmap(QPixmap(path_img_bg).scaled(self.width(), 77))

        layout_cnt.addWidget(self.label_wait, alignment=Qt.AlignCenter)
        layout_cnt.addWidget(self.label_scoor, alignment=Qt.AlignCenter)
        layout_cnt.addWidget(self.progress_bar)

        layout.addWidget(container)
        layout.addWidget(bg)

        self.setLayout(layout)

        self.open()

        QApplication.processEvents()
        QThread.msleep(200)

        for i in range(1, 101):
            self.label_scoor.setText(f"{i}%")
            self.progress_bar.setValue(i)

            QApplication.processEvents()
            QThread.msleep(50)

        return True