from Custom.CustomWidgets import PopupLabels

from PyQt5.QtCore import Qt
from Custom.CustomQtFunctions import blur_widget

class PopupWindow(PopupLabels):
    def __init__(self, parent):
        super(PopupWindow, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/PopupWindow.png"
        self.setStyleSheet("background-color:transparent;")
        self.blur_home_widgets()
        self.clickable = False
        self.visible = True
        super().setup()

    def blur_home_widgets(self):
        blur_widget(self.main_window.home_widgets)

    def resize_(self):
        if self.visible:
            width, height = 75/100*self.main_window.width(), 75/100*self.main_window.height()
            self.setPixmap(self.pixmap_idle.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            x, y = self.main_window.width() / 2 - self.pixmap().width() / 2, self.main_window.height() / 2 - self.pixmap().height() / 2
            self.setGeometry(x, y, width, height)
            self.main_window.select_osu_folder.resize_(self.pixmap().width(), self.pixmap().height(), self.x(), self.y())
            self.main_window.select_output_folder.resize_(self.pixmap().width(), self.pixmap().height(), self.x(), self.y())
