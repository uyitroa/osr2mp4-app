from Custom.CustomWidgets import CustomButtons
from PyQt5.QtCore import Qt

class SelectOsr(CustomButtons):
    def __init__(self, parent):
        super(SelectOsr, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/SelectOsrIdle.png"
        self.pixmap_hover = "images/SelectOsrHover.png"
        self.pixmap_clicked = "images/SelectOsrClicked.png"
        self.file_extension = ".osr"
        self.setAlignment(Qt.AlignRight)
        super().setup()
