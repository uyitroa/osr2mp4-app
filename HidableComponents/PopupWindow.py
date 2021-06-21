from Custom.CustomWidgets import CustomLabel


class PopupWindow(CustomLabel):
    def __init__(self, parent):
        super(PopupWindow, self).__init__(parent)
        self.pixmap_idle = "images/PopupWindow.png"
        self.default_scale = [506, 330]
        self.default_coordinates = [150, 70]
        super().setup()

