from PyQt5.QtWidgets import QLabel

from Parents import Button, PathImage


class OsrPath(PathImage):
	def __init__(self, parent):
		super(OsrPath, self).__init__(parent)

		self.default_x = 400
		self.default_y = 250
		self.default_size = 5

		self.img = "res/OsrPath.png"
		self.img_shadow = "res/OsrPath_Shadow.png"

		super().setup()


class MapSetPath(PathImage):
	def __init__(self, parent):
		super(MapSetPath, self).__init__(parent)

		self.default_x = 400
		self.default_y = 300
		self.default_size = 5

		self.img = "res/MapsetPath.png"
		self.img_shadow = "res/MapsetPath_Shadow.png"

		super().setup()
