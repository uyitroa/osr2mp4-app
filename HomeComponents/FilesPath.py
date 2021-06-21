from Custom.CustomWidgets import CustomButtons, CustomLabel
from PyQt5 import QtCore

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/MapPathIdle.png"
        self.default_scale = [273, 27]
        self.default_coordinates = [544, 210]
        self.row = 3
        self.col = 3
        super().setup()


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.main_window = parent

        self.pixmap_idle = "images/OsrPathIdle.png"
        self.default_scale = [273, 27]
        self.default_coordinates = [544, 170]
        self.row = 4
        self.col = 3
        super().setup()