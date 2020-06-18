import os

import cv2
from PyQt5.QtWidgets import QScrollArea

from PyQt5.QtWidgets import QSlider
from PyQt5 import QtCore


class CustomScrolbar(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent)
		self.setOrientation(QtCore.Qt.Vertical)

		self.default_width, self.default_height = 20, 400
		self.default_x, self.default_y = 500, -100

		self.img_handle = "res/SliderBall_HD.png"
		self.img_scroll = "res/scroll_back.png"

		self.setScrollStyle()
		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)

	def setScrollStyle(self):
		self.setStyleSheet("""
		QSlider::groove:vertical 
		{
			border-image: url(%s);
		    height:%ipx;
		}

		QSlider::handle:vertical 
		{
			image: url(%s);
			margin: -6px 0;
		}


		""" % (self.img_scroll, self.default_height, self.img_handle))


class Scrollbar(QScrollArea):
	def __init__(self, parent, layout):
		super().__init__(parent)

		self.main_window = parent
		self.gridLayout = layout

		self.scrollsize = 30
		self.customscroll = CustomScrolbar(self)

		self.setWidgetResizable(True)
		self.setScrollStyle()
		self.setStyleSheet("background: transparent;border: none;")


	def setScrollStyle(self):
		# scroll_handle = self.fixsize(self.img_handle)

		styleSheet = """
 QScrollBar:vertical {
     width: 0px;
     height: 0px;
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
     width: 0px;
     height: 0px;
     background: none;
 }

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     background: none;
 }
 """
		self.verticalScrollBar().setStyleSheet(styleSheet)



	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		# reload scroll stylesheet
		# scrollbar = self.verticalScrollBar()
		# self.resizehandle(self.img_handle, scale * scrollbar.maximum() / 15 / self.scrollsize)
		# scrollbar.style().unpolish(scrollbar)
		# scrollbar.style().polish(scrollbar)
		# scrollbar.update()

	def fixsize(self, filename):
		self.np_handle = cv2.imread(filename, -1)
		scaley = self.gridLayout.rowcounter[0] / self.scrollsize
		return self.resizehandle(filename, scaley)

	def resizehandle(self, filename, scaley):
		scaley = max(0.01, scaley)
		img = cv2.resize(self.np_handle, (0, 0), fx=1, fy=scaley)
		filename, ext = os.path.splitext(filename)
		filename = filename + "1" + ext
		cv2.imwrite(filename, img)
		return filename

