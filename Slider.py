from PyQt5.QtWidgets import QSlider
from PyQt5 import QtCore

from helper import getsize


class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal)

		self.img = "res/Sliderball2_Scale.png"
		self.default_width, self.default_height = 200, 20

		self.setStyleSheet("""
QSlider::groove:horizontal 
{
	border-image: url(res/Slider_HD.png);
    height:10px;
}

QSlider::handle:horizontal 
{
	image: url(%s);
	margin: -6px 0;
}


""" % self.img)

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)
	
	def setFixedHeight(self, p_int):
		pass
