from Custom.CustomWidgets import CustomButtons
from PyQt5 import QtCore



class SelectBeatmap(CustomButtons):
    def __init__(self, parent):
        super(SelectBeatmap, self).__init__(parent)
        self.main_window = parent
        self.file_extension = "folder"
        self.img_idle = "images/SelectMapIdle.png"
        self.img_hover = "images/SelectMapHover.png"
        self.img_clicked = "images/SelectMapClicked.png"
        self.layout = self.main_window.button_vertical_layout

        self.setAlignment(QtCore.Qt.AlignRight)
        super().setup()
