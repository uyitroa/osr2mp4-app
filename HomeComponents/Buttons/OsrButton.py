import os
from BaseComponents.Buttons import ButtonBrowse
from config_data import current_config

from helper.helper import get_right_map


class OsrButton(ButtonBrowse):
	def __init__(self, parent):
		super(OsrButton, self).__init__(parent)

		self.default_x = 490
		self.default_y = 30
		self.default_size = 3.5
		self.file_type = ".osr"

		self.img_idle = "res/B1_Idle.png"
		self.img_hover = "res/B1_Hover.png"
		self.img_click = "res/B1_Click.png"
		self.img_shadow = "res/B1_Shadow.png"

		self.browsepath = os.path.join(current_config["osu! path"], "Replays/")

		super().setup()

	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return

		self.main_window.setreplay(filename)
		mappath = get_right_map(filename)
		if mappath is not None:
			self.main_window.setmap(mappath)
