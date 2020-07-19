import os
import sys
from PyQt5.QtWidgets import QLabel

from abspath import abspath


class UpdateButton(QLabel):
	def __init__(self, jsondata=None, default_fontsize=1):
		super().__init__()
		self.default_width = 75
		self.default_height = 27
		self.img = os.path.join(abspath, "res/update_HD.png")
		self.default_fontsize = default_fontsize
		self.setFixedWidth(self.default_width)
		self.setFixedWidth(self.default_height)
		self.setStyleSheet("""border-image:url(%s)""" % self.img)

	# def setFixedHeight(self, p_int):
	# 	pass

	def mousePressEvent(self, event):
		fupdate = open("exit.txt", "w")
		fupdate.write("1")
		fupdate.close()
		sys.exit(0)

	def updatevalue(self):
		pass
