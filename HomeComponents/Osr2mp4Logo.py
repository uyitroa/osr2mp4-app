from Custom.CustomWidgets import CustomLabel
from PyQt5.QtWidgets import QGraphicsBlurEffect

class Osr2mp4Logo(CustomLabel):
    def __init__(self, parent):
        super(Osr2mp4Logo, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/osr2mp4_logo.png"
        self.row = 0
        self.col = 0
        super().setup()

