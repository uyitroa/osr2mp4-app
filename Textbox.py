from PyQt5.QtWidgets import QLineEdit


class ParentTextbox(QLineEdit):
	def __init__(self):
		super().__init__()
		self.default_width = 1
		self.default_height = 1

	def setFixedHeight(self, p_int):
		pass


class Big_Textbox(ParentTextbox):
	def __init__(self, parent=None):
		super().__init__()

		self.default_width = 200
		self.default_height = 20

		self.setStyleSheet("font: bold 12px;color:white;")
		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)


class Small_Textbox(ParentTextbox):
	def __init__(self, parent=None):
		super().__init__()

		self.default_width = 50
		self.default_height = 20

		self.setStyleSheet("font: bold 12px;color:white;")
		self.setFixedWidth(self.default_width)
		self.setFixedHeight(self.default_height)
