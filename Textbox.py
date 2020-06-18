from PyQt5.QtWidgets import QLineEdit


class ParentTextbox(QLineEdit):
	def __init__(self):
		super().__init__()
		self.default_width = 1
		self.default_height = 1

		# Do your setStylesheet here
		self.setStyleSheet("font: bold 12px;color:white;")

	def setFixedHeight(self, p_int):
		pass


class Big_Textbox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()

		self.default_width = 200
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)
		self.setStyleSheet("""
QLineEdit {
 border: 2px solid white;
 border-radius: 6px;
}
"""
			)


class Small_Textbox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()

		self.default_width = 50
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)
		self.setStyleSheet("""
QLineEdit {
 border: 2px solid white;
 border-radius: 6px;
}
""")
