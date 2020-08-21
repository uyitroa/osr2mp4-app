import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from SettingComponents.Components.Pathbox import PathBox
from SettingComponents.Layouts.GridLayout import GridLayout
from SettingComponents.Components.QLabel import Titles, SmallTitles
from SettingComponents.Components.Scrollbar import Scrollbar
from SettingComponents.Components.Separator import Separator
from SettingComponents.Components.Textbox import BigTextBox, SmallTextBox
from SettingComponents.Components.Slider import Slider
import json


class PPLayout(QtWidgets.QScrollArea):
	def __init__(self, parent, main_window):
		super().__init__(parent)

		self.main_window = parent

		self.loaded = False
		self.default_width, self.default_height = parent.default_width, parent.default_height - parent.ppsample.settings.height
		self.default_x, self.default_y = 10, parent.ppsample.settings.height

		self.widgetlists = {"Big_Textbox": BigTextBox, "Small_Textbox": SmallTextBox,
							"Titles": Titles, "Small_Titles": SmallTitles,
							"Slider": Slider, "PathBox": PathBox}

		self.layout = QtWidgets.QHBoxLayout(parent)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		self.setStyleSheet("background: gray;")
		self.gridLayout = GridLayout(scrollAreaWidgetContents)

		parent.default_width = self.default_width
		parent.default_height = self.default_height
		self.scrollArea = Scrollbar(parent, self.gridLayout)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)
		self.scrollArea.horizontalScrollBar().setEnabled(False)
		self.setWidgetResizable(False)
		self.setup()

	def setup(self):
		self.layout.setGeometry(QtCore.QRect(self.default_x, self.default_y, self.default_width, self.default_height))

	def load_settings(self, ppsettings):
		if self.loaded:
			return
		self.loaded = True

		with open(self.main_window.optionpath) as f:
			data = json.load(f)

		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified
				widgetname = data[header][key]["type"]

				widget = self.widgetlists[widgetname](key=key, jsondata=data[header][key], datadict=ppsettings)

				self.gridLayout.smart_addWidget(SmallTitles(key + ":"), column)
				self.gridLayout.smart_addWidget(widget, column+1)
			self.gridLayout.smart_addWidget(Titles(" "), 0)

		self.updatevalue()
		self.scrollArea.show()

	def updatevalue(self):
		self.gridLayout.updatevalue()
