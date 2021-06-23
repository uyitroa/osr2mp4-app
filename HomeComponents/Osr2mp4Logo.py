from Custom.CustomWidgets import CustomLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import os

class Osr2mp4Logo(CustomLabel):
    def __init__(self, parent):
        super(Osr2mp4Logo, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/osr2mp4_logo.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.layout = self.main_window.logo_horizontal
        self.setAlignment(QtCore.Qt.AlignBottom)
        super().setup()

