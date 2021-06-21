from Custom.CustomWidgets import CustomButtons


class SelectBeatmap(CustomButtons):
    def __init__(self, parent):
        super(SelectBeatmap, self).__init__(parent)
        self.main_window = parent
        self.pixmap_idle = "images/SelectMapIdle.png"
        self.pixmap_hover = "images/SelectMapHover.png"
        self.pixmap_clicked = "images/SelectMapClicked.png"
        self.file_extension = "folder"
        super().setup()
