from BaseComponents.Buttons import Button


class OsrGrayButton(Button):
	def __init__(self, parent):
		super(OsrGrayButton, self).__init__(parent)

		self.default_x = 490
		self.default_y = 30
		self.default_size = 3.5

		self.img_idle = "res/osr_idle_unavailable.png"
		self.img_hover = "res/osr_idle_unavailable.png"
		self.img_click = "res/osr_idle_unavailable.png"
		super().setup()

		self.hide()
