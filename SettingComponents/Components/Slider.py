import os

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QSlider, QToolTip
from PyQt5 import QtCore
from PyQt5 import QtGui
from abspath import abspath
from config_data import current_config, current_settings
from helper.osudatahelper import ensure_rightmap, osrhash, getmaptime


class Slider(QSlider):
	def __init__(self, key=None, jsondata=None, datadict=None):
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

		self.default_min = jsondata["min"] * 1000
		self.default_max = jsondata["max"] * 1000

		self.bordersize = self.cursize = (self.default_max - self.default_min) * 0.0125

		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)

		self.setMinimum(self.default_min - self.bordersize)
		self.setMaximum(self.default_max + self.bordersize)
		self.setSingleStep(jsondata["step"] * 1000)

		self.jsondata = jsondata

		step = jsondata["step"]
		self.precision = len(str(step-int(step))[1:])

		self.key = key
		if datadict is not None:
			self.current_data = datadict
		else:
			if self.key in current_config:
				self.current_data = current_config
			else:
				self.current_data = current_settings

		if self.key not in self.current_data:
			self.current_data[self.key] = 0

		self.mousemove = False

		super().valueChanged.connect(self.valueChanged)
		self.setValue(self.current_data[self.key] * 1000)
		self.show = str(self.current_data[self.key])

		self.installEventFilter(self)

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

		self.show = self.current_data[self.key]
		if self.show == int(self.show):
			self.show = int(self.show)

		if self.mousemove:
			QToolTip.showText(QtGui.QCursor.pos(), str(self.show), self)
		self.mousemove = False

	def updatevalue(self):
		self.setValue(self.current_data[self.key] * 1000)

	def enterEvent(self, event):
		QToolTip.showText(QtGui.QCursor.pos(), str(self.show), self)

	def eventFilter(self, object, event):
		if event.type() == QEvent.MouseMove:
			self.mousemove = True
		return False


class StartTimeSlider(Slider):

	objs = []

	def __init__(self, key=None, jsondata=None):
		StartTimeSlider.objs.append(self)
		jsondata["min"] = 0
		jsondata["step"] = 1

		ensure_rightmap(current_config, current_settings)
		self.prevhash = osrhash()

		jsondata["max"] = getmaptime(current_config, current_settings)

		super().__init__(key=key, jsondata=jsondata)

	def updatevalue(self):
		ensure_rightmap(current_config, current_settings)
		if self.prevhash != osrhash():
			self.updatetime()

	def updatetime(self):
		self.prevhash = osrhash()
		self.jsondata["max"] = getmaptime(current_config, current_settings)
		self.default_max = self.jsondata["max"] * 1000
		tmp = self.bordersize
		self.bordersize = (self.default_max - self.default_min) * 0.0125
		self.cursize = self.cursize * self.bordersize / tmp
		self.setMaximum(self.default_max + self.cursize)
		self.setMinimum(self.default_min - self.cursize)
		self.current_data[self.key] = 0
		self.setValue(self.minimum())


class EndTimeSlider(StartTimeSlider):
	objs = []

	def __init__(self, key=None, jsondata=None):
		EndTimeSlider.objs.append(self)
		end_time = current_config["End time"]
		super().__init__(key=key, jsondata=jsondata)
		if end_time == -1:
			val = self.maximum()
		else:
			val = self.current_data[self.key]
		self.setValue(val)

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		super().valueChanged(p_int)
		if p_int >= self.maximum() - self.cursize:
			self.current_data[self.key] = -1
			self.show = "Max"

	def setFixedHeight(self, p_int):
		super().setFixedHeight(p_int)

	def updatevalue(self):
		prevhash = self.prevhash
		super().updatevalue()
		if prevhash != self.prevhash:
			self.updateendtime()

	def updateendtime(self):
		self.current_data[self.key] = -1
		self.setValue(self.maximum())

	def enterEvent(self, QEvent):
		self.show = self.current_data[self.key]
		if self.show == int(self.show):
			self.show = int(self.show)

		if self.show == -1:
			self.show = "Max"
		QToolTip.showText(QtGui.QCursor.pos(), str(self.show), self)
