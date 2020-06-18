from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QScrollBar, QCommonStyle

from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Separator import Separator
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
import os, json, cv2, sys


class Scroll_Class:
	def __init__(self, parent):
		super().__init__()

		self.main_window = parent

		self.layout_width, self.layout_height = 550, 450
		self.layout_x, self.layout_y = 20, 20
		self.scrollsize = 30
		self.defaultspacing = 10

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider}
		self.img_handle = "res/scroll_back.png"
		self.img_scroll = "res/SliderBall_HD.png"

		self.layout = QtWidgets.QHBoxLayout(parent)
		self.scrollArea = QtWidgets.QScrollArea(parent)
		self.scrollArea.setWidgetResizable(True)
		scrollAreaWidgetContents = QtWidgets.QWidget()

		self.gridLayout = GridLayout(scrollAreaWidgetContents)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)

		self.layout.setGeometry(QtCore.QRect(self.layout_x, self.layout_y, self.layout_width, self.layout_height))


		with open('gui_config.json') as f:
			data = json.load(f)

		rowcounter = self.gridLayout.count
		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified

				self.gridLayout.smart_addWidget(Small_Titles(key), column)

				widgetname = data[header][key]["type"]
				Widget = self.widgetlists[widgetname]
				self.gridLayout.smart_addWidget(Widget(jsondata=data[header][key]), column)


		for x in range(10):
			render_ = QtWidgets.QLabel("Render Options")
			render_.setStyleSheet("""font: bold 24px;color:white;""")
			self.gridLayout.addWidget(render_, rowcounter(), 0)

		self.setScrollStyle()
		scrollAreaWidgetContents.setStyleSheet("background: transparent;")
		self.scrollArea.setStyleSheet("background: transparent;")
		self.scrollArea.verticalScrollBar().setStyle(QCommonStyle())

		self.gridLayout.setSpacing(self.defaultspacing)

		print("settings")

	def setScrollStyle(self):
		scroll_handle = self.fixsize(self.img_handle)
		blank = "res/blank.png"

		styleSheet = """

				QScrollBar:vertical {
				background-color: transparent;
				border: none;
				width: %ipx;
				image: url('%s');
				}


				QScrollBar::handle:vertical {
					background-color: transparent;
					border: none;
					height: 1px;
					image: url('%s');
				
				}
				
				QScrollBar::add-line:vertical {
					background-color: transparent;
					border: none;
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
					border: none;
				}
				
				QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
					background-color: transparent;
					border: none;
				}
				
				QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
					background-color: transparent;
					border: none;
				}""" % (self.scrollsize, scroll_handle, self.img_scroll)
		self.scrollArea.verticalScrollBar().setStyleSheet(styleSheet)


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

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.setSpacing(scale * self.defaultspacing)

		x = scale * self.layout_x
		y = scale * self.layout_y
		width = scale * self.layout_width
		height = scale * self.layout_height
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))

		for x in range(self.gridLayout.count()):
			item = self.gridLayout.itemAt(x).widget()

			if type(item).__name__ == "QLabel":
				continue

			width = item.default_width * scale
			height = item.default_height * scale
			item.setFixedWidth(width)
			item.setFixedHeight(height)

		# reload scroll stylesheet
		scrollbar = self.scrollArea.verticalScrollBar()
		self.resizehandle(self.img_handle, scale * scrollbar.maximum() / 10 / self.scrollsize)
		scrollbar.style().unpolish(scrollbar)
		scrollbar.style().polish(scrollbar)
		scrollbar.update()
