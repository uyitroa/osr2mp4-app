import glob
import json
import os
import shutil
from copy import copy
import cv2
import psutil
from PyQt5 import QtCore
import logging
from osr2mp4 import osrparse
from osr2mp4.Parser import osuparser
from osr2mp4.Utils.HashBeatmap import get_osu
from osr2mp4.Utils.getmods import mod_string_to_enums
from osr2mp4.osrparse.enums import Mod

from abspath import configpath, settingspath
from Info import Info


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

	api = current_settings["api key"]
	current_settings["api key"] = None
	logging.info(config)
	logging.info(current_settings)
	current_settings["api key"] = api

	with open(configpath, 'w+') as f:
		json.dump(config, f, indent=4)
		f.close()
	with open(settingspath, 'w+') as f:
		json.dump(current_settings, f, indent=4)
		f.close()


def parse_osr(config, settings):
	try:
		logging.info(config[".osr path"])
		Info.replay = osrparse.parse_replay_file(config[".osr path"])
		Info.real_mod = Info.replay.mod_combination
		if settings["Custom mods"] != "":
			Info.replay.mod_combination = mod_string_to_enums(settings["Custom mods"])

		return True
	except Exception as e:
		logging.error(repr(e))
		return False


def parse_map(config, settings):
	try:
		logging.info(config["Beatmap path"])
		osupath = get_osu(config["Beatmap path"], Info.replay.beatmap_hash)

		logging.info(osupath)
		return parse_osu(osupath)
	except Exception as e:
		logging.error(repr(e))
		return False


def parse_osu(osupath):
	try:
		Info.map = osuparser.read_file(osupath)
		Info.maphash = Info.replay.beatmap_hash
		return True
	except Exception as e:
		logging.error(repr(e))
		return False


def ensure_rightmap(config, settings):
	t = Info.replay is not None
	if not t:
		t = parse_osr(config, settings)

	wrongmap = Info.replay is not None and Info.replay.beatmap_hash != Info.maphash
	if Info.map is None or wrongmap:
		t = parse_map(config, settings) and t
	return t


def osrhash():
	return str(Info.maphash) + str(Info.map)


def getmaptime(config, settings):
	ensure_rightmap(config, settings)
	try:
		nomod_time = Info.map.end_time - Info.map.start_time

		if Mod.DoubleTime in Info.replay.mod_combination or Mod.Nightcore in Info.replay.mod_combination:
			nomod_time /= 1.5

		if Mod.HalfTime in Info.replay.mod_combination:
			nomod_time /= 0.75

		return nomod_time
	except Exception as e:
		logging.error(repr(e))
		return 1


def loadsettings(config, settings, ppsettings):
	outputpath = config["Output path"]

	config["Output name"] = config.get("Output name", "{Player} - {Map} {PlayDate} {Accuracy}.mp4")

	if os.path.isdir(outputpath):
		config["Output path"] = os.path.basename(outputpath)
	else:
		config["Output path"] = os.path.dirname(outputpath)

	ppsettings["Rgb"] = eval(str(ppsettings["Rgb"]))
	ppsettings["Hitresult Rgb"] = eval(str(ppsettings["Hitresult Rgb"]))

	parse_osr(config, settings)
	parse_map(config, settings)


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