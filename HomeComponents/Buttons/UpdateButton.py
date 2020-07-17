import os
import sys

from PyQt5.QtWidgets import QLabel
import logging
from Parents import Button

import pkg_resources
import subprocess as sp
import io
from multiprocessing.pool import ThreadPool
import json
import sys
from urllib import request    
from pkg_resources import parse_version 
class UpdateButton(Button):
	def __init__(self, parent):
		super(UpdateButton, self).__init__(parent)
		self.osr2mp4_current_ver = pkg_resources.get_distribution("osr2mp4").version
		self.osr2mp4app_current_ver = pkg_resources.get_distribution("osr2mp4app").version

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(self.check_updates)

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
		self.text.setToolTip("{} | {}".format(self.osr2mp4_current_ver, self.osr2mp4app_current_ver))
		logging.info("{} | {}".format(self.osr2mp4_current_ver, self.osr2mp4app_current_ver))

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
		print("p")
		osr2mp4_latest_ver = get_version('osr2mp4')
		print("d")
		osr2mp4app_latest_ver = get_version('osr2mp4app')
		print("c")

		print(osr2mp4_latest_ver[0])
		print("B")
		print(osr2mp4app_latest_ver[0])
		print("A")
		if self.osr2mp4_current_ver == osr2mp4_latest_ver[0] and self.osr2mp4app_current_ver == osr2mp4app_latest_ver[0]:
			print("updated")
			self.hide()
		else:
			print("outdated")

def get_version(pkg_name):
	print("Z")
	url = f'https://pypi.python.org/pypi/{pkg_name}/json'
	print("Y")
	releases = json.loads(request.urlopen(url).read())['releases']
	print("BB")
	return sorted(releases, key=parse_version, reverse=True)  