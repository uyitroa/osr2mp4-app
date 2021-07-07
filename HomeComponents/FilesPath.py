from Custom.CustomWidgets import CustomLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from Custom.CustomFunctions import get_latest_replay

import os

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/MapPathIdle.png"
        self.setGeometry(10, 10, 10, 10)
        self.layout = self.main_window.path_vertical_layout
        #map_path_text = get_latest_replay()
        self.text = QLabel(self)
        #self.text.setText(map_path_text)
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
        self.layout = self.main_window.path_vertical_layout
        self.text = QLabel(self)
        replay_path_text = get_latest_replay(self.main_window.current_config)
        self.text.setText(replay_path_text)
        self.text.setStyleSheet("background-color:transparent;color:white;")
        super().setup()

    def resize_text_path(self):
        self.text.move(0, self.height() - self.pixmap().height())
        self.text.resize(self.pixmap().width(), self.pixmap().height())


