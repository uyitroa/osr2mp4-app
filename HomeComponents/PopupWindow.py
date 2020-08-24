from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit, QFrame, QLabel
from PyQt5 import QtCore
from BaseComponents.Buttons import Button


class PopupWindow(Button):
	def __init__(self, parent):
		super(PopupWindow, self).__init__(parent)

		self.default_x = 150
		self.default_y = 70
		self.default_size = 3.5

		self.default_fontsize = 24
		self.text_x = 20
		self.text_y = -30

		self.img_idle = "res/Window.png"
		self.img_hover = "res/Window.png"
		self.img_click = "res/Window.png"
		self.img_shadow = "res/Window_Shadow.png"

		self.setup = self.main_window.langs_dropdown.getlang_popupwindow()

		self.text = QLabel(self)
		self.text.setText(self.setup["Setup"])
		self.text.setFont(QFont('Tahoma'))
		self.text.setStyleSheet("QLabel{background: transparent; color: white}")
		self.text.setAlignment(QtCore.Qt.AlignCenter)

		super().setup()

	def reload_popupwindow(self):
		setup = self.main_window.langs_dropdown.getlang_popupwindow()
		self.text.setText(setup["Setup"])

	def changesize(self):
		super().changesize()
		scale = self.height()/self.main_window.default_height

		x = scale * self.text_x
		y = scale * self.text_y

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("font-size: {}pt; color: white; background-color: rgba(0,0,0,0%)".format(fontsize))
		self.text.setGeometry(x, y, int(self.width() * 0.95), int(self.height() * 0.9))


class CustomTextWindow(Button):
	def __init__(self, parent):
		super(CustomTextWindow, self).__init__(parent)

		self.default_x = 10
		self.default_y = 50
		self.default_size = 3

		self.default_fontsize = 30
		self.text_x = 30
		self.text_y = 10

		self.img_idle = "res/WindowShadow.png"
		self.img_hover = "res/WindowShadow.png"
		self.img_click = "res/WindowShadow.png"

		self.text = QTextEdit(self)
		self.text.setText("")
		self.text.setReadOnly(True)
		self.text.setFrameStyle(QFrame.NoFrame)

		super().setup()

	def directory_changed(self, filename):
		pass

	def file_changed(self, filename):
		fopen = open(filename, "r")
		self.text.setText(str(fopen.read()))
		self.show()
		fopen.close()
		self.main_window.progressbar.hide()

	def changesize(self):
		super().changesize()
		scale = self.height()/self.main_window.default_height

		x = scale * self.text_x
		y = scale * self.text_y

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("font-size: {}pt; font-weight: bold; color: white; background-color: rgba(0,0,0,0%)".format(fontsize))
		self.text.setGeometry(x, y, int(self.width() * 0.95), int(self.height() * 0.9))
