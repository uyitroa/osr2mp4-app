from PyQt5.QtWidgets import QLineEdit

class Big_Textbox(QLineEdit):
	def __init__(self, parent=None):
		super().__init__()
		self.setStyleSheet("font: bold 12px;color:white;")
		self.setFixedWidth(200)

class Small_Textbox(QLineEdit):
	def __init__(self, parent=None):
		super().__init__()
		self.setStyleSheet("font: bold 12px;color:white;")
		self.setFixedWidth(50)
