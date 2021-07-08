from Custom.CustomWidgets import DefaultLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import os

class Osr2mp4Logo(DefaultLabel):
    def __init__(self, parent):
        super(Osr2mp4Logo, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/osr2mp4_logo.png"
        self.img_hover = None
        self.layout = self.main_window.logo_horizontal
        self.setAlignment(QtCore.Qt.AlignBottom)
        self.text = None
        super().setup()

