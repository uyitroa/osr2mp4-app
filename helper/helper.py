import json
import os
from copy import copy

import cv2
from PyQt5 import QtCore
import logging

from abspath import configpath, settingspath


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


def loadname(config):
	from osr2mp4.osrparse import parse_replay_file
	import datetime
	import re

	custom = {}
	custom["Map"] = os.path.basename(os.path.normpath(config["Beatmap path"]))
	try:
		replay = parse_replay_file(config[".osr path"])
		custom["Player"] = replay.player_name
		custom["PlayDate"] = str(replay.timestamp)
		p = (300 * replay.number_300s + 100 * replay.number_100s + 50 * replay.number_50s)
		total = 300 * (replay.number_300s + replay.number_100s + replay.number_50s + replay.misses)
		custom["Accuracy"] = "{:.2f}".format(p / total * 100)
	except Exception as e:
		logging.error(repr(e))
	custom["Date"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	filename = config["Output name"]
	for name in custom:
		template = "{" + name + "}"
		filename = filename.replace(template, custom[name])

	filename = re.sub('[^0-9a-zA-Z.]+', ' ', filename)
	return filename


def save(filename=None):
	from config_data import current_config, current_settings

	if filename is None:
		filename = loadname(current_config)

	config = copy(current_config)
	config["Output path"] = os.path.join(config["Output path"], filename)

	with open(configpath, 'w+') as f:
		json.dump(config, f, indent=4)
		f.close()
	with open(settingspath, 'w+') as f:
		json.dump(current_settings, f, indent=4)
		f.close()


def loadsettings(config, settings, ppsettings):
	outputpath = config["Output path"]

	config["Output name"] = config.get("Output name", "{Player} - {Map} {PlayDate} {Accuracy}.mp4")

	if os.path.isdir(outputpath):
		config["Output path"] = os.path.basename(outputpath)
	else:
		config["Output path"] = os.path.dirname(outputpath)

	ppsettings["Rgb"] = eval(str(ppsettings["Rgb"]))
	ppsettings["Hitresult Rgb"] = eval(str(ppsettings["Hitresult Rgb"]))
