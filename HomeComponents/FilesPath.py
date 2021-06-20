from Custom.CustomWidgets import CustomLabel
from PyQt5 import QtCore

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.pixmap_idle = "images/MapPathIdle.png"
        self.pixmap_hover = "images/MapPathIdle.png"
        self.pixmap_clicked = "images/MapPathIdle.png"
        self.default_scale = [273, 27]
        self.default_coordinates = [544, 210]
        super().setup()


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.pixmap_idle = "images/OsrPathIdle.png"
        self.pixmap_hover = "images/OsrPathIdle.png"
        self.pixmap_clicked = "images/OsrPathIdle.png"
        self.default_scale = [273, 27]
        self.default_coordinates = [544, 175]
        super().setup()