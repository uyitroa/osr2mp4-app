from Custom.CustomWidgets import PopupLabels
from PyQt5.QtCore import Qt


class SelectOsuFolder(PopupLabels):
    def __init__(self, parent):
        super(SelectOsuFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OsuFolderIdle.png"
        self.img_hover = "images/OsuFolderHover.png"
        self.img_clicked = "images/OsuFolderClicked.png"
        self.setStyleSheet("background-color:transparent;")
        self.clickable = True
        self.file_extension = "folder"
        self.file_name = "Osu Path"
        super().setup()

    def resize_(self, popup_width, popup_height, popup_x, popup_y):
        width, height = 60/100*popup_width, 17/100*popup_height
        x, y = 47/100*popup_width, 75/100*popup_height
        self.setPixmap(self.pixmap_idle.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setGeometry(popup_x + x, popup_y + y, width, height)
