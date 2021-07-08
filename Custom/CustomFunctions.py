import os
import json
import logging
import glob
import re
from Custom.BeatmapParser import find_beatmap

def check_data_paths(app):
    logging.info("Checking data paths existence")
    data_directory = os.path.join(app.app_directory, "data/config.json")
    with open(data_directory, 'r') as f:
        data = json.load(f)
        if data["osu! path"] == "" or data["Output path"] == "":
            app.show_popups()
        else:
            app.popupable_bool = False


def get_latest_replay(current_config):
    logging.info("Getting latest replay")
    try:
        if current_config["osu! path"] == "":
            print("Error: The current osu! path is wrong")
            logging.error("Error: The current osu! path is wrong")
            return
        path = current_config["osu! path"] + "/Replays/*.osr"
        list_of_files = glob.glob(path)
        if not list_of_files:
            return
        path = max(list_of_files, key=os.path.getctime)
        current_config[".osr path"] = path
        path = path_parser(path)
        beatmap_name = get_beatmap(current_config, current_config["osu! path"] + "/Replays/" + path)
        return path, beatmap_name
    # if prevreplay == replay or current_config[".osr path"] == "auto":
    # 	return prevreplay

    except Exception as e:
        print("Error: {}".format(e))
        logging.error(repr(e))
        return None


def get_beatmap(current_config, replay):
    logging.info("Getting beatmap path from replay: {}".format(replay))
    try:
        if current_config["osu! path"] == "":
            print("Error: The current osu! path is wrong")
            logging.error("Error: The current osu! path is wrong")
            return
        beatmap_name = find_beatmap(replay, current_config["osu! path"])
        beatmap_path = os.path.join(current_config["osu! path"], "Songs", beatmap_name)
        #app.map_path.text.setText(beatmap_name)
        if not os.path.isdir(beatmap_path):
            return None
        current_config["Beatmap path"] = beatmap_path
        return beatmap_name

    except Exception as e:
        print("Error: {}".format(e))
        logging.error(repr(e))
        return None


def path_parser(path):
    path = path.replace('\\', '/')
    splitted_path = re.split('/', path)
    return splitted_path[len(splitted_path)-1]

