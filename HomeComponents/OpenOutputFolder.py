from Custom.CustomWidgets import CustomLabel
class OpenOutputFolder(CustomLabel):
    def __init__(self, parent):
        super(OpenOutputFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OpenOutputFolderIdle.png"
        self.layout = self.main_window.open_output_button
        self.text = None

        super().setup()