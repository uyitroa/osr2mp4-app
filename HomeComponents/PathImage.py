from PyQt5.QtWidgets import QLabel

from Parents import Button, PathImage


class OsrPath(PathImage):
	def __init__(self, parent):
		super(OsrPath, self).__init__(parent)

		self.default_x = 544
		self.default_y = 165
		self.default_size = 4.5

		self.img = "res/OsrPath.png"
		self.img_shadow = "res/OsrPath_Shadow.png"

		super().setup()


class MapSetPath(PathImage):
	def __init__(self, parent):
		super(MapSetPath, self).__init__(parent)

		self.default_x = 544
		self.default_y = 200
		self.default_size = 4.5

		self.img = "res/MapsetPath.png"
		self.img_shadow = "res/MapsetPath_Shadow.png"

		super().setup()
