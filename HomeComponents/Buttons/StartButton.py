import json
import os
import subprocess
import sys
from Parents import Button
from abspath import abspath, configpath, settingspath, Log
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
		self.parent = parent
		super().setup()

	def mouseclicked(self):
		if os.path.isdir(current_config["Output path"]):
			current_config["Output path"] = os.path.join(current_config["Output path"], "output.avi")

		with open(configpath, 'w+') as f:
			json.dump(current_config, f, indent=4)
			f.close()
		with open(settingspath, 'w+') as f:
			json.dump(current_settings, f, indent=4)
			f.close()

		if self.proc is None or self.proc.poll() is not None:
			outputfile = open(Log.runosupath, "w")
			self.proc = subprocess.Popen([sys.executable, os.path.join(abspath, "run_osu.py"), self.main_window.execpath], stdout=outputfile, stderr=outputfile)
			self.main_window.progressbar.show()
