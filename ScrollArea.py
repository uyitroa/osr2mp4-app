from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtQuickWidgets import QQuickWidget

from DoubleSlider import DoubleSlider
from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Scrollbar import Scrollbar
from Separator import Separator
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
import json
from CheckBox import CheckBox
import os
from RangeSlider import QRangeSlider
class ScrollArea:
	def __init__(self, parent):
		super().__init__()

		self.main_window = parent

		self.default_width, self.default_height = None, None
		self.default_x, self.default_y = None, None

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider, "DoubleSlider": DoubleSlider,
		                    "CheckBox": CheckBox}

		self.layout = QtWidgets.QHBoxLayout(parent)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		scrollAreaWidgetContents.setStyleSheet("background: transparent;border: none;")

		self.gridLayout = GridLayout(scrollAreaWidgetContents)

		self.scrollArea = Scrollbar(parent, self.gridLayout)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)
		self.scrollArea.horizontalScrollBar().setEnabled(False)
		self.scrollArea.horizontalScrollBar().setEnabled(True)

	def setup(self):
		self.layout.setGeometry(QtCore.QRect(self.default_x, self.default_y, self.default_width, self.default_height))

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.changesize(scale)

		x = scale * self.default_x
		y = scale * self.default_y
		width = scale * self.default_width
		height = scale * self.default_height
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))


		self.scrollArea.changesize()

	def load_settings(self):
		paths_config = load_paths()

		data_config = load_config()

		print(data_config)
		previous_text = ""
		with open('options_config.json') as f:
			data = json.load(f)

		rowcounter = self.gridLayout.count
		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified
				widgetname = data[header][key]["type"]
				Widget = self.widgetlists[widgetname]


				if widgetname == "CheckBox":
					self.gridLayout.addWidget(CheckBox(key), self.gridLayout.rowcounter[column], column)
				
				else:
					self.gridLayout.smart_addWidget(Small_Titles(key), column)
					self.gridLayout.smart_addWidget(Widget(jsondata=data[header][key]), column)

				if key[len(key)-1] == ":":	
					key = key[0:len(key)-1]


				if key in paths_config and bool(paths_config):
					print("Key {} in {}".format(key,paths_config))
					self.gridLayout.itemAtPosition(self.gridLayout.rowcounter[column] - 1, column).widget().setText(str(paths_config[key]))
				

				elif key in data_config and bool(data_config):
					self.gridLayout.itemAtPosition(self.gridLayout.rowcounter[column] - 1, column).widget().setText(str(data_config[key]))

		for x in range(10):
			render_ = QtWidgets.QLabel("Render Options")
			render_.setStyleSheet("""font: bold 24px;color:white;""")
			self.gridLayout.addWidget(render_, rowcounter(), 0)

		self.scrollArea.hide()
		self.scrollArea.raise_()

def load_paths():
	data = {}
	if os.path.isfile("user_data.json"):
		with open('user_data.json') as f:
			data = json.load(f)
	if not data == None:
		return data

def load_config():
	data = {}
	if os.path.isfile("config_data.json"):
		with open('config_data.json') as f:
			data = json.load(f)
	if not data == None:
		return data



	def setup(self):
		self.layout.setGeometry(QtCore.QRect(self.default_x, self.default_y, self.default_width, self.default_height))

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.changesize(scale)

		x = scale * self.default_x
		y = scale * self.default_y
		width = scale * self.default_width
		height = scale * self.default_height
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))


