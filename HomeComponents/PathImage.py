from BaseComponents.PathBox import PathBox


class OsrPath(PathBox):
	def __init__(self, parent):
		super(OsrPath, self).__init__(parent)

		self.default_x = 544
		self.default_y = 175
		self.default_size = 4.5

		self.img = "res/OsrPath.png"
		self.img_shadow = "res/OsrPath_Shadow.png"

		super().setup()


class MapSetPath(PathBox):
	def __init__(self, parent):
		super(MapSetPath, self).__init__(parent)

		self.default_x = 544
		self.default_y = 210
		self.default_size = 4.5

		self.img = "res/MapsetPath.png"
		self.img_shadow = "res/MapsetPath_Shadow.png"

		super().setup()
