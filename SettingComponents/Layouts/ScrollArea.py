import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from autologging import traced, logged

from SettingComponents.Components.Buttons import UpdateButton
from SettingComponents.Components.DoubleSlider import DoubleSlider
from SettingComponents.Components.Pathbox import PathBox
from SettingComponents.Layouts.GridLayout import GridLayout
from SettingComponents.Components.QLabel import Titles, SmallTitles
from SettingComponents.Components.Scrollbar import Scrollbar
from SettingComponents.Components.Separator import Separator
from SettingComponents.Components.Textbox import BigTextBox, SmallTextBox, CustomModsTextBox, VeryBigTextBox, \
	AverageTextBox
from SettingComponents.Components.Slider import Slider, EndTimeSlider, StartTimeSlider
import json
from SettingComponents.Components.CheckBox import CheckBox
from abspath import optionconfigpath
from config_data import current_config, current_settings


@logged(logging.getLogger(__name__))
@traced("changesize", exclude=True)
class ScrollArea(QtWidgets.QScrollArea):
	def __init__(self, parent, main_window):
		super().__init__()

		self.main_window = main_window
		self.settingspage = parent

		self.loaded = False
		self.default_width, self.default_height = parent.default_width, parent.default_height * 0.94
		self.default_x, self.default_y = 15, 15

		self.widgetlists = {"BigTextBox": BigTextBox, "SmallTextBox": SmallTextBox, "CustomModsTextBox": CustomModsTextBox,
		                    "VeryBigTextBox": VeryBigTextBox, "AverageTextBox": AverageTextBox,
							"Titles": Titles, "SmallTitles": SmallTitles,
							"Slider": Slider, "DoubleSlider": DoubleSlider, "StartTimeSlider": StartTimeSlider,
							"EndTimeSlider": EndTimeSlider,
							"CheckBox": CheckBox, "UpdateButton": UpdateButton, "PathBox": PathBox}

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

		scale = self.settingspage.height() / self.settingspage.default_height

		self.gridLayout.changesize(scale)

		x = scale * self.default_x
		y = scale * self.default_y
		width = self.settingspage.width()
		height = self.settingspage.height() * 0.93
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))
		self.scrollArea.changesize()

	def load_settings(self):
		if self.loaded:
			return
		self.loaded = True

		with open(optionconfigpath) as f:
			data = json.load(f)

		options, tooltips, headers = self.main_window.langs_dropdown.getlang()

		for header in data:
			self.gridLayout.smart_addWidget(Titles(headers.get(header, header)), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified
				widgetname = data[header][key]["type"]

				data[header][key]["desc"] = tooltips.get(key, "")
				data[header][key]["name"] = options.get(key, key)
				widget = self.widgetlists[widgetname](key=key, jsondata=data[header][key])

				if widgetname == "CheckBox" or widgetname == "UpdateButton":
					self.gridLayout.smart_addWidget(widget, column)
				else:
					self.gridLayout.smart_addWidget(SmallTitles(options.get(key, key) + ":"), column)
					self.gridLayout.smart_addWidget(widget, column)
			self.gridLayout.smart_addWidget(Titles(" "), 0)

		self.scrollArea.hide()
		self.scrollArea.raise_()

	def reload_settings(self):
		self.loaded = False

		while self.gridLayout.count():
			child = self.gridLayout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

		EndTimeSlider.objs = []
		StartTimeSlider.objs = []

		self.load_settings()
