from Custom.CustomWidgets import CustomLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import os

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/MapPathIdle.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.layout = self.main_window.path_vertical_layout
        self.setAlignment(QtCore.Qt.AlignBottom)
        super().setup()


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OsrPathIdle.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.layout = self.main_window.path_vertical_layout
        self.setAlignment(QtCore.Qt.AlignRight)
        super().setup()