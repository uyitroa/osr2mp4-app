import json
import os
import subprocess
import sys
import psutil
from Parents import Button
from abspath import abspath, configpath, settingspath, Log
from config_data import current_config, current_settings

class CancelButton(Button):
	def __init__(self, parent):
		super(CancelButton, self).__init__(parent)

		self.default_x = 600
		self.default_y = 330
		self.default_size = 3.5

		self.img_idle = "res/CancelButton.png"
		self.img_hover = "res/CancelButton_hover.png"
		self.img_click = "res/CancelButton_click.png"
		# self.img_shadow = "res/CancelButton_shadow.png"
		self.proc = None
		self.parent = parent
		super().setup()
    
	def kill(self, proc_pid):
		process = psutil.Process(proc_pid)
		for proc in process.children(recursive=True):
			proc.kill()
		process.kill()
    
	def mouseclicked(self):
		if self.main_window.startbutton.proc is not None and self.main_window.startbutton.proc.poll() is None:
			self.kill(self.main_window.startbutton.proc.pid)
		with open("progress.txt", "w") as file:
			file.write("done")