from Custom.CustomWidgets import PopupLabels
from PyQt5.QtCore import Qt


class SelectOsuFolder(PopupLabels):
    def __init__(self, parent):
        super(SelectOsuFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OsuFolderIdle.png"
        self.setStyleSheet("background-color:transparent;")
        super().setup()

    def resize_(self):
        width, height = 38/100*self.main_window.width(), 12/100*self.main_window.height()
        print(width, height)
        print(self.main_window.width(), self.main_window.height())
        print(width/self.main_window.width()*100, height/self.main_window.height()*100)
        x, y = 48/100*self.main_window.width(), 68/100*self.main_window.height()
        self.setPixmap(self.pixmap_idle.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setGeometry(x, y, width, height)
