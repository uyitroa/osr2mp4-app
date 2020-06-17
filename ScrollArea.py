from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
import os, json, cv2, sys


class Scroll_Class:
	def __init__(self, parent):
		super().__init__()

		self.nelements = 10
		self.layout_width, self.layout_height = 550, 450
		self.scrollsize = 30

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider}

		layout = QtWidgets.QHBoxLayout(parent)
		self.scrollArea = QtWidgets.QScrollArea(parent)
		self.scrollArea.setWidgetResizable(True)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		scrollAreaWidgetContents.setStyleSheet("background: rgb(49, 45, 45);")

		self.gridLayout = GridLayout(scrollAreaWidgetContents)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		layout.addWidget(self.scrollArea)

		layout.setGeometry(QtCore.QRect(20, 20, self.layout_width, self.layout_height))

		separator = QtWidgets.QLabel()
		separator_img = QtGui.QPixmap('res/Separator.png')
		separator_img = separator_img.scaled(500, 10, QtCore.Qt.KeepAspectRatio)
		separator.setPixmap(separator_img)


		with open('gui_config.json') as f:
			data = json.load(f)

		rowcounter = self.gridLayout.count
		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(separator, 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified

				self.gridLayout.smart_addWidget(Small_Titles(key), column)

				widgetname = data[header][key]["type"]
				Widget = self.widgetlists[widgetname]
				self.gridLayout.smart_addWidget(Widget(jsondata=data[header][key]), column)


		for x in range(10):
			self.gridLayout.addWidget(Small_Textbox(), rowcounter(), 0)

		self.setScrollStyle()

	def setScrollStyle(self):
		scroll_handle = "res/scroll_back.png"
		scroll_handle = self.fixsize(scroll_handle)
		scroll_ball = "res/SliderBall_HD.png"
		blank = "res/blank.png"

		styleSheet = """

				QScrollBar:vertical {
				width: %i px;
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
				}""" % (self.scrollsize, scroll_handle, scroll_ball, blank, blank)
		self.scrollArea.verticalScrollBar().setStyleSheet(styleSheet)

	def fixsize(self, filename):
		img = cv2.imread(filename, -1)
		scaley = self.nelements / self.scrollsize
		print(scaley)
		img = cv2.resize(img, (0, 0), fx=1, fy=scaley)
		filename, ext = os.path.splitext(filename)
		filename = filename + "1" + ext
		cv2.imwrite(filename, img)
		return filename
