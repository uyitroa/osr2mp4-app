import json
import os
from abspath import abspath, configpath, settingspath
# import logging


if os.path.isfile(settingspath):
	with open(settingspath) as f:
		current_settings = json.load(f)
		# logging.info("Current settings is updated to: {}".format(current_settings))
else:
	current_settings = {
		"Cursor size": 1.0,
		"In-game interface": 1.0,
		"Show scoreboard": 1.0,
		"Background dim": 100.0,
		"Always show key overlay": 1.0,
		"Automatic cursor size": 0.0,
		"Score meter size": 1.28,
		"Song volume": 100.0,
		"Effect volume": 85.0,
		"Ignore beatmap hitsounds": 0.0,
		"Use skin's sound samples": 1.0,
		"Global leaderboard": 0,
		"Mods leaderboard": "*",
		"api key": "",
		"Rotate sliderball": 0
	}
	# logging.info("Current settings is set to default")

if os.path.isfile(configpath):
	with open(configpath) as f:
		current_config = json.load(f)
		# logging.info("Current config is updated to: {}".format(current_settings))
else:
	current_config = {
		"osu! path": "",
		"Skin path": "",
		"Beatmap path": "",
		".osr path": "",
		"Default skin path": "",
		"Output path": "",
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
