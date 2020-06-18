import json

from Parents import ButtonBrowse
from config_data import current_config, user_data


class OutputButton(ButtonBrowse):
	def __init__(self, parent):
		super(OutputButton, self).__init__(parent)

		self.default_x = 213
		self.default_y = 330
		self.default_size = 3.35
		self.file_type = "Folder"

		self.img_idle = "res/OutputFolder_Idle.png"
		self.img_hover = "res/OutputFolder_Hover.png"
		self.img_click = "res/OutputFolder_Click.png"
		self.parent = parent
		super().setup()

	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return
		current_config["Output path"] = filename

		if current_config["Output path"] != "" and current_config["osu! path"] != "":
			self.main_window.delete_popup()
			self.main_window.popup_bool = False

			user_data["Output path"], user_data["osu! path"] = current_config["Output path"], current_config["osu! path"]
			self.main_window.check_replay_map()
			self.main_window.resizeEvent(True)
			self.main_window.skin_dropdown.get_configInfo(current_config["osu! path"])
			with open('user_data.json', 'w+') as f:
				json.dump(user_data, f, indent=4)
				f.close()
			self.parent.settingspage.load_settings()
