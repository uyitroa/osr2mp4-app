from Parents import Button
from ScrollArea import ScrollArea


def get_arearect(settings):
	area_width = settings.default_width * 0.9
	area_height = settings.default_height * 0.9

	middle_x = settings.default_x + settings.default_width/2
	middle_y = settings.default_y + settings.default_height/2

	area_x = middle_x - area_width/2
	area_y = middle_y - area_height/2

	return area_x, area_y, area_width, area_height


class SettingsPage(Button):
	def __init__(self, parent):
		super(SettingsPage, self).__init__(parent)

		self.default_x = 20
		self.default_y = 20
		self.default_size = 4

		self.img_idle = "res/WindowShadow.png"
		self.img_hover = "res/WindowShadow.png"
		self.img_click = "res/WindowShadow.png"

		super().setup()

		settingsarea = ScrollArea(parent)
		settingsarea.default_x, settingsarea.default_y, settingsarea.default_width, settingsarea.default_height = get_arearect(self)
		settingsarea.setup()

		self.settingsarea = settingsarea

	def changesize(self):
		super().changesize()
		self.settingsarea.changesize()

