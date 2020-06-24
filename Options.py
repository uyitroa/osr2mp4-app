from Parents import Button
from Slider import StartTimeSlider, Map, EndTimeSlider
from config_data import current_config


class Options(Button):
	def __init__(self, parent):
		super(Options, self).__init__(parent)

		self.default_x = 20
		self.default_y = 360
		self.default_size = 3.5

		self.img_idle = "res/Options_Idle.png"
		self.img_hover = "res/options_hover.png"
		self.img_click = "res/Options_Click.png"
		self.img_shadow = "res/Options_Shadow.png"
		# self.parent = parent
		super().setup()

	def mouseclicked(self):
		self.main_window.settingspage.updatevalue()
		self.main_window.settingspage.show()
		self.main_window.settingspage.settingsarea.scrollArea.show()
		self.main_window.resizeEvent(True)




