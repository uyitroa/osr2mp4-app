from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel


class Separator(QLabel):
	def __init__(self):
		super().__init__()

		self.default_width = 500
		self.default_height = 10
		self.img = "res/Separator.png"
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
