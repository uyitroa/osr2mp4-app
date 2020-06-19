from Parents import PopupButton


class OutputButton(PopupButton):
	def __init__(self, parent):
		super(OutputButton, self).__init__(parent)

		self.default_x = 213
		self.default_y = 330
		self.default_size = 3.35
		self.file_type = "Folder"

		self.img_idle = "res/OutputFolder_Idle.png"
		self.img_hover = "res/OutputFolder_Hover.png"
		self.img_click = "res/OutputFolder_Click.png"
		self.parent = parent
		super().setup()
