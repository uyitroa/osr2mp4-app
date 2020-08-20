import logging
import os
import os.path
import sys
import traceback
import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from autologging import TRACE
from urllib.parse import urlparse

from osr2mp4.Utils.getmods import mod_string_to_enums
from osr2mp4.osrparse.replay import Replay

from HomeComponents.AutoCheckBox import AutoCheckBox
from HomeComponents.Buttons.FolderButton import FolderButton
from HomeComponents.Buttons.MapsetButton import MapsetButton
from HomeComponents.Buttons.Options import Options
from HomeComponents.Buttons.OsrButton import OsrButton
from HomeComponents.Buttons.OsrGrayButton import OsrGrayButton
from HomeComponents.Buttons.OutputButton import OutputButton
from HomeComponents.Buttons.StartButton import StartButton
from HomeComponents.Buttons.UpdateButton import UpdateButton
from HomeComponents.Buttons.osuButton import osuButton
from HomeComponents.Buttons.CancelButton import CancelButton
from HomeComponents.Buttons.osuMapButton import osuMapButton
from HomeComponents.LanguageDropDown import LanguageDropDown
from HomeComponents.Logo import Logo
from HomeComponents.PathImage import OsrPath, MapSetPath
from HomeComponents.PopupWindow import PopupWindow, CustomTextWindow
from HomeComponents.ProgressBar import ProgressBar
from HomeComponents.SkinDropDown import SkinDropDown
from Info import Info
from BaseComponents.Buttons import ButtonBrowse, PopupButton
from SettingComponents.Layouts.SettingsPage import SettingsPage
from abspath import abspath, configpath, Log
from config_data import current_config, current_settings
from helper.helper import kill, cleanupkill, get_latest_replay, get_right_map
from helper.osudatahelper import parse_osr, parse_map
from helper.datahelper import save


