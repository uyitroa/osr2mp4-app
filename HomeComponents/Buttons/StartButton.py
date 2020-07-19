import json
import os
import subprocess
import sys
from Parents import Button
from abspath import abspath, configpath, settingspath, Log
from config_data import current_config, current_settings
from helper.helper import save, loadname


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
		filename = loadname(current_config)
		save(filename)

		if self.proc is None or self.proc.poll() is not None:
			outputfile = open(Log.runosupath, "w")
			self.proc = subprocess.Popen([sys.executable, os.path.join(abspath, "run_osu.py"), self.main_window.execpath], stdout=outputfile, stderr=outputfile)
			self.main_window.progressbar.show()
