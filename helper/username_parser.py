import glob
import configparser
import logging

settings_translator = {
	"CursorSize": "Cursor size",
	"ShowInterface": "In-game interface",
	"ScoreboardVisible": "Show scoreboard",
	"DimLevel": "Background dim",
	"KeyOverlay": "Always show key overlay",
	"AutomaticCursorSizing": "Automatic cursor size",
	"ScoreMeterScale": "Score meter size",
	"VolumeMusic": "Song volume",
	"VolumeEffect": "Effect volume",
	"IgnoreBeatmapSamples": "Ignore beatmap hitsounds",
	"SkinSamples": "Use skin's sound samples"
}


def read_properties_file(file_path):
	with open(file_path, encoding="utf-8") as f:
		config = "[dummy_section]\n#" + f.read().replace('%', '%%')
		cp = configparser.SafeConfigParser()
		cp.read_string(config)

		return dict(cp.items('dummy_section'))


def get_configInfo(path):
	try:
		settings_result = {}
		if path != "":
			c = glob.glob(path + "/*.cfg")
			logging.info(c)
			if not c:
				raise Exception
			cfg = [x for x in c if "osu!.cfg" not in x]
			logging.info(f"cfg {cfg}")
			props = read_properties_file(cfg[0])
			for x in settings_translator:
				settings_result[x] = props[x.lower()]
		return settings_result
	except Exception as e:
		logging.error(repr(e))
		return {
			"CursorSize": 1,
			"ShowInterface": 1,
			"ScoreboardVisible": 1,
			"DimLevel": 100.0,
			"KeyOverlay": 1,
			"AutomaticCursorSizing": 0,
			"ScoreMeterScale": 1,
			"VolumeMusic": 100,
			"VolumeEffect": 100,
			"IgnoreBeatmapSamples": 0,
			"SkinSamples": 1
		}
