import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox

from abspath import abspath


class CheckBox(QCheckBox):
	def __init__(self, jsondata=None):
		super().__init__()

		self.img_uncheck = os.path.join(abspath, "res/Uncheck_HD.png")
		self.img_check = os.path.join(abspath, "res/Check_HD.png")

		self.box_width = 20
		self.box_height = 20
		self.default_fontsize = 14

		self.text = "  " + jsondata["key"] + "     "
		self.setText(self.text)
		self.curfont = self.font()

		self.default_width = self.box_width * 1.1 + self.textwidth()
		self.default_height = self.box_height * 1.1

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		if bool(self.current_data[self.key]):
			self.setCheckState(QtCore.Qt.Checked)
		else:
			self.setCheckState(QtCore.Qt.Unchecked)

		super().stateChanged.connect(self.stateChanged)

	def textwidth(self):
		return self.fontMetrics().boundingRect(self.text).width() * 2

	def textheight(self):
		return self.fontMetrics().boundingRect(self.text).height() * 2

	def updatevalue(self):
		if bool(self.current_data[self.key]):
			self.setCheckState(QtCore.Qt.Checked)
		else:
			self.setCheckState(QtCore.Qt.Unchecked)

	def setFixedWidth(self, p_int):
		scale = p_int / self.default_width

		self.setStyleSheet("""
		QCheckBox {
			font-weight: bold;
			color: white;
		}
		QCheckBox::indicator {
		    width: %fpx;
		    height: %fpx;
		}
		QCheckBox::indicator:unchecked {
		    border-image: url(%s);
		}
		QCheckBox::indicator:checked {
		    border-image: url(%s);
		}
					""" % (self.box_width * scale, self.box_height * scale, self.img_uncheck, self.img_check))

		self.curfont.setPointSize(self.default_fontsize * scale)
		self.setFont(self.curfont)

		super().setFixedWidth(p_int)


	@QtCore.pyqtSlot(int)
	def stateChanged(self, p_int):
		if p_int == 2:
			self.current_data[self.key] = True
		else:
			self.current_data[self.key] = False