class Window(QMainWindow):
	def __init__(self, App, execpath):
		super().__init__()

		logging.basicConfig(level=TRACE, filename=Log.apppath, filemode="w",
		                    format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")

		apikey = current_settings["api key"]
		current_settings["api key"] = None  # avoid logging api key
		logging.info("Current settings is updated to: {}".format(current_settings))
		current_settings["api key"] = apikey

		logging.info("Current config is updated to: {}".format(current_config))

		self.setFocus()
		App.applicationStateChanged.connect(self.applicationStateChanged)
		self.setWindowIcon(QtGui.QIcon(os.path.join(abspath, "res/OsrLogo.png")))
		self.setWindowTitle("Osr2mp4")
		self.setStyleSheet("background-color: rgb(30, 30, 33);")
		self.setAcceptDrops(True)

		window_width, window_height = 832, 469

		self.execpath = execpath
		self.minimum_resolution = [640, 360]
		self.previous_resolution = [0, 0]
		self.default_width, self.default_height = window_width, window_height

		self.popup_bool = True
		self.clicked_inside = False
		self.prevreplay = ""

		self.osrbutton = OsrButton(self)
		self.mapsetbutton = MapsetButton(self)
		self.startbutton = StartButton(self)
		self.logo = Logo(self)
		self.osrpath = OsrPath(self)
		self.mapsetpath = MapSetPath(self)
		self.skin_dropdown = SkinDropDown(self)
		self.options = Options(self)
		self.updatebutton = UpdateButton(self)
		self.folderbutton = FolderButton(self)
		self.osrgraybutton = OsrGrayButton(self)
		self.osumapbutton = osuMapButton(self)
		self.autocheckbox = AutoCheckBox(self)
		self.cancelbutton = CancelButton(self)

		logging.info("Loaded Buttons")

		self.blurrable_widgets = [self.osrbutton, self.mapsetbutton, self.startbutton, self.logo, self.osrpath,
		                          self.mapsetpath, self.options, self.skin_dropdown, self.cancelbutton, self.folderbutton, self.autocheckbox]

		self.langs_dropdown = LanguageDropDown(self)
		self.popup_window = PopupWindow(self)
		self.output_window = OutputButton(self)
		self.osu_window = osuButton(self)


		self.customwindow = CustomTextWindow(self)
		self.customwindow.hide()

		logging.info("Loaded Popupwindow output button and osu button")
		self.settingspage = SettingsPage(self)

		logging.info("Loaded settings page")

		self.popup_widgets = [self.popup_window, self.output_window, self.osu_window]

		self.progressbar = ProgressBar(self)
		self.progressbar.hide()

		current_config[".osr path"] = "brrrrr"  # because if .osr path is auto, it won't check for latest play on startup
		self.check_osu_path()
		# self.check_replay_map()

		self.show()
		self.resize(window_width, window_height)

	def toggle_auto(self, enable_auto):
		if enable_auto:
			self.prevreplay = "auto"
			self.setreplay("auto")
			self.setmap("")

			Info.replay = Replay()
			Info.replay.mod_combination = mod_string_to_enums(current_settings["Custom mods"])
			Info.map = None
			Info.maphash = None

			self.osrgraybutton.show()
			self.osrbutton.hide()

			self.mapsetbutton.hide()
			self.osumapbutton.show()
		else:
			self.setreplay("")
			self.setmap("")

			current_settings["Custom mods"] = ""
			current_config[".osr path"] = ""
			current_config["Beatmap path"] = ""
			Info.replay = None
			Info.real_mod = None
			Info.map = None
			Info.maphash = None

			self.check_replay_map()

			self.osrgraybutton.hide()
			self.osrbutton.show()

			self.mapsetbutton.show()
			self.osumapbutton.hide()

	def applicationStateChanged(self, state):
		if ButtonBrowse.browsing or PopupButton.browsing:
			ButtonBrowse.browsing = False
			PopupButton.browsing = False
			return
		if state == 4:
			self.check_replay_map()

	def resizeEvent(self, event):
		height = self.width() * 9 / 16
		self.resize(self.width(), height)
		if self.width() < self.minimum_resolution[0] and self.height() < self.minimum_resolution[1]:
			self.resize(self.previous_resolution[0], self.previous_resolution[1])

		self.osrbutton.changesize()
		self.mapsetbutton.changesize()
		self.startbutton.changesize()
		self.logo.changesize()
		self.osrpath.changesize()
		self.mapsetpath.changesize()
		self.output_window.changesize()
		self.osu_window.changesize()
		self.popup_window.changesize()
		self.skin_dropdown.changesize()
		self.settingspage.changesize()
		self.options.changesize()
		self.progressbar.changesize()
		self.customwindow.changesize()
		self.updatebutton.changesize()
		self.cancelbutton.changesize()
		self.folderbutton.changesize()
		self.autocheckbox.changesize()
		self.osrgraybutton.changesize()
		self.osumapbutton.changesize()
		self.langs_dropdown.changesize()

		if self.popup_bool:
			self.blur_function(True)
		else:
			self.blur_function(False)

		self.previous_resolution[0] = self.width()
		self.previous_resolution[1] = self.height()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.hidesettings()

	def mousePressEvent(self, QMouseEvent):
		self.hidesettings()

	def hidesettings(self):
		if self.settingspage.isVisible():
			self.settingspage.hide()
			self.settingspage.settingsarea.scrollArea.hide()

			save()

		if self.customwindow.isVisible():
			self.customwindow.hide()

	def blur_function(self, blur):
		if blur:
			for x in self.blurrable_widgets:
				x.blur_me(True)
				x.clickable = False
		else:
			for x in self.blurrable_widgets:
				x.blur_me(False)
				x.clickable = True

	def delete_popup(self):
		for x in self.popup_widgets:
			x.setParent(None)

	def check_osu_path(self):
		if os.path.isfile(configpath):
			self.skin_dropdown.get_skins()
			if current_config["Output path"] != "" and current_config["osu! path"] != "":
				self.delete_popup()
				self.popup_bool = False

		if current_config[".osr path"] == "auto":
			current_settings["Custom mods"] = ""

		save()

		if not self.popup_bool:
			self.settingspage.load_settings()
		else:
			self.settingspage.settingsarea.scrollArea.hide()

	def setreplay(self, replay_path):
		if replay_path is None or replay_path == "":
			return

		replay_name = os.path.split(replay_path)[-1]
		self.osrpath.setText(replay_name)

		current_config[".osr path"] = replay_path
		parse_osr(current_config, current_settings)
		logging.info("Updated replay path to: {}".format(replay_path))

	def setmap(self, mapset_path):
		if mapset_path is None or mapset_path == "":
			return
		current_config["Beatmap path"] = mapset_path
		map_name = os.path.split(mapset_path)[-1]
		self.mapsetpath.setText(map_name)

		parse_map(current_config, current_settings)
		logging.info("Updated beatmap path to: {}".format(mapset_path))

	def check_replay_map(self):
		if current_config[".osr path"] == "auto":
			return

		replay = get_latest_replay()
		if self.prevreplay == replay or replay is None:
			return
		self.prevreplay = replay

		self.setreplay(replay)

		mapset = get_right_map(replay)
		if mapset is None:
			return
		self.setmap(mapset)

	def dragEnterEvent(self, e):
		e.accept()

	def dropEvent(self, e):
		for url in e.mimeData().urls():
			p = urlparse(url.url())
			final_path = os.path.abspath(os.path.join(p.netloc, p.path))
			if final_path.endswith(".osr"):
				self.setreplay(final_path)
				mapset = get_right_map(final_path)
				if mapset is not None:
					self.setmap(mapset)

			elif os.path.isdir(final_path):
				self.setmap(final_path)

			elif final_path.endswith(".osu"):
				if current_config[".osr path"] != "auto":
					final_path = os.path.dirname(final_path)
				self.setmap(final_path)


def excepthook(exc_type, exc_value, exc_tb):
	tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
	logging.exception(tb)
	print(tb)
	QApplication.quit()


def main(execpath="."):
	sys.excepthook = excepthook
	floop = open(os.path.join(execpath, "exit.txt"), "w")
	floop.write("0")
	floop.close()

	execpath = os.path.abspath(execpath)

	if not os.path.isdir(os.path.join(execpath, "Logs")):
		os.mkdir(os.path.join(execpath, "Logs"))

	Log.apppath = os.path.join(execpath, "Logs", Log.apppath)
	Log.runosupath = os.path.join(execpath, "Logs", Log.runosupath)

	qtpath = os.path.dirname(PyQt5.__file__)
	pluginpath = os.path.join(qtpath, "Qt/plugins")
	os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = pluginpath

	App = QApplication(sys.argv)
	window = Window(App, execpath)
	b = open(os.path.join(abspath, "progress.txt"), "w")
	b.close()
	watcher = QtCore.QFileSystemWatcher([os.path.join(abspath, 'progress.txt')])
	watcher.directoryChanged.connect(window.progressbar.directory_changed)
	watcher.fileChanged.connect(window.progressbar.file_changed)

	b = open("error.txt", "w")  # remove abspath for temporary fix
	b.close()
	errorwatcher = QtCore.QFileSystemWatcher(['error.txt'])
	errorwatcher.directoryChanged.connect(window.customwindow.directory_changed)
	errorwatcher.fileChanged.connect(window.customwindow.file_changed)

	ret = App.exec_()
	if window.startbutton.proc is not None and window.startbutton.proc.poll() is None:
		kill(window.startbutton.proc.pid)
		cleanupkill()
		with open("progress.txt", "w") as file:
			file.write("done")
		file.close()

	sys.exit(ret)


if __name__ == "__main__":
	main()
