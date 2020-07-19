import os
import sys
from PyQt5.QtWidgets import QLabel

from Parents import ButtonBrowse
from SettingComponents.Components.Textbox import Big_Textbox
from abspath import abspath


class UpdateButton(QLabel):
	def __init__(self, jsondata=None, default_fontsize=1):
		super().__init__()
		self.default_width = 75
		self.default_height = 27
		self.img = os.path.join(abspath, "res/update_HD.png")
		self.default_fontsize = default_fontsize
		self.setFixedWidth(self.default_width)
		self.setFixedWidth(self.default_height)
		self.setStyleSheet("""border-image:url(%s)""" % self.img)

	# def setFixedHeight(self, p_int):
	# 	pass

	def mousePressEvent(self, event):
		fupdate = open("exit.txt", "w")
		fupdate.write("1")
		fupdate.close()
		sys.exit(0)

	def updatevalue(self):
		pass


class SettingsBrowse(ButtonBrowse):
	def __init__(self, parent):
		super().__init__(parent)

		self.default_x = parent.default_width - 60
		self.default_y = parent.default_height * 0.5
		self.default_size = 1

		self.img_idle = "res/Browse.png"
		self.img_hover = "res/Browse hover.png"
		self.img_click = "res/Browse click.png"

		super().setup()

	def afteropenfile(self, filename):
		self.main_window.afteropenfile(filename)
