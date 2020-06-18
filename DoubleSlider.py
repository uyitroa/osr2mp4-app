from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from RangeSlider import QRangeSlider


class DoubleSlider(QWidget):
	def __init__(self):
		super().__init__()

		self.default_width = 300
		self.default_height = 30

		self.setStyleSheet("image: url(res/Slider_HD.png);")
		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)

		self.rangeslider = QRangeSlider(self)
