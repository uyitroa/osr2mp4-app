import logging
from data.Info import Info
from osr2mp4 import osrparse
from osr2mp4.Parser import osuparser
from osr2mp4.Utils.HashBeatmap import get_osu

import os

def parse_osr(config, settings=None):
	try:
		logging.info(config[".osr path"])
		Info.replay = osrparse.parse_replay_file(config[".osr path"])
		#Info.real_mod = Info.replay.mod_combination
		#if settings["Custom mods"] != "":
			#Info.replay.mod_combination = mod_string_to_enums(settings["Custom mods"])

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