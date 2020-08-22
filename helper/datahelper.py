import json
import logging
import os
from copy import copy
import datetime
import re
from osr2mp4.global_var import defaultsettings, defaultppconfig
from Info import Info
from abspath import configpath, settingspath
from helper.osudatahelper import parse_osr, parse_map


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


def loadname(config):
	custom = {}

	try:
		custom["Map"] = os.path.basename(os.path.normpath(config["Beatmap path"]))
		if Info.map is not None:
			custom["MapTitle"] = Info.map.meta.get("Title", "")
			custom["Artist"] = Info.map.meta.get("Artist", "")
			custom["Creator"] = Info.map.meta.get("Creator", "")
			custom["Difficulty"] = Info.map.meta.get("Version", "")
	except Exception as e:
		logging.error("From loadname map", repr(e))

	try:
		if Info.replay is not None:
			custom["Player"] = Info.replay.player_name
			custom["PlayDate"] = str(Info.replay.timestamp)
			p = (300 * Info.replay.number_300s + 100 * Info.replay.number_100s + 50 * Info.replay.number_50s)
			total = 300 * (Info.replay.number_300s + Info.replay.number_100s + Info.replay.number_50s + Info.replay.misses)
			custom["Accuracy"] = "{:.2f}".format(p / total * 100)
	except Exception as e:
		logging.error("From loadname replay", repr(e))
	custom["Date"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	filename = config["Output name"]
	for name in custom:
		template = "{" + name + "}"
		filename = filename.replace(template, str(custom[name]))

	filename = re.sub('[^0-9a-zA-Z.]+', ' ', filename)
	return filename


def loadsettings(config, settings, ppsettings):
	outputpath = config["Output path"]

	config["Output name"] = config.get("Output name", "{Player} - {Map} {PlayDate} {Accuracy}.mp4")

	config["Audio codec"] = config.get("Audio codec", "aac")

	for key in defaultsettings:
		if key not in settings:
			settings[key] = defaultsettings[key]

	for key in defaultppconfig:
		if key not in ppsettings:
			ppsettings[key] = defaultppconfig[key]

	if os.path.isdir(outputpath):
		config["Output path"] = os.path.basename(outputpath)
	else:
		config["Output path"] = os.path.dirname(outputpath)

	ppsettings["Rgb"] = eval(str(ppsettings["Rgb"]))
	ppsettings["Hitresult Rgb"] = eval(str(ppsettings["Hitresult Rgb"]))

	parse_osr(config, settings)
	parse_map(config, settings)
