from Custom.CustomWidgets import CustomButtons
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import os

class SelectOsr(CustomButtons):
    def __init__(self, parent):
        super(SelectOsr, self).__init__(parent)
        self.main_window = parent
        self.file_extension = ".osr"
        self.img_idle = "images/SelectOsrIdle.png"
        self.img_hover = "images/SelectOsrHover.png"
        self.img_clicked = "images/SelectOsrClicked.png"

        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.pixmap_hover = QPixmap(os.path.join(self.main_window.app_directory, self.img_hover))
        self.pixmap_clicked = QPixmap(os.path.join(self.main_window.app_directory, self.img_clicked))
        self.layout = self.main_window.button_vertical_layout

        self.setAlignment(QtCore.Qt.AlignRight)
        super().setup()
