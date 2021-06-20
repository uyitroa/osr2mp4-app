from Custom.CustomWidgets import CustomLabel


class SelectOsr(CustomLabel):
    def __init__(self, parent):
        super(SelectOsr, self).__init__(parent)
        self.pixmap_idle = "images/SelectOsrIdle.png"
        self.pixmap_hover = "images/SelectOsrHover.png"
        self.pixmap_clicked = "images/SelectOsrClicked.png"
        self.default_scale = [346, 52]
        self.default_coordinates = [490, 30]
        super().setup()
