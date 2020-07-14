import os
import sys

from PyQt5.QtWidgets import QLabel
import logging
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui


class Buttons(QPushButton):
	def __init__(self, jsondata=None):
		super().__init__()


		self.default_x = 20
		self.default_y = 20
		self.default_width, self.default_height = 100, 10

		self.default_fontsize = 1

		self.img_icon = "res/SmallText_HD.png"
		self.setIcon(QtGui.QIcon(self.img_icon))

		self.text = QLabel(self)
		self.text.setText(jsondata["key"])

		'''self.text.setToolTip("0.0.2a3")
								logging.info("0.0.2a3")
						'''
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
		self.text.setGeometry(x, y, self.width(), self.height())

	def setFixedHeight(self, p_int):
		pass
	def updatevalue(self):
		pass
class Small_Buttons(Buttons):
	def __init__(self, jsondata=None):
		super().__init__(jsondata=jsondata)
		self.default_x = 20
		self.default_y = 430
		self.default_width, self.default_height = 100, 10
		
		self.default_fontsize = 100

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_width)
