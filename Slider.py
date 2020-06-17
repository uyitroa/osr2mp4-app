from PyQt5.QtWidgets import QSlider
from PyQt5 import QtCore
class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal) 
		self.setStyleSheet("""
		QSlider::handle:horizontal {
		image: url('res/start_slider.png');}
""")
		self.setFixedWidth(200)
