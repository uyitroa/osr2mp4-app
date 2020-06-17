import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import cv2
import os


class Scroll_Class():
	def __init__(self, parent):
		super().__init__()

		self.nelements = 10
		self.layout_width, self.layout_height = 400, 250

		self.layout = QtWidgets.QHBoxLayout(parent)
		self.scrollArea = QtWidgets.QScrollArea(parent)
		self.scrollArea.setWidgetResizable(True)
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)

		self.setScrollStyle()

		self.layout.setGeometry(QtCore.QRect(20, 20, self.layout_width, self.layout_height))

		for i in range(self.nelements):
			self.gridLayout.addWidget(QtWidgets.QPushButton(), i, 2)

	def setScrollStyle(self):
		scroll_handle = "res/scroll_back.png"
		scroll_handle = self.fixsize(scroll_handle)
		scroll_ball = "res/SliderBall_HD.png"
		blank = "res/blank.png"

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
				}""" % (scroll_handle, scroll_ball, blank, blank)
		self.scrollArea.verticalScrollBar().setStyleSheet(styleSheet)

	def fixsize(self, filename):
		img = cv2.imread(filename, -1)
		scale = self.nelements/22
		img = cv2.resize(img, (0, 0), fx=0.5, fy=scale)
		filename, ext = os.path.splitext(filename)
		filename = filename + "1" + ext
		cv2.imwrite(filename, img)
		return filename
