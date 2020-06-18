from PyQt5.QtCore import QUrl
from PyQt5.QtQuickWidgets import QQuickWidget


class DoubleSlider(QQuickWidget):
	def __init__(self):
		super().__init__()

		self.default_width = 200
		self.default_height = 300

		self.setSource(QUrl('rangeslider.qml'))
		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)
