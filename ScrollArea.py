import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from DoubleSlider import DoubleSlider
from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Scrollbar import Scrollbar
from Separator import Separator
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider, EndTimeSlider, StartTimeSlider
import json
from CheckBox import CheckBox
from abspath import abspath, optionconfigpath

from config_data import current_settings, current_config


class ScrollArea(QtWidgets.QScrollArea):
	def __init__(self, parent, main_window):
		super().__init__()

		self.main_window = parent

		self.loaded = False
		self.default_width, self.default_height = parent.default_width, parent.default_height * 0.94
		self.default_x, self.default_y = 15, 15

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider, "DoubleSlider": DoubleSlider, "StartTimeSlider": StartTimeSlider, "EndTimeSlider": EndTimeSlider,
		                    "CheckBox": CheckBox}

		self.layout = QtWidgets.QHBoxLayout(parent)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		scrollAreaWidgetContents.setStyleSheet("background: transparent;border: none;")

		self.gridLayout = GridLayout(scrollAreaWidgetContents)

		self.scrollArea = Scrollbar(parent, self.gridLayout)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)
		self.scrollArea.horizontalScrollBar().setEnabled(False)
		self.setWidgetResizable(False)

	def setup(self):
		self.layout.setGeometry(QtCore.QRect(self.default_x, self.default_y, self.default_width, self.default_height))

	def changesize(self):

		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.changesize(scale)

		x = scale * self.default_x
		y = scale * self.default_y
		width = self.main_window.width()
		height = self.main_window.height() * 0.93
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))
		self.scrollArea.changesize()

	def load_settings(self):
		if self.loaded:
			return
		self.loaded = True

		data_config = {"config": current_config, "settings": current_settings}

		print(data_config)
		with open(optionconfigpath) as f:
			data = json.load(f)

		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified
				widgetname = data[header][key]["type"]


				jsondata = {"option_config": data[header][key], "data": data_config, "key": key}
				widget = self.widgetlists[widgetname](jsondata=jsondata)


				if widgetname == "CheckBox":
					self.gridLayout.smart_addWidget(CheckBox(jsondata=jsondata), column)
				else:
					self.gridLayout.smart_addWidget(Small_Titles(key + ":"), column)
					self.gridLayout.smart_addWidget(widget, column)
			self.gridLayout.smart_addWidget(Titles(" "), 0)




		self.scrollArea.hide()
		self.scrollArea.raise_()

		print("settings")

	def reload_settings(self):
		self.loaded = False
		self.load_settings()
