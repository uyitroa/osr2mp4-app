from Custom.CustomWidgets import CustomLabel
from PyQt5.QtCore import Qt


class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/MapPathIdle.png"
        self.setAlignment(Qt.AlignBottom)
        super().setup()


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/OsrPathIdle.png"
        self.setAlignment(Qt.AlignRight)
        super().setup()