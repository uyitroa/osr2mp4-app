from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsBlurEffect, QPushButton, QFileDialog, QLabel
from pathlib import Path
import cv2


def getsize(img):
	a = cv2.imread(img, -1)
	return a.shape[1]/10, a.shape[0]/10


def get_shadowpos(button, width, height):
	middle_x = button.x() + button.width()/2
	middle_y = button.y() + button.height()/2

	shadow_x = middle_x - width/2
	shadow_y = middle_y - height/2

	return shadow_x, shadow_y


class Button(QPushButton):
	def __init__(self, parent):
		self.main_window = parent
		self.shadow = QPushButton(self.main_window)
		super(Button, self).__init__(parent)

		self.blur_effect = None
		self.clickable = True
		self.default_width, self.default_height = None, None
		self.default_shadowwidth, self.default_shadowheight = None, None
		self.img_shadow = None

	def setup(self):

		if self.img_shadow is not None:
			self.setup_shadow()
		else:
			self.shadow.setParent(None)
			self.shadow = None

		self.setIcon(QtGui.QIcon(self.img_idle))

		imgsize = getsize(self.img_idle)

		width = self.default_size * imgsize[0]
		height = self.default_size * imgsize[1]

		self.default_width, self.default_height = width, height

		self.setIconSize(QtCore.QSize(width, height))
		self.setGeometry(self.default_x, self.default_y, width, height)
		self.setFlat(True)


		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

	def setup_shadow(self):
		imgsize = getsize(self.img_shadow)

		width = self.default_size * imgsize[0] * 1.01
		height = self.default_size * imgsize[1] * 1.01

		self.default_shadowwidth, self.default_shadowheight = width, height
		self.shadow.setIcon(QtGui.QIcon(self.img_shadow))
		self.shadow.setIconSize(QtCore.QSize(width, height))
		x, y = get_shadowpos(self, width, height)
		self.shadow.setGeometry(x, y, width, height)
		self.shadow.setFlat(True)

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25)
		else:
			self.blur_effect.setBlurRadius(0)

	def mousePressEvent(self, QEvent):
		if self.clickable:
			self.setIcon(QtGui.QIcon(self.img_click))

	def mouseReleaseEvent(self, QEvent):
		if self.clickable:
			self.mouseclicked()
			self.setIcon(QtGui.QIcon(self.img_idle))

	def enterEvent(self, QEvent):
		if self.clickable:
			self.setIcon(QtGui.QIcon(self.img_hover))

	def leaveEvent(self, QEvent):
		self.setIcon(QtGui.QIcon(self.img_idle))

	def mouseclicked(self):
		pass

	def setParent(self, parent):
		super().setParent(parent)
		if self.shadow is not None:
			self.shadow.setParent(parent)

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		x = self.default_x * scale
		y = self.default_y * scale

		width = self.default_width * scale
		height = self.default_height * scale

		self.setIconSize(QtCore.QSize(width, height))
		self.setGeometry(x, y, width, height)

		if self.shadow is not None:
			width = self.default_shadowwidth * scale
			height = self.default_shadowheight * scale
			self.shadow.setIconSize(QtCore.QSize(width, height))
			x, y = get_shadowpos(self, width, height)
			self.shadow.setGeometry(x, y, width, height)


class ButtonBrowse(Button):
	def __init__(self, parent):
		super(ButtonBrowse, self).__init__(parent)

	def mouseclicked(self):
		file_name = ""
		if self.file_type == "Folder":
			home_dir = str(Path.home())
			file_name = QFileDialog.getExistingDirectory(None, "Select Directory", home_dir)
		else:
			home_dir = str(Path.home())
			file_name = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type, self.file_type))[0]

		self.afteropenfile(file_name)

	def afteropenfile(self, filename):
		pass


class PathImage(Button):
	def __init__(self, parent):
		super(PathImage, self).__init__(parent)
		self.img_idle = self.img_hover = self.img_click = None
		self.text = QLabel(parent)
		self.text.setText("")
		self.default_fontsize = 150

		self.offset = 115

	def setup(self):
		self.img_idle = self.img_hover = self.img_click = self.img

		super().setup()

	def setText(self, text):
		text = text[:45]  # max 45 characters
		self.text.setText(text)

	def changesize(self):
		super().changesize()

		scale = self.height()/self.main_window.default_height

		x = self.x() + scale * self.offset
		y = self.y() + scale * self.offset

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("font-size: {}pt; font-weight: bold; color: white; background-color: rgba(0,0,0,0%)".format(fontsize))
		self.text.setGeometry(x, y, self.width(), self.height())

