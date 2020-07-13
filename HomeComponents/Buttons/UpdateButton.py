import os
import sys

from PyQt5.QtWidgets import QLabel
import logging
from Parents import Button

import pkg_resources
import subprocess as sp
import io

class UpdateButton(Button):
	def __init__(self, parent):
		super(UpdateButton, self).__init__(parent)

		self.default_x = 20
		self.default_y = 430
		self.default_size = 0.5
		self.text_x = 500
		self.text_y = -10
		self.default_fontsize = 250

		self.img_idle = "res/SmallText_HD.png"
		self.img_hover = "res/SmallText_HD.png"
		self.img_click = "res/SmallText_HD.png"
		super().setup()

		self.text = QLabel(self)
		self.text.setText("Update")
		self.text.setToolTip("0.0.2a3")
		logging.info("0.0.2a3")

	def mouseclicked(self):
		# proc = subprocess.Popen([sys.executable, "updater.py"])
		fupdate = open(os.path.join(self.main_window.execpath, "exit.txt"), "w")
		fupdate.write("1")
		fupdate.close()
		sys.exit(0)

	def changesize(self):
		super().changesize()
		scale = self.height()/self.main_window.default_height

		x = scale * self.text_x
		y = scale * self.text_y

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("QLabel{font-size: %ipt; font-weight: bold; color: white; background-color: transparent;}QToolTip { background-color:white;color: black; }" % fontsize)
		self.text.setGeometry(x, y, self.width(), self.height())

	def check_updates(self):
		process = sp.Popen(['pip', 'search', 'osr2mp4'], stdout=sp.PIPE)
		stdout = str(process.communicate()[0]).split(":")
		for x in range(len(stdout)):
			if "LATEST" in stdout[x]:
				latest_version = stdout[x+1]
				break

		current_version = pkg_resources.get_distribution("osr2mp4").version
		print("version:", current_version)
		if current_version == latest_version.strip().split(" ")[0]:
			print("updated")
			self.hide()
		else:
			print("outdated")
			