import glob
import os
import shutil
import cv2
import psutil
from PyQt5 import QtCore
import logging
from config_data import current_config
from helper.find_beatmap import find_beatmap_


def getsize(img):
	a = cv2.imread(img, -1)
	logging.info("Image loaded: {}".format(img))
	return a.shape[1], a.shape[0]


def changesize(widget):
	scale = widget.main_window.height() / widget.main_window.default_height

	x = widget.default_x * scale
	y = widget.default_y * scale

	width = widget.default_width * scale
	height = widget.default_height * scale

	widget.setIconSize(QtCore.QSize(width, height))
	widget.setGeometry(x, y, width, height)


def kill(proc_pid):
	process = psutil.Process(proc_pid)
	for proc in process.children(recursive=True):
		proc.kill()
	process.kill()


def cleanupkill():
	import osr2mp4
	osr2mp4dir = os.path.dirname(osr2mp4.__file__)
	to_deletes = glob.glob(os.path.join(osr2mp4dir, "*temp"))
	for folder in to_deletes:
		shutil.rmtree(folder, ignore_errors=True)


def get_latest_replay():
	try:
		if current_config["osu! path"] == "":
			return

		path = os.path.join(current_config["osu! path"], "Replays/*.osr")
		list_of_files = glob.glob(path)
		if not list_of_files:
			return
		return max(list_of_files, key=os.path.getctime)
		# if prevreplay == replay or current_config[".osr path"] == "auto":
		# 	return prevreplay

	except Exception as e:
		print("Error: {}".format(e))
		logging.error(repr(e))
		return None


def get_right_map(replay):
	try:
		if current_config["osu! path"] == "":
			return

		beatmap_name = find_beatmap_(replay, current_config["osu! path"])
		beatmap_path = os.path.join(current_config["osu! path"], "Songs", beatmap_name)

		if not os.path.isdir(beatmap_path):
			return None

		return beatmap_path

	except Exception as e:
		print("Error: {}".format(e))
		logging.error(repr(e))
		return None
