import os
from BaseComponents.Buttons import ButtonBrowse
from config_data import current_config
from helper.osudatahelper import parse_osu


class osuMapButton(ButtonBrowse):
	def __init__(self, parent):
		super(osuMapButton, self).__init__(parent)

		self.default_x = 505
		self.default_y = 85
		self.default_size = 3.35
		self.file_type = ".osu"

		self.img_idle = "res/B3_Idle.png"
		self.img_hover = "res/B3_Hover.png"
		self.img_click = "res/B3_Click.png"

		self.browsepath = os.path.join(current_config["osu! path"], "Songs/")

		super().setup()
		self.hide()

	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return
		current_config["Beatmap path"] = filename
		self.main_window.mapsetpath.setText(os.path.basename(filename))
		parse_osu(filename)
