import json
import os
from copy import copy

from abspath import configpath, settingspath, pppath
# import logging
from osr2mp4.global_var import defaultsettings, defaultppconfig

from helper.helper import loadsettings

if os.path.isfile(pppath):
	with open(pppath) as f:
		current_ppsettings = json.load(f)
	for key in defaultppconfig:
		if key not in current_ppsettings:
			current_ppsettings[key] = defaultppconfig[key]
else:
	current_ppsettings = copy(defaultppconfig)

if os.path.isfile(settingspath):
	with open(settingspath) as f:
		current_settings = json.load(f)

	for key in defaultsettings:
		if key not in current_settings:
			current_settings[key] = defaultsettings[key]

else:
	current_settings = copy(defaultsettings)

if os.path.isfile(configpath):
	with open(configpath) as f:
		current_config = json.load(f)
	outputpath = current_config["Output path"]

else:
	current_config = {
		"osu! path": "",
		"Skin path": "",
		"Beatmap path": "",
		".osr path": "",
		"Default skin path": "",
		"Output path": "",
		"Output name": "",
		"Width": 1280,
		"Height": 720,
		"FPS": 60,
		"Start time": 0,
		"End time": -1,
		"Video codec": "XVID",
		"Process": 2,
		"ffmpeg path": "ffmpeg"
	}
	# logging.info("Current config is set to default")

loadsettings(current_config, current_settings, current_ppsettings)
