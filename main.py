import glob
import logging
import os
import os.path
import sys
import traceback

import PyQt5
import psutil
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from autologging import TRACE

from HomeComponents.Buttons.MapsetButton import MapsetButton
from HomeComponents.Buttons.Options import Options
from HomeComponents.Buttons.OsrButton import OsrButton
from HomeComponents.Buttons.OutputButton import OutputButton
from HomeComponents.Buttons.StartButton import StartButton
from HomeComponents.Buttons.UpdateButton import UpdateButton
from HomeComponents.Buttons.osuButton import osuButton
from HomeComponents.Logo import Logo
from HomeComponents.PathImage import OsrPath, MapSetPath
from HomeComponents.PopupWindow import PopupWindow, CustomTextWindow
from HomeComponents.ProgressBar import ProgressBar
from HomeComponents.SkinDropDown import SkinDropDown
from Parents import ButtonBrowse, PopupButton
from SettingComponents.Layouts.SettingsPage import SettingsPage
from abspath import abspath, configpath, Log
from config_data import current_config, current_settings
from helper.find_beatmap import find_beatmap_
from helper.helper import save


class Window(QMainWindow):
	def __init__(self, App, execpath):
		super().__init__()

		logging.basicConfig(level=TRACE, filename=Log.apppath, filemode="w", format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")

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

		logging.info("Loaded Buttons")

		self.blurrable_widgets = [self.osrbutton, self.mapsetbutton, self.startbutton, self.logo, self.osrpath,
								  self.mapsetpath, self.options, self.skin_dropdown]

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

		self.check_osuPath()
		# self.check_replay_map()

		self.show()
		self.resize(window_width, window_height)
	def on_focusChanged(self):
		if ButtonBrowse.browsing or PopupButton.browsing:
			ButtonBrowse.browsing = False
			PopupButton.browsing = False
			return
		if self.isActiveWindow():
			self.check_replay_map()
			print("Checking latest map")

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

	def check_osuPath(self):
		if os.path.isfile(configpath):
			self.skin_dropdown.get_configInfo(current_config["osu! path"])
			if current_config["Output path"] != "" and current_config["osu! path"] != "":
				self.delete_popup()
				self.popup_bool = False

		save()

		if not self.popup_bool:
			self.settingspage.load_settings()
		else:
			self.settingspage.settingsarea.scrollArea.hide()

	def find_latestReplay(self):
		try:
			if current_config["osu! path"] != "":
				path = os.path.join(current_config["osu! path"], "Replays/*.osr")
				list_of_files = glob.glob(path)
				if not list_of_files:
					return
				replay = max(list_of_files, key=os.path.getctime)
				if self.prevreplay == replay:
					return

				self.prevreplay = replay
				replay_name = os.path.split(replay)[-1]
				self.find_latestMap(replay)
				if replay_name != "":
					self.osrpath.setText(replay_name)

				current_config[".osr path"] = replay
				logging.info("Updated replay path to: {}".format(replay))
		except Exception as e:
			print("Error: {}".format(e))
			logging.error(repr(e))

	def find_latestMap(self, replay):

		if current_config["osu! path"] != "":
			beatmap_path = find_beatmap_(replay, current_config["osu! path"])
			current_config["Beatmap path"] = os.path.join(current_config["osu! path"], "Songs", beatmap_path)
			if beatmap_path != "":
				self.mapsetpath.setText(beatmap_path)
				print("press F")
				logging.info("Updated beatmap path to: {}".format(beatmap_path))

	def check_replay_map(self):
		self.find_latestReplay()


def kill(proc_pid):
	process = psutil.Process(proc_pid)
	for proc in process.children(recursive=True):
		proc.kill()
	process.kill()


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

	print(Log.apppath, Log.runosupath)

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

	sys.exit(ret)


if __name__ == "__main__":
	main()

