from Custom.CustomWidgets import CustomButtons
from PyQt5 import QtCore

class SelectOsr(CustomButtons):
    def __init__(self, parent):
        super(SelectOsr, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/SelectOsrIdle.png"
        self.pixmap_hover = "images/SelectOsrHover.png"
        self.pixmap_clicked = "images/SelectOsrClicked.png"
        self.file_extension = ".osr"
        self.row = 1
        self.col = 3
        #self.setAlignment(QtCore.Qt.)
        super().setup()
