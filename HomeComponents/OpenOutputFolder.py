from Custom.CustomWidgets import DefaultLabel
from PyQt5.QtGui import QPixmap
import os
import subprocess
class OpenOutputFolder(DefaultLabel):
    def __init__(self, parent):
        super(OpenOutputFolder, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/OpenOutputFolderIdle.png"
        self.img_hover = "images/OpenOutputFolderHover.png"
        self.img_clicked = "images/OpenOutputFolderClicked.png"
        self.pixmap_idle = QPixmap(os.path.join(self.main_window.app_directory, self.img_clicked))

        self.layout = self.main_window.open_output_button
        self.text = None
        super().setup()

    def on_clicked(self):
        output_dir = self.main_window.current_config["Output path"].replace("/", "\\")
        subprocess.Popen(['explorer', output_dir])



