from Custom.CustomWidgets import CustomLabel


class Osr2mp4Logo(CustomLabel):
    def __init__(self, parent):
        super(Osr2mp4Logo, self).__init__(parent)
        self.pixmap_idle = "images/osr2mp4_logo.png"
        self.pixmap_hover = "images/osr2mp4_logo.png"
        self.pixmap_clicked = "images/osr2mp4_logo.png"
        self.default_scale = [365, 366]
        self.default_coordinates = [20, 30]
        super().setup()

