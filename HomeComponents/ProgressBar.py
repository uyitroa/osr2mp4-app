import os

from PyQt5 import QtCore
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QProgressBar

from abspath import abspath


class ProgressBar(QProgressBar):
	def __init__(self, parent):
		super(ProgressBar, self).__init__(parent)
		self.main_window = parent

		self.default_x = 0
		self.default_y = 420
		self.default_width = 830
		self.default_height = 40
		self.notification = {"done": QSound(os.path.join(abspath, "res/success.wav")),
							"error": QSound(os.path.join(abspath, "res/fail.wav")),
							".": QSound("blank")}

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)

		self.setAlignment(QtCore.Qt.AlignCenter)

		self.setStyleSheet("""
QProgressBar {
	border: 2px solid white;
	border-radius: 5px;
	color:white;	
}

QProgressBar::chunk {
	background-color: rgba(226, 107, 167, 255);
}""")

	def directory_changed(self, path):
		print('Directory Changed:', path)

	def file_changed(self, path):
		f = open(path, "r")
		content = f.read()
		if content in self.notification:
			self.notification[content].play()
			self.hide()
			self.setValue(0)
			return

		self.setValue(max(self.value(), float("0" + content)))
		f.close()
		# if self.value() >= 100:
		# 	self.hide()
		# 	self.setValue(0)

	def hide(self):
		self.main_window.startbutton.default_y = 370
		self.main_window.startbutton.show()
		self.main_window.cancelbutton.hide()
		self.main_window.options.default_y = 430
		self.main_window.updatebutton.default_y = 400
		self.main_window.resizeEvent(True)
		super().hide()

	def show(self):
		self.main_window.startbutton.default_y = 330
		self.main_window.options.default_y = 390
		self.main_window.updatebutton.default_y = 360
		self.main_window.resizeEvent(True)
		self.main_window.startbutton.hide()
		self.main_window.cancelbutton.show()
		super().show()

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height
		width = self.default_width * scale
		height = self.default_height * scale
		x = self.default_x * scale
		y = self.default_y * scale

		self.setGeometry(x, y, width, height)
