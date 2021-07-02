from Custom.CustomWidgets import PopupLabels
from PyQt5.QtCore import Qt


class SelectOutputFolder(PopupLabels):
    def __init__(self, parent):
        super(SelectOutputFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OutputFolderIdle.png"
        self.setStyleSheet("background-color:transparent;")
        super().setup()

    def resize_(self):
        width, height = 26 / 100 * self.main_window.width(), 10 / 100 * self.main_window.height()
        x, y = 25 / 100 * self.main_window.width(), 69 / 100 * self.main_window.height()
        self.setPixmap(self.pixmap_idle.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setGeometry(x, y, width, height)