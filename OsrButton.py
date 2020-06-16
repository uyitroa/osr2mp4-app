from Parents import ButtonBrowse
from config_data import current_config


class OsrButton(ButtonBrowse):
	def __init__(self, parent):
		super(OsrButton, self).__init__(parent)

		self.default_x = 490
		self.default_y = 30
		self.default_size = 3.5
		self.file_type = ".osr"

		self.img_idle = "res/B1_Idle.png"
		self.img_hover = "res/B1_Hover.png"
		self.img_click = "res/B1_Click.png"
		self.img_shadow = "res/B1_Shadow.png"

		super().setup()

	def afteropenfile(self, filename):
		if filename == "":  # if user cancel select
			return
		current_config[".osr path"] = filename

		try:
			self.main_window.find_latestMap(filename)
		except:
			pass
