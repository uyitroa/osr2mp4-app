import json

from Parents import ButtonBrowse
from config_data import current_config, user_data


class osuButton(ButtonBrowse):
	def __init__(self, parent):
		super(osuButton, self).__init__(parent)

		self.default_x = 400
		self.default_y = 85
		self.default_size = 3.35
		self.file_type = "Folder"

		self.img_idle = "res/osu!Folder_Idle.png"
		self.img_hover = "res/osu!Folder_Hover.png"
		self.img_click = "res/osu!Folder_Click.png"

		super().setup()

	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return
		current_config["osu! path"] = filename

		if current_config["Output path"] != "" and current_config["osu! path"] != "":
			self.main_window.delete_popup()
			self.main_window.popup_bool = False

			user_data["Output path"], user_data["osu! path"] = current_config["Output path"], current_config[
				"osu! path"]
			self.main_window.check_replay_map()
			self.main_window.resizeEvent(True)
			self.main_window.skin_dropdown.get_configInfo(current_config["osu! path"])
			with open('user_data.json', 'w+') as f:
				json.dump(user_data, f, indent=4)
				f.close()
