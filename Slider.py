from PyQt5.QtWidgets import QSlider
from PyQt5 import QtCore

from helper import getsize


class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal)

		self.img = "res/Sliderball2_Scale.png"
		self.default_width, self.default_height = 300, 30

		self.setStyleSheet("""
QSlider {
    min-height: 68px;
    max-height: 68px;
}
QSlider::groove:horizontal 
{
	image: url(res/Slider_HD.png);

}

QSlider::handle:horizontal 
{
	image: url(%s);
}


""" % self.img)

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)
	
	def setFixedHeight(self, p_int):
		pass
