from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit
from osr2mp4.Utils.getmods import mod_string_to_enums

from Info import Info
from SettingComponents.Components.Slider import StartTimeSlider, EndTimeSlider
from config_data import current_config


class ParentTextbox(QLineEdit):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.default_width = 1
		self.default_height = 1

		self.setStyleSheet("""
		QLineEdit {
		 border: 2px solid white;
		 border-radius: 6px;
		 color:white;
		}
		""")

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		if jsondata["key"] not in self.current_data:
			self.current_data[jsondata["key"]] = ""

		super().textChanged.connect(self.textChanged)
		self.raise_()

	def updatevalue(self):
		self.setText(str(self.current_data[self.key]))

	def setFixedHeight(self, p_int):
		pass

	@QtCore.pyqtSlot(str)
	def textChanged(self, p_str):
		if p_str.isdigit():
			p_str = int(p_str)
		else:
			try:
				p_str = float(p_str)
			except ValueError:
				pass
		self.current_data[self.key] = p_str


class BigTextBox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		self.default_width = 250
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class SmallTextBox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		self.default_width = 50
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class CustomModsTextBox(SmallTextBox):
	@QtCore.pyqtSlot(str)
	def textChanged(self, p_str):
		super().textChanged(p_str)
		mods = mod_string_to_enums(p_str)
		if Info.replay is not None:
			if p_str == "":
				Info.replay.mod_combination = Info.real_mod
			else:
				Info.replay.mod_combination = mods

			# hmmmmmmmmmmm
			prevmax = EndTimeSlider.objs[0].maximum()
			prevstart = StartTimeSlider.objs[0].value()
			prevend = EndTimeSlider.objs[0].value()
			if current_config["End time"] == -1:
				prevend = -1

			StartTimeSlider.objs[0].updatetime()
			EndTimeSlider.objs[0].updatetime()
			EndTimeSlider.objs[0].updateendtime()

			scale = EndTimeSlider.objs[0].maximum()/prevmax
			StartTimeSlider.objs[0].setValue(prevstart * scale)
			if prevend != -1:
				EndTimeSlider.objs[0].setValue(prevend * scale)

