import webbrowser

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit
from osr2mp4.Utils.getmods import mod_string_to_enums

from Info import Info
from SettingComponents.Components.Slider import StartTimeSlider, EndTimeSlider
from SettingComponents.Components.ToolTip import ClickableTooltip
from config_data import current_config, current_settings


class ParentTextbox(QLineEdit):
	def __init__(self, key=None, jsondata=None, datadict=None):
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

		self.key = key

		if datadict is not None:
			self.current_data = datadict
		else:
			if key in current_config:
				self.current_data = current_config
			else:
				self.current_data = current_settings

		if self.key not in self.current_data:
			self.current_data[self.key] = ""

		super().textChanged.connect(self.textChanged)
		self.raise_()

		tip = jsondata.get("desc", "")
		self.setToolTip(tip)
		self.installEventFilter(self)

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

	def tooltip_link_clicked(self, url):
		webbrowser.open(url)

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.ToolTip and source.toolTip():
			toolTip = ClickableTooltip.showText(
				QtGui.QCursor.pos(), source.toolTip(), source)
			toolTip.linkActivated.connect(self.tooltip_link_clicked)
			return True
		return super().eventFilter(source, event)


class BigTextBox(ParentTextbox):
	def __init__(self, key=None, jsondata=None, datadict=None):
		super().__init__(key=key, jsondata=jsondata, datadict=datadict)

		self.default_width = 250
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class SmallTextBox(ParentTextbox):
	def __init__(self, key=None, jsondata=None, datadict=None):
		super().__init__(key=key, jsondata=jsondata, datadict=datadict)

		self.default_width = 50
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class AverageTextBox(ParentTextbox):
	def __init__(self, key, jsondata=None, datadict=None):
		super().__init__(key=key, jsondata=jsondata, datadict=datadict)

		self.default_width = 100
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class VeryBigTextBox(ParentTextbox):
	def __init__(self, key=None, jsondata=None, datadict=None):
		super().__init__(key=key, jsondata=jsondata, datadict=datadict)

		self.default_width = 350
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class CustomModsTextBox(AverageTextBox):
	@QtCore.pyqtSlot(str)
	def textChanged(self, p_str):
		super().textChanged(p_str)
		mods = mod_string_to_enums(p_str)
		if Info.replay is not None:
			if p_str == "":
				Info.replay.mod_combination = Info.real_mod
			else:
				Info.replay.mod_combination = mods

			if not EndTimeSlider.objs or not StartTimeSlider.objs:
				return

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
			current_config["Start time"] = prevstart * scale / 1000
			if prevend != -1:
				EndTimeSlider.objs[0].setValue(prevend * scale)
				current_config["End time"] = prevend * scale / 1000

