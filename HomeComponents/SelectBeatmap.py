from Custom.CustomWidgets import CustomLabel


class SelectBeatmap(CustomLabel):
    def __init__(self, parent):
        super(SelectBeatmap, self).__init__(parent)
        self.pixmap_idle = "images/SelectMapIdle.png"
        self.pixmap_hover = "images/SelectMapHover.png"
        self.pixmap_clicked = "images/SelectMapClicked.png"
        self.default_scale = [328, 52]
        self.default_coordinates = [505, 85]
        super().setup()
