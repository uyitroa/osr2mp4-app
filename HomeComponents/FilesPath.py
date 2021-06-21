from Custom.CustomWidgets import CustomLabel

class MapPath(CustomLabel):
    def __init__(self, parent):
        super(MapPath, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/MapPathIdle.png"
        super().setup()


class OsrPath(CustomLabel):
    def __init__(self, parent):
        super(OsrPath, self).__init__(parent)
        self.main_window = parent

        self.pixmap_idle = "images/OsrPathIdle.png"
        super().setup()