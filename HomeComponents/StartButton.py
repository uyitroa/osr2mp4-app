from Custom.CustomWidgets import CustomLabel
from PyQt5.QtCore import QSize


class StartButton(CustomLabel):
    def __init__(self, parent):
        super(StartButton, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/StartIdle.png"
        self.layout = self.main_window.start_layout_button
        #self.setMinimumSize(QSize(200, 200))

        self.text = None
        super().setup()