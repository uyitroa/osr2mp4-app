from PyQt5.QtWidgets import QLabel


class ParentTitle(QLabel):
	def __init__(self):
		super().__init__()
		self.default_width = 1
		self.default_height = 1
		self.default_fontsize = 1

	def width(self):
		return self.fontMetrics().boundingRect( "My text" ).width()

	def height(self):
		return self.fontMetrics().boundingRect( "My text" ).height()

	def setFixedWidth(self, p_int):
		# scale = p_int / self.default_width
		# self.setStyleSheet("font: bold %f; color: white;" % scale * self.default_fontsize)
		# super().setFixedHeight(p_int)
		pass

	def setFixedHeight(self, p_int):
		# scale = p_int / self.default_height
		# self.setStyleSheet("font: bold %f; color: white;" % scale * self.default_fontsize)
		# super().setFixedHeight(p_int)
		pass


class Titles(ParentTitle):
	def __init__(self, title, pixmap=None, parent=None):
		super().__init__()
		if pixmap:
			separator_img = QtGui.QPixmap('res/Separator.png')
			separator_img = separator_img.scaled(500, 10, QtCore.Qt.KeepAspectRatio)
			separator.setPixmap(separator_img)
		self.setText(title)
		self.default_fontsize = 24
		self.setStyleSheet("font: bold 24;color:white;")

		self.default_width = super().width()
		self.default_height = super().height()



class Small_Titles(ParentTitle):
	def __init__(self, title, parent=None):
		super().__init__()
		self.setText(title)
		self.default_fontsize = 12
		self.setStyleSheet("font: bold 12;color:white;")

		self.default_width = super().width()
		self.default_height = super().height()

