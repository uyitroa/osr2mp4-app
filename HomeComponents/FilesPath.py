from Custom.CustomWidgets import CustomLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import os

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/MapPathIdle.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.setGeometry(10, 10, 10, 10)
        self.layout = self.main_window.path_vertical_layout
        self.text = QLabel(self)
        self.text.setText("motherfuckerrrr")
        self.text.setStyleSheet("background-color:transparent;color:white;")
        super().setup()

    def resize_text_path(self):
        self.text.move(0, self.height() - self.pixmap().height())
        self.text.resize(self.pixmap().width(), self.pixmap().height())


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.main_window = parent
        self.text = None
        self.img_idle = "images/OsrPathIdle.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.layout = self.main_window.path_vertical_layout
        self.text = QLabel(self)
        self.text.setText("motherfuckerrrr")
        self.text.setStyleSheet("background-color:transparent;color:white;")
        super().setup()

    def resize_text_path(self):
        self.text.move(0, 0)
        self.text.resize(self.pixmap().width(), self.pixmap().height())

