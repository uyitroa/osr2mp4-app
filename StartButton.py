import json
import os
import threading

from Parents import Button
from config_data import current_config


class StartButton(Button):
	def __init__(self, parent):
		super(StartButton, self).__init__(parent)

		self.default_x = 515
		self.default_y = 350
		self.default_size = 3.5

		self.img_idle = "res/Start_Idle.png"
		self.img_hover = "res/Start_Hover.png"
		self.img_click = "res/Start_Click.png"
		self.img_shadow = "res/Start_Shadow.png"

		super().setup()

	def run_osu(self):
		from osr2mp4.osr2mp4 import Osr2mp4
		converter = Osr2mp4(filedata="config.json", filesettings="settings.json")
		converter.startall()
		converter.joinall()

	def mouseclicked(self):
		if os.path.isdir(current_config["Output path"]):
			current_config["Output path"] = os.path.join(current_config["Output path"], "output.avi")

		with open('config.json', 'w+') as f:
			json.dump(current_config, f, indent=4)
			f.close()
		print(current_config)
		func = threading.Thread(target=self.run_osu)
		func.start()
