import os
import json
import logging
import glob
import re

def check_data_paths(app_directory, app):
    data_directory = os.path.join(app_directory, "data/config.json")
    with open(data_directory) as f:
        data = json.load(f)
        if data["osu! path"] == "" or data["Output path"] == "":
            app.show_popups()


def get_latest_replay():
    try:
        #if current_config["osu! path"] == "":
            #return

        path = r"D:/Games/osu!/Replays/*.osr"
        list_of_files = glob.glob(path)
        if not list_of_files:
            return
        path = max(list_of_files, key=os.path.getctime)
        path = path_parser(path)
        return path
    # if prevreplay == replay or current_config[".osr path"] == "auto":
    # 	return prevreplay

    except Exception as e:
        print("Error: {}".format(e))
        logging.error(repr(e))
        return None


def get_right_map(replay):
    try:
        if current_config["osu! path"] == "":
            return

        beatmap_name = find_beatmap_(replay, current_config["osu! path"])
        beatmap_path = os.path.join(current_config["osu! path"], "Songs", beatmap_name)

        if not os.path.isdir(beatmap_path):
            return None

        return beatmap_path

    except Exception as e:
        print("Error: {}".format(e))
        logging.error(repr(e))
        return None


def path_parser(path):
    path = path.replace('\\', '/')
    splitted_path = re.split('/', path)
    return splitted_path[len(splitted_path)-1]

