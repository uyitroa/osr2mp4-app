import os

from PyQt5.QtWidgets import QSlider, QToolTip
from PyQt5 import QtCore
from PyQt5 import QtGui
from osr2mp4.Exceptions import BeatmapNotFound
from osr2mp4.Utils.HashBeatmap import get_osu
from osr2mp4.Parser import osuparser
import osrparse
from osrparse.enums import Mod
import logging
from abspath import abspath
from config_data import current_config


class Slider(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.setOrientation(QtCore.Qt.Horizontal)

		self.img_handle = os.path.join(abspath, "res/Sliderball2_Scale.png")
		self.img_groove = os.path.join(abspath, "res/Slider_HD.png")
		self.default_width, self.default_height = 250, 20
		self.value_ = 0
		self.setStyleSheet("""
QSlider::groove:horizontal 
{
	image: url(%s);

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
""" % (self.img_groove, self.img_handle))

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

		# print(val)

		self.current_data[self.key] = round(self.value() / 1000, self.precision)

		self.show = round(self.value() / 1000, self.precision)
		if self.show == int(self.show):
			self.show = int(self.show)
		QToolTip.showText(QtGui.QCursor.pos(), str(self.show), self)

	def updatevalue(self):
		self.setValue(self.current_data[self.key] * 1000)

	def enterEvent(self, QEvent):
		self.show = round(self.value() / 1000, self.precision)
		if self.show == int(self.show):
			self.show = int(self.show)
		QToolTip.showText(QtGui.QCursor.pos(), str(self.show), self)


class Map:
	length = None
	name = None


class StartTimeSlider(Slider):

	objs = []

	def __init__(self, parent=None, jsondata=None):
		StartTimeSlider.objs.append(self)
		jsondata["option_config"]["min"] = 0
		jsondata["option_config"]["step"] = 1

		if Map.length is None:
			self.get_maplength(jsondata)

		jsondata["option_config"]["max"] = Map.length

		self.mapname = Map.name

		super().__init__(parent=parent, jsondata=jsondata)

	# @classmethod
	def get_maplength(self, jsondata):
		if Map.name == jsondata["data"]["config"][".osr path"]:
			return
		Map.name = jsondata["data"]["config"][".osr path"]

		try:
			replay_data = osrparse.parse_replay_file(jsondata["data"]["config"][".osr path"])
		except Exception as e:
			logging.error(repr(e))
			Map.length = 1
			Map.name = None
			return

		if Mod.DoubleTime in replay_data.mod_combination or Mod.Nightcore in replay_data.mod_combination:
			time_frame = 1500
		elif Mod.HalfTime in replay_data.mod_combination:
			time_frame = 750
		else:
			time_frame = 1000

		laststring = jsondata["data"]["config"]["Beatmap path"][-1]
		if laststring != "/" and laststring != "\\":
			jsondata["data"]["config"]["Beatmap path"] += "/"

		try:
			mappath = get_osu(jsondata["data"]["config"]["Beatmap path"], replay_data.beatmap_hash)
		except BeatmapNotFound:
			print("replay not specified yet")
			Map.length = 1
			Map.name = None
			return

		color = {"ComboNumber": 1}
		osudata = osuparser.read_file(mappath, 1, color, False)

		Map.length = osudata.hitobjects[-1]["end time"] - osudata.hitobjects[0]["time"]
		Map.length /= time_frame

	# @classmethod
	def updatevalue(self):
		self.get_maplength({"data": {"config": current_config}, "option_config": {}})
		# for self in cls.objs:
		if self.mapname != Map.name:
			self.mapname = Map.name
			self.default_max = Map.length * 1000
			tmp = self.bordersize
			self.bordersize = (self.default_max - self.default_min) * 0.0125
			self.cursize = self.cursize * self.bordersize/tmp

			self.setMaximum(self.default_max + self.cursize)
			self.setMinimum(self.default_min - self.cursize)

			self.current_data[self.key] = 0
			self.setValue(self.minimum())

	# def setFixedHeight(self, p_int):
	# 	super().setFixedHeight(p_int)
	# 	print("from height", self.cursize, self.bordersize)


class EndTimeSlider(StartTimeSlider):
	objs = []

	def __init__(self, parent=None, jsondata=None):
		EndTimeSlider.objs.append(self)
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

	def setFixedHeight(self, p_int):
		super().setFixedHeight(p_int)

	# @classmethod
	def updatevalue(self):
		mapname = self.mapname
		super().updatevalue()
		# for self in cls.objs:
			# if self.current_data[self.key] == -1:
			# 	self.setValue(self.maximum())
		if mapname != Map.name:
			self.current_data[self.key] = -1
			print(self.maximum())
			self.setValue(self.maximum())
