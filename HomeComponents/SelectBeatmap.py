from Custom.CustomWidgets import CustomButtons
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import os


class SelectBeatmap(CustomButtons):
    def __init__(self, parent):
        super(SelectBeatmap, self).__init__(parent)
        self.main_window = parent
        self.file_extension = "folder"
        self.img_idle = "images/SelectMapIdle.png"
        self.img_hover = "images/SelectMapHover.png"
        self.img_clicked = "images/SelectMapClicked.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.pixmap_hover = QPixmap(os.path.join(self.main_window.app_directory, self.img_hover))
        self.pixmap_clicked = QPixmap(os.path.join(self.main_window.app_directory, self.img_clicked))
        self.layout = self.main_window.button_vertical_layout

        self.setAlignment(QtCore.Qt.AlignRight)
        super().setup()
