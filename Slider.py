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
		self.default_width, self.default_height = 250, 20

		self.setStyleSheet("""
QSlider::groove:horizontal 
{
	image: url(res/Slider_HD.png);

}

QSlider::handle:horizontal 
{
	image: url(%s);
}
QToolTip { 
background-color:rgb(10, 14, 13);
opacity: 150;
color: white; 
}
""" % self.img)

		self.default_min = jsondata["option_config"]["min"] * 1000
		self.default_max = jsondata["option_config"]["max"] * 1000

		self.bordersize = self.cursize = (self.default_max - self.default_min) * 0.0125

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)

		self.setMinimum(self.default_min - self.bordersize)
		self.setMaximum(self.default_max + self.bordersize)
		self.setSingleStep(jsondata["option_config"]["step"] * 1000)


		step = jsondata["option_config"]["step"]
		self.precision = len(str(step-int(step))[1:])

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		super().valueChanged.connect(self.valueChanged)
		self.setValue(self.current_data[self.key] * 1000)

	def setFixedHeight(self, p_int):
		super().setFixedHeight(p_int)
		size = self.cursize = self.bordersize * (p_int/self.default_height)
		self.setMinimum(self.default_min - size)
		self.setMaximum(self.default_max + size)

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		val = max(self.minimum() + self.cursize, self.sliderPosition())
		val = min(self.maximum() - self.cursize, val)
		self.setSliderPosition(val)

		self.current_data[self.key] = round(self.value() / 1000, self.precision)

		show = round(self.value() / 1000, self.precision)
		if show == int(show):
			show = int(show)
		QToolTip.showText(QtGui.QCursor.pos(), str(show), self)


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
			self.default_max = Map.length * 1000
			self.bordersize = (self.default_max - self.default_min) * 0.0125
		super().setFixedHeight(p_int)



class EndTimeSlider(StartTimeSlider):
	def __init__(self, parent=None, jsondata=None):
		endtime = jsondata["data"]["config"]["End time"]
		super().__init__(parent=parent, jsondata=jsondata)
		if endtime == -1:
			val = self.maximum()
		else:
			val = self.current_data[self.key] * 1000

		self.setValue(val)

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		super().valueChanged(p_int)
		if p_int >= self.maximum() - self.cursize:
			self.current_data[self.key] = -1

