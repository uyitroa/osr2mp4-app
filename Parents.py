import json
import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsBlurEffect, QPushButton, QFileDialog, QLabel
from pathlib import Path

from autologging import traced, logged

from abspath import abspath, configpath
from config_data import current_config, current_settings
from helper.helper import getsize, changesize, save
from helper.username_parser import get_configInfo, settings_translator
import logging


def get_shadowpos(button, width, height):
	middle_x = button.x() + button.width() / 2
	middle_y = button.y() + button.height() / 2

	shadow_x = middle_x - width / 2
	shadow_y = middle_y - height / 2

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

		self.img_idle = os.path.join(abspath, self.img_idle)
		self.img_hover = os.path.join(abspath, self.img_hover)
		self.img_click = os.path.join(abspath, self.img_click)

		if self.img_shadow is not None:
			self.setup_shadow()
		else:
			self.shadow.setParent(None)
			self.shadow = None

		self.setIcon(QtGui.QIcon(self.img_idle))
		self.setStyleSheet("""
		QPushButton:flat
		{
			border: none;
			background: none;
			outline: none;
		}""")

		imgsize = getsize(self.img_idle)

		self.setMaximumWidth(imgsize[0])
		self.setMaximumHeight(imgsize[1])

		width = self.default_size * imgsize[0] / 10
		height = self.default_size * imgsize[1] / 10

		self.default_width, self.default_height = width, height

		self.setIconSize(QtCore.QSize(width, height))
		self.setGeometry(self.default_x, self.default_y, width, height)
		self.setFlat(True)
		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

	def setup_shadow(self):

		self.img_shadow = os.path.join(abspath, self.img_shadow)

		imgsize = getsize(self.img_shadow)

		width = self.default_size * imgsize[0] / 10 * 1.01
		height = self.default_size * imgsize[1] / 10 * 1.01

		self.default_shadowwidth, self.default_shadowheight = width, height
		self.shadow.setIcon(QtGui.QIcon(self.img_shadow))
		self.shadow.setStyleSheet("""
		QPushButton:flat
		{
			border: none;
			background: none;
                        outline: none;
		}""")
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
		changesize(self)

		if self.shadow is not None:
			scale = self.main_window.height() / self.main_window.default_height
			width = self.default_shadowwidth * scale
			height = self.default_shadowheight * scale
			self.shadow.setIconSize(QtCore.QSize(width, height))
			x, y = get_shadowpos(self, width, height)
			self.shadow.setGeometry(x, y, width, height)


class ButtonBrowse(Button):
	browsing = False

	def __init__(self, parent):
		super(ButtonBrowse, self).__init__(parent)
		self.browsepath = str(Path.home())
		self.file_type = ""

	def mouseclicked(self):
		file_name = ""
		self.browsing = True
		if self.file_type == "Folder":
			file_name = QFileDialog.getExistingDirectory(None, "Select Directory", self.browsepath)
		else:
			file_name = QFileDialog.getOpenFileName(self, 'Open file', self.browsepath,
			                                        "{} files (*{})".format(self.file_type, self.file_type))[0]
		logging.info("Updated: {}".format(current_config))
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
		self.offset = 225

	def setup(self):
		self.img_idle = self.img_hover = self.img_click = self.img
		super().setup()
		self.textblur_effect = QGraphicsBlurEffect()
		self.textblur_effect.setBlurRadius(0)
		self.text.setGraphicsEffect(self.textblur_effect)
	
	def blur_me(self, blur):
		super().blur_me(blur)
		if blur:
			self.textblur_effect.setBlurRadius(10)
		else:
			self.textblur_effect.setBlurRadius(0)

	def setText(self, text):
		# set stylesheet doesnt work for self.text qtoooltip so who cares./. night
		self.text.setToolTip(text)
		self.setToolTip(text)
		# text = text[:57]  # commented cause u ask me to remove. i dont like following ur oders
		self.text.setText(text)
		self.main_window.settingspage.updatevalue()

	def changesize(self):
		super().changesize()

		scale = self.height() / self.main_window.default_height

		x = self.x() + scale * self.offset
		y = self.y() + scale * self.offset

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet(
			"QLabel{font-size: %ipt; font-weight: bold; color: white; background-color: transparent;}QToolTip { background-color:white;color: black; }" % (fontsize))
		self.text.setGeometry(x, y, self.width() * 0.95, self.height() * 0.5)


@logged(logging.getLogger(__name__))
@traced
class PopupButton(ButtonBrowse):
	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return
		if current_config["Output path"] != "" and current_config["osu! path"] != "":
			logging.info("entering output")
			self.main_window.delete_popup()
			self.main_window.popup_bool = False

			self.main_window.check_replay_map()
			self.main_window.resizeEvent(True)

			self.main_window.skin_dropdown.get_configInfo(current_config["osu! path"])
			logging.info(configpath)

			self.main_window.settingspage.load_settings()

			osusettings = get_configInfo(current_config["osu! path"])

			self.set_settings(osusettings)

			save()

			self.main_window.osrbutton.browsepath = os.path.join(current_config["osu! path"], "Replays/")
			self.main_window.mapsetbutton.browsepath = os.path.join(current_config["osu! path"], "Songs/")

	def set_settings(self, osusettings):
		logging.info(f"current settings {current_settings}")
		logging.info(f"osu settings {osusettings}")
		for osukey in osusettings:
			mykey = settings_translator[osukey]
			try:
				setting = float(osusettings[osukey])
			except ValueError:
				setting = osusettings[osukey]

			current_settings[mykey] = setting

		logging.info(f"current settings after set {current_settings}")
