import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QGraphicsBlurEffect

from abspath import abspath
from helper.helper import changesize


class AutoCheckBox(QCheckBox):
	def __init__(self, parent):
		super().__init__(parent)

		self.main_window = parent

		self.img_uncheck = os.path.join(abspath, "res/Uncheck_HD.png")
		self.img_check = os.path.join(abspath, "res/Check_HD.png")

		self.box_width = 20
		self.box_height = 20
		self.default_fontsize = 14

		self.default_x = 520
		self.default_y = 145

		self.text = " " + "Use Auto Replay"
		self.setText(self.text)
		self.curfont = self.font()

		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

		self.default_width = self.box_width * 1.1 + self.textwidth()
		self.default_height = self.box_height * 1.1

		self.setCheckState(QtCore.Qt.Unchecked)

		super().stateChanged.connect(self.stateChanged)

	def textwidth(self):
		return self.fontMetrics().boundingRect(self.text).width() * 2

	def textheight(self):
		return self.fontMetrics().boundingRect(self.text).height() * 2

	def changesize(self):
		changesize(self)
		scale = self.main_window.height() / self.main_window.default_height

		self.setStyleSheet("""
		QCheckBox {
			font-weight: bold;
			color: white;
			background-color: transparent;
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

		# super().setFixedWidth(p_int)

	@QtCore.pyqtSlot(int)
	def stateChanged(self, p_int):
		self.main_window.toggle_auto(p_int == 2)

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25)
		else:
			self.blur_effect.setBlurRadius(0)
