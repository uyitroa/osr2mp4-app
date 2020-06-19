from PyQt5.QtWidgets import QSlider, QToolTip
from PyQt5 import QtCore
from PyQt5 import QtGui
from osr2mp4.Parser import osuparser
from osr2mp4.Utils.HashBeatmap import get_osu
from osr2mp4.Parser import osuparser
import osrparse


class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal)

		self.img = "res/Sliderball2_Scale.png"
		self.default_width, self.default_height = 250, 10

		self.setStyleSheet("""
QSlider {
}
QSlider::groove:horizontal 
{
	image: url(res/Slider_HD.png);

}

QSlider::handle:horizontal 
{
	image: url(%s);
}
QToolTip { 
background-color:rgba(0, 0, 255, 127);
color: white; 
}
""" % self.img)

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)

		self.setMinimum(jsondata["option_config"]["min"] * 1000)
		self.setMaximum(jsondata["option_config"]["max"] * 1000)
		self.setSingleStep(jsondata["option_config"]["step"] * 1000)

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		super().valueChanged.connect(self.valueChanged)
		print(self.current_data, self.key)
		self.setValue(self.current_data[self.key] * 1000)

	def setFixedHeight(self, p_int):
		pass

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		self.current_data[self.key] = p_int / 1000
		QToolTip.showText(QtGui.QCursor.pos(), str(p_int/1000), self)


class Map:
	length = None
	name = None


class StartTimeSlider(Slider):

	def __init__(self, parent=None, jsondata=None):

		jsondata["option_config"]["min"] = 0
		jsondata["option_config"]["step"] = 1

		if Map.length is None:
			try:
				self.get_maplength(jsondata)
			except FileNotFoundError:
				print("replay not specified yet")
				Map.length = 1
				Map.name = None
		print(Map.length)
		jsondata["option_config"]["max"] = Map.length

		super().__init__(parent=parent, jsondata=jsondata)

	@classmethod
	def get_maplength(cls, jsondata):

		if Map.name == jsondata["data"]["config"][".osr path"]:
			return
		Map.name = jsondata["data"]["config"][".osr path"]

		replay_data = osrparse.parse_replay_file(jsondata["data"]["config"][".osr path"])

		laststring = jsondata["data"]["config"]["Beatmap path"][-1]
		if laststring != "/" and laststring != "\\":
			jsondata["data"]["config"]["Beatmap path"] += "/"

		mappath = get_osu(jsondata["data"]["config"]["Beatmap path"], replay_data.beatmap_hash)
		color = {"ComboNumber": 1}
		osudata = osuparser.read_file(mappath, 1, color, False)

		Map.length = osudata.hitobjects[-1]["end time"] - osudata.hitobjects[0]["time"]
		Map.length /= 1000

	def setFixedHeight(self, p_int):
		if Map.length is not None:
			self.setMaximum(Map.length * 1000)
		super().setFixedHeight(p_int)


class EndTimeSlider(StartTimeSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		if self.current_data[self.key] == -1:
			val = self.maximum()
		else:
			val = self.current_data[self.key] * 1000

		self.setValue(val)

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		if p_int == self.maximum():
			p_int = -1000
		self.current_data[self.key] = p_int / 1000
		QToolTip.showText(QtGui.QCursor.pos(), str(p_int/1000), self)
