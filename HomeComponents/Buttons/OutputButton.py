import os

from Parents import PopupButton
from config_data import current_config


class OutputButton(PopupButton):
	def __init__(self, parent):
		super(OutputButton, self).__init__(parent)

		self.default_x = 213
		self.default_y = 330
		self.default_size = 3.35
		self.file_type = "Folder"

		self.img_idle = "res/OutputFolder_Idle.png"
		self.img_hover = "res/OutputFolder_Hover.png"
		self.img_click = "res/OutputFolder_Click.png"
		self.parent = parent
		super().setup()

	def afteropenfile(self, filename):
		current_config["Output path"] = filename
		if current_config["Output name"] == "":
			current_config["Output name"] = "{Map} played by {Player}.avi"
		super().afteropenfile(filename)
