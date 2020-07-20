import os
import sys

from PyQt5.QtWidgets import QLabel
import logging
from Parents import Button

import pkg_resources
import json
import sys
from urllib import request    
from pkg_resources import parse_version 
import threading


class UpdateButton(Button):
	def __init__(self, parent):
		super(UpdateButton, self).__init__(parent)
		self.main_window = parent
		self.osr2mp4_current_ver = pkg_resources.get_distribution("osr2mp4").version
		self.osr2mp4app_current_ver = pkg_resources.get_distribution("osr2mp4app").version
		x = threading.Thread(target=self.check_updates)
		x.start()
		self.default_x = 20
		self.default_y = 400
		self.default_size = 0.5
		self.text_x = 500
		self.text_y = -10
		self.default_fontsize = 250

		self.img_idle = "res/SmallButton.png"
		self.img_hover = "res/SmallButton hover.png"
		self.img_click = "res/SmallButton click.png"

		super().setup()

		self.text = QLabel(self)
		self.text.setText("Update")
		self.text.setToolTip("{} | {}".format(self.osr2mp4_current_ver, self.osr2mp4app_current_ver))
		logging.info("{} | {}".format(self.osr2mp4_current_ver, self.osr2mp4app_current_ver))
		self.hide()

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
		osr2mp4_latest_ver = get_version('osr2mp4')
		osr2mp4app_latest_ver = get_version('osr2mp4app')
		logging.info("Latest Version of osr2mp4: {}".format(osr2mp4_latest_ver[0]))
		logging.info("Latest Version of osr2mp4app: {}".format(osr2mp4app_latest_ver[0]))
		logging.info("Current Version of osr2mp4: {}".format(self.osr2mp4_current_ver))
		logging.info("Current Version of osr2mp4app: {}".format(self.osr2mp4app_current_ver))

		if self.osr2mp4_current_ver == osr2mp4_latest_ver[0] and self.osr2mp4app_current_ver == osr2mp4app_latest_ver[0]:
			print("Updated")
			self.hide()
		else:
			print("Outdated")
			self.show()


def get_version(pkg_name):
	url = f'https://pypi.python.org/pypi/{pkg_name}/json'
	releases = json.loads(request.urlopen(url).read())['releases']
	return sorted(releases, key=parse_version, reverse=True)
