import json
import os
from copy import copy
from abspath import configpath, settingspath, pppath, tooltippath
from osr2mp4.global_var import defaultsettings, defaultppconfig

from helper.datahelper import loadsettings

if os.path.isfile(pppath):
	with open(pppath) as f:
		current_ppsettings = json.load(f)
else:
	current_ppsettings = copy(defaultppconfig)

if os.path.isfile(settingspath):
	with open(settingspath) as f:
		current_settings = json.load(f)

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


loadsettings(current_config, current_settings, current_ppsettings)
