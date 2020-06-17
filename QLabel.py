from PyQt5.QtWidgets import QLabel

class Titles(QLabel):
	def __init__(self, title, pixmap=None, parent=None):
		super().__init__()
		if pixmap:
			separator_img = QtGui.QPixmap('res/Separator.png')
			separator_img = separator_img.scaled(500, 10, QtCore.Qt.KeepAspectRatio)
			separator.setPixmap(separator_img)
		self.setText(title)
		self.setStyleSheet("font: bold 24;color:white;")

class Small_Titles(QLabel):
	def __init__(self, title, parent=None):
		super().__init__()
		self.setText(title)
		self.setStyleSheet("font: bold 12;color:white;")

