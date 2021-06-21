from Custom.CustomWidgets import CustomButtons


class SelectOsuFolder(CustomButtons):
    def __init__(self, parent):
        super(SelectOsuFolder, self).__init__(parent)
        self.pixmap_idle = "images/OsuFolderIdle.png"
        self.pixmap_hover = "images/OsuFolderHover.png"
        self.pixmap_clicked = "images/OsuFolderClicked.png"
        self.file_extension = "folder"
        self.default_scale = [227, 53]
        self.default_coordinates = [389, 325]
        super().setup()
