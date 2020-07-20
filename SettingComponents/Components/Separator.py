import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel

from abspath import abspath


class Separator(QLabel):
	def __init__(self, width=500):
		super().__init__()

		self.default_width = width
		self.default_height = 10
		self.img = os.path.join(abspath, "res/Separator.png")
		self.load(1)

	def load(self, scale):
		separator_img = QtGui.QPixmap(self.img)
		separator_img = separator_img.scaled(self.default_width * scale, self.default_height * scale, QtCore.Qt.KeepAspectRatio)
		self.setPixmap(separator_img)

	def setFixedWidth(self, p_int):
		scale = p_int / self.default_width
		self.load(scale)

	def setFixedHeight(self, p_int):
		pass

	def updatevalue(self):
		pass
