import os
import subprocess
import sys
from BaseComponents.Buttons import Button
from abspath import abspath, Log
from config_data import current_config
from helper.datahelper import save, loadname
import queue
from PyQt5 import QtGui, QtCore
from helper.helper import get_right_map


class BeatmapQueue(QtCore.QThread):
	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.queue = queue.Queue(maxsize=0)
		self.parent = parent

	def run(self):
		while True:
			item = self.queue.get()
			self.parent.processing_something = True
			print("mother item")
			for f_name in item:
				print("FUCK")
				mappath = get_right_map(f_name)
				self.parent.main_window.setreplay(f_name)
				self.parent.main_window.setmap(mappath)
				#current_config[".osr path"] = f_name
				#current_config["Beatmap path"] = mappath
				filename = loadname(current_config)
				save(filename)
				self.parent.main_window.progressbar.show()
				subprocess.call(
						[sys.executable, os.path.join(abspath, "run_osu.py"), self.parent.main_window.execpath])
			self.parent.processing_something = False
			self.queue.task_done()
			"""
			filename = loadname(current_config)
			save(filename)
			outputfile = open(Log.runosupath, "w")
			subprocess.Popen(
				[sys.executable, os.path.join(abspath, "run_osu.py"), self.parent.main_window.execpath], stdout=outputfile,
				stderr=outputfile)
			self.parent.main_window.progressbar.show()
			self.queue.task_done()
			"""

	def put(self, tmp_list):
		self.queue.put(tmp_list)


class StartButton(Button):
	def __init__(self, parent):
		super(StartButton, self).__init__(parent)
		self.beatmap_queue = BeatmapQueue(self)
		self.beatmap_queue.start()
		self.default_x = 600
		self.default_y = 330
		self.default_size = 3.5
		self.processing_something = False
		self.img_idle = "res/Start_Idle.png"
		self.img_hover = "res/Start_Hover.png"
		self.img_click = "res/Start_Click.png"
		self.img_shadow = "res/Start_Shadow.png"
		self.proc = None
		self.parent = parent
		super().setup()

	def mouseclicked(self):
		tmp_list = []
		for osr_path in current_config[".osr path"]:
			tmp_list.append(osr_path)
		self.beatmap_queue.put(tmp_list)

