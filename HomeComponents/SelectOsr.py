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

        self.layout = self.main_window.button_vertical_layout

        self.setAlignment(QtCore.Qt.AlignRight)
        super().setup()
