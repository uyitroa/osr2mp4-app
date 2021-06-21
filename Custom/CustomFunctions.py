import os
import json


def check_data_paths(app_directory, app):
    data_directory = os.path.join(app_directory, "data/config.json")
    with open(data_directory) as f:
        data = json.load(f)
        if data["osu! path"] == "" or data["Output path"] == "":
            app.get_hidden_popup()

