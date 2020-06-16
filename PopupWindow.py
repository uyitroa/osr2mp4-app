from Parents import Button


class PopupWindow(Button):
	def __init__(self, parent):
		super(PopupWindow, self).__init__(parent)

		self.default_x = 150
		self.default_y = 70
		self.default_size = 3.5

		self.img_idle = "res/Window.png"
		self.img_hover = "res/Window.png"
		self.img_click = "res/Window.png"
		self.img_shadow = "res/Window_Shadow.png"

		super().setup()
