from Parents import Button


class Logo(Button):
	def __init__(self, parent):
		super(Logo, self).__init__(parent)

		self.default_x = 20
		self.default_y = 30
		self.default_size = 3.5

		self.img_idle = "res/OsrLogo.png"
		self.img_hover = "res/OsrLogo.png"
		self.img_click = "res/OsrLogo.png"
		self.img_shadow = "res/OsrLogo_Shadow.png"
		super().setup()
