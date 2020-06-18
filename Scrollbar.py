import os

import cv2
from PyQt5.QtWidgets import QScrollArea


class Scrollbar(QScrollArea):
	def __init__(self, parent, layout):
		super().__init__(parent)

		self.main_window = parent
		self.gridLayout = layout

		self.img_handle = "res/scroll_back.png"
		self.img_scroll = "res/SliderBall_HD.png"
		self.scrollsize = 30

		self.setWidgetResizable(True)
		self.setScrollStyle()
		self.setStyleSheet("background: transparent;")


	def setScrollStyle(self):
		scroll_handle = self.fixsize(self.img_handle)

		styleSheet = """

				QScrollBar:vertical {
				background: transparent;
				width: %ipx;
				image: url('%s');
				}


				QScrollBar::handle:vertical {
					background: transparent;
					height: 1px;
					image: url('%s');

				}

				QScrollBar::add-line:vertical {
					background: transparent;
					height: 1px;
					subcontrol-position: bottom;
					subcontrol-origin: margin;
				}

				QScrollBar::sub-line:vertical {
					height: 1px;
					subcontrol-position: top left;
					subcontrol-origin: margin;
					position: absolute;
					background: transparent;
				}

				QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
					background: transparent;
				}

				QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
					background: transparent;
				}""" % (self.scrollsize, scroll_handle, self.img_scroll)
		self.verticalScrollBar().setStyleSheet(styleSheet)

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		# reload scroll stylesheet
		scrollbar = self.verticalScrollBar()
		self.resizehandle(self.img_handle, scale * scrollbar.maximum() / 10 / self.scrollsize)
		scrollbar.style().unpolish(scrollbar)
		scrollbar.style().polish(scrollbar)
		scrollbar.update()

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

