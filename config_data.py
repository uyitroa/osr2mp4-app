import json
import os

if os.path.isfile("settings.json"):
	with open('settings.json') as f:
		current_settings = json.load(f)
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
		"Global leaderboard": False,
		"Mods leaderboard": "*",
		"api key": "",
		"Rotate sliderball": False
	}

if os.path.isfile("config.json"):
	with open('config.json') as f:
		current_config = json.load(f)
else:
	current_config = {
		"osu! path": "",
		"Skin path": "",
		"Beatmap path": "",
		".osr path": "",
		"Default skin path": "",
		"Output path": "",
		"Width": 600,
		"Height": 400,
		"FPS": 60,
		"Start time": 0,
		"End time": -1,
		"Video codec": "XVID",
		"Process": 0,
		"ffmpeg path": "ffmpeg"
	}