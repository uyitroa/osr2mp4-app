import os
import webbrowser
from PyQt5.QtWidgets import QLabel
from Parents import Button
from config_data import current_config


class FolderButton(Button):
	def __init__(self, parent):
		super(FolderButton, self).__init__(parent)
		self.main_window = parent
		self.default_x = 200
		self.default_y = 400
		self.default_size = 0.5
		self.text_x = 500
		self.text_y = -10
		self.default_fontsize = 250

		self.img_idle = "res/SmallButton.png"
		self.img_hover = "res/SmallButton hover.png"
		self.img_click = "res/SmallButton click.png"

		super().setup()

		self.text = QLabel(self)
		self.text.setText("Open Folder")

	def mouseclicked(self):
		outputpath = current_config["Output path"]
		if not os.path.isdir(outputpath):
			outputpath = os.path.dirname(outputpath)
		webbrowser.open("file:///" + outputpath)

	def changesize(self):
		super().changesize()
		scale = self.height()/self.main_window.default_height

		x = scale * self.text_x
		y = scale * self.text_y

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("QLabel{font-size: %ipt; font-weight: bold; color: white; background-color: transparent;}" % fontsize)
		self.text.setGeometry(x, y, self.width(), self.height())
