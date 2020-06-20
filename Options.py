from Parents import Button
from Slider import StartTimeSlider, Map, EndTimeSlider
from config_data import current_config


class Options(Button):
	def __init__(self, parent):
		super(Options, self).__init__(parent)

		self.default_x = 20
		self.default_y = 380
		self.default_size = 3.5

		self.img_idle = "res/Options_Idle.png"
		self.img_hover = "res/options_hover.png"
		self.img_click = "res/Options_Click.png"
		self.img_shadow = "res/Options_Shadow.png"
		self.parent = parent
		super().setup()

	def mouseclicked(self):
		StartTimeSlider.updatevalue()
		EndTimeSlider.updatevalue()
		self.parent.settingspage.show()
		self.parent.settingspage.settingsarea.scrollArea.show()
		self.parent.resizeEvent(True)




