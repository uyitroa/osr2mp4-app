import logging
import os

from osr2mp4 import osrparse
from osr2mp4.Parser import osuparser
from osr2mp4.Utils.HashBeatmap import get_osu
from osr2mp4.Utils.getmods import mod_string_to_enums
from osr2mp4.osrparse.enums import Mod

from Info import Info


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
		if os.path.isdir(config["Beatmap path"]):
			osupath = get_osu(config["Beatmap path"], Info.replay.beatmap_hash)
		else:
			osupath = config["Beatmap path"]
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
		return nomod_time/1000
	except Exception as e:
		logging.error(repr(e))
		return 1
