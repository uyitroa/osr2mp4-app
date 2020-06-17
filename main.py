from PyQt5.QtWidgets import QMainWindow, QApplication
import os, json, sys, glob, os.path
from Logo import Logo
from MapsetButton import MapsetButton
from OsrButton import OsrButton
from OutputButton import OutputButton
from PathImage import OsrPath, MapSetPath
from PopupWindow import PopupWindow
from SkinDropDown import SkinDropDown
from StartButton import StartButton
from osuButton import osuButton
from find_beatmap import find_beatmap_
from PyQt5 import QtGui
from config_data import current_config
from ProgressBar import ProgressBar
from ScrollArea import Scroll_Class


class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: rgb(30, 30, 33);")

		window_width, window_height = 832, 469

		self.minimum_resolution = [640, 360]
		self.previous_resolution = [0, 0]
		self.default_width, self.default_height = window_width, window_height

		self.popup_bool = True

		self.osrbutton = OsrButton(self)
		self.mapsetbutton = MapsetButton(self)
		self.startbutton = StartButton(self)
		self.logo = Logo(self)
		self.osrpath = OsrPath(self)
		self.progressbar = ProgressBar(self)
		self.mapsetpath = MapSetPath(self)
		self.skin_dropdown = SkinDropDown(self)
		self.blurrable_widgets = [self.osrbutton, self.mapsetbutton, self.startbutton, self.logo, self.osrpath, self.mapsetpath]

		
		self.popup_window = PopupWindow(self)
		self.output_window = OutputButton(self)
		self.osu_window = osuButton(self)
		self.settingspage = Scroll_Class(self)
		
		self.popup_widgets = [self.popup_window, self.output_window, self.osu_window]

		self.check_osuPath()
		self.check_replay_map()
		self.skin_dropdown.raise_()

		self.show()
		self.resize(window_width, window_height)

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

		self.progressbar.changesize()
		if self.popup_bool:
			self.blur_function(True)
		else:
			self.blur_function(False)

		self.previous_resolution[0] = self.width()
		self.previous_resolution[1] = self.height()

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
		if os.path.isfile("user_data.json"):
			with open('user_data.json') as f:
				data = json.load(f)
			current_config["Output path"] = data["Output path"] + "/output.avi"
			current_config["osu! path"] = data["osu! path"]
			self.skin_dropdown.get_configInfo(current_config["osu! path"])
			print("F")
			if data["Output path"] != "" and data["osu! path"] != "":
				self.delete_popup()
				self.popup_bool = False
			print("Data loaded:\n{}\n{}".format(data["Output path"], data["osu! path"]))

	def find_latestReplay(self):
		# current_config["osu! path"] = "/Users/yuitora./Documents/osu!.app/Contents/Resources/drive_c/osu!"
		if current_config["osu! path"] != "":
			path = current_config["osu! path"] + "/Replays/*.osr"
			list_of_files = glob.glob(path)
			replay = max(list_of_files, key=os.path.getctime)
			slash, backslash = replay.rfind("/"), replay.rfind("\\")  # find_lastIndex
			replay_name = replay[max(slash, backslash) + 1:len(replay)]
			self.find_latestMap(replay_name)
			if replay_name != "":
				self.osrpath.setText(replay_name)

			current_config[".osr path"] = replay

	def find_latestMap(self, replay):
		print(replay)
		if current_config["osu! path"] != "":
			beatmap_path = find_beatmap_(current_config["osu! path"] + "/Replays/" + replay,
										 current_config["osu! path"])
			current_config["Beatmap path"] = current_config["osu! path"] + "/Songs/" + beatmap_path
			if beatmap_path != "":
				self.mapsetpath.setText(beatmap_path)

			print(beatmap_path)

	def check_replay_map(self):
		self.find_latestReplay()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
