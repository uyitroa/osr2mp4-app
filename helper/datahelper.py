import json
import logging
import os
from copy import copy

from osr2mp4.global_var import defaultsettings, defaultppconfig

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
