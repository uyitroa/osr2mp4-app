from Parents import PopupButton
from config_data import current_config


class osuButton(PopupButton):
	def __init__(self, parent):
		super(osuButton, self).__init__(parent)

		self.default_x = 389
		self.default_y = 325
		self.default_size = 3.35
		self.file_type = "Folder"

		self.img_idle = "res/osu!Folder_Idle.png"
		self.img_hover = "res/osu!Folder_Hover.png"
		self.img_click = "res/osu!Folder_Click.png"
		self.parent = parent
		super().setup()

	def afteropenfile(self, filename):
		current_config["osu! path"] = filename
		super().afteropenfile(filename)


