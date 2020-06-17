from PyQt5.QtWidgets import QSlider
from PyQt5 import QtCore

from helper import getsize


class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal)

		self.img = "res/Slider_HD.png"
		self.default_width, self.default_height = 200, 50

		self.setStyleSheet("""
		QSlider::handle:horizontal {
		image: url(%s);}
""" % self.img)

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)
