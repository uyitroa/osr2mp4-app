import os

from Parents import ButtonBrowse
from config_data import current_config


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
		replay_name = os.path.split(filename)[-1]
		current_config[".osr path"] = filename
		self.main_window.osrpath.setText(replay_name)

		try:
			self.main_window.find_latestMap(replay_name)
		except Exception as e:
			print(e)
