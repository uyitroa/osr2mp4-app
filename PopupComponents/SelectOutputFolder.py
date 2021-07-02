from Custom.CustomWidgets import PopupLabels
from PyQt5.QtCore import Qt


class SelectOutputFolder(PopupLabels):
    def __init__(self, parent):
        super(SelectOutputFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OutputFolderIdle.png"
        self.img_hover = "images/OutputFolderHover.png"
        self.img_clicked = "images/OutputFolderClicked.png"
        self.setStyleSheet("background-color:transparent;")
        self.clickable = True
        super().setup()

    def resize_(self, popup_width, popup_height, popup_x, popup_y):
        width, height = 40/100*popup_width, 14/100*popup_height
        x, y = 11 / 100 * popup_width, 78 / 100 * popup_height

        self.setPixmap(self.pixmap_idle.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setGeometry(popup_x + x, popup_y + y, width, height)
