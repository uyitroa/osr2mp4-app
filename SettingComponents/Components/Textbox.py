from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit


class ParentTextbox(QLineEdit):
	def __init__(self, parent=None, jsondata=None):
		super().__init__()
		self.default_width = 1
		self.default_height = 1

		self.setStyleSheet("""
		QLineEdit {
		 border: 2px solid white;
		 border-radius: 6px;
		 color:white;
		}
		""")

		self.key = jsondata["key"]

		if jsondata["key"] in jsondata["data"]["config"]:
			self.current_data = jsondata["data"]["config"]
		else:
			self.current_data = jsondata["data"]["settings"]

		super().textChanged.connect(self.textChanged)
		self.raise_()

	def updatevalue(self):
		self.setText(str(self.current_data[self.key]))

	def setFixedHeight(self, p_int):
		pass

	@QtCore.pyqtSlot(str)
	def textChanged(self, p_str):
		if p_str.isdigit():
			p_str = int(p_str)
		self.current_data[self.key] = p_str


class Big_Textbox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		self.default_width = 250
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)


class Small_Textbox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		self.default_width = 50
		self.default_height = 20

		self.setFixedWidth(self.default_width)
		QLineEdit().setFixedHeight(self.default_height)

