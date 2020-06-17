import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import cv2


class Scroll_Class():
	def __init__(self, parent):
		super().__init__()

		self.layout = QtWidgets.QHBoxLayout(parent)
		self.scrollArea = QtWidgets.QScrollArea(parent)
		self.scrollArea.setWidgetResizable(True)
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)

		self.setScrollStyle()

		self.layout.setGeometry(QtCore.QRect(20, 20, 400, 250))

		self.nelements = 10

		for i in range(self.nelements):
			self.gridLayout.addWidget(QtWidgets.QPushButton(), i, 2)

	def setScrollStyle(self):
		scroll_handle = "res/scroll_back.png"
		scroll_ball = "res/SliderBall_HD.png"

		styleSheet = """

				QScrollBar:vertical {
				height: 100px;
				width: 10px;
				image: url('%s');
				}


				QScrollBar::handle:vertical {
					background: transparent;
					height: 1px;
					image: url('%s');
				
				}
				
				QScrollBar::add-line:vertical {
					height: 1px;
					subcontrol-position: bottom;
					subcontrol-origin: margin;
				}
				
				QScrollBar::sub-line:vertical {
					height: 1px;
					subcontrol-position: top left;
					subcontrol-origin: margin;
					position: absolute;
					image: url('%s');
				}
				
				QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
					image: url('%s');
				}
				
				QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
					background: transparent;
				}""" % (scroll_handle, scroll_ball, scroll_handle, scroll_handle)
		self.scrollArea.verticalScrollBar().setStyleSheet(styleSheet)

	def fixsize(self, filename):
		img = cv2.imread(filename, -1)
		
