from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from RangeSlider import QRangeSlider


class DoubleSlider(QWidget):
	def __init__(self, jsondata=None):
		super().__init__()

		self.default_width = 300
		self.default_height = 30

		self.setStyleSheet("image: url(res/Slider_HD.png);")
		super().setFixedWidth(self.default_width)
		super().setFixedHeight(self.default_height)

		self.rangeslider = QRangeSlider(self)

	def setFixedHeight(self, p_int):
		self.rangeslider.setFixedHeight(p_int)
		super().setFixedHeight(p_int)

	def setFixedWidth(self, p_int):
		self.rangeslider.setFixedWidth(p_int)
		super().setFixedWidth(p_int)
