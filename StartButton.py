import json
import os
import subprocess

from Parents import Button
from config_data import current_config, current_settings


class StartButton(Button):
	def __init__(self, parent):
		super(StartButton, self).__init__(parent)

		self.default_x = 600
		self.default_y = 330
		self.default_size = 3.5

		self.img_idle = "res/Start_Idle.png"
		self.img_hover = "res/Start_Hover.png"
		self.img_click = "res/Start_Click.png"
		self.img_shadow = "res/Start_Shadow.png"
		self.proc = None

		super().setup()

	def mouseclicked(self):
		if os.path.isdir(current_config["Output path"]):
			current_config["Output path"] = os.path.join(current_config["Output path"], "output.avi")

		with open('config.json', 'w+') as f:
			json.dump(current_config, f, indent=4)
			f.close()
		with open('settings.json', 'w+') as f:
			json.dump(current_settings, f, indent=4)
			f.close()


		self.proc = subprocess.Popen(["python3", "run_osu.py"], shell=False)
