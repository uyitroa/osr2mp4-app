from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QCheckBox, QPushButton


class CheckBox(QPushButton):
	def __init__(self, jsondata=None):
		super().__init__()

		self.box_width = self.default_box_width = 20
		self.box_height = self.default_box_height = 20
		self.default_fontsize = 14

		self.text = "  " + jsondata["key"]
		self.setText(self.text)
		self.curfont = self.font()

		self.default_width = self.box_width + self.textwidth()
		self.default_height = self.box_height

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		self.img_checked = "res/Check_HD.png"
		self.img_unchecked = "res/Uncheck_HD.png"
		self.setIcon(QtGui.QIcon(self.img_unchecked))
		self.state = bool(self.current_data[self.key])
		self.updateState()

	def textwidth(self):
		return self.fontMetrics().boundingRect(self.text).width()

	def textheight(self):
		return self.fontMetrics().boundingRect(self.text).height()

	def setFixedWidth(self, p_int):
		scale = p_int / self.default_width

		self.curfont.setPointSize(self.default_fontsize * scale)
		self.setFont(self.curfont)

		self.box_width = self.default_box_width * scale
		self.box_height = self.default_box_height * scale
		self.setIconSize(QtCore.QSize(self.box_width, self.box_height))
		# self.setGeometry(QtCore.QRect(0, 0, p_int, self.default_height * scale))
		super().setFixedWidth(p_int)

	def updateState(self):
		if self.state:
			self.setIcon(QtGui.QIcon(self.img_checked))
		else:
			self.setIcon(QtGui.QIcon(self.img_unchecked))

	def mousePressEvent(self, QMouseEvent):
		self.state = (self.state + 1) % 2
		self.current_data[self.key] = bool(self.state)
		self.updateState()
