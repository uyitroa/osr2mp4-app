from PyQt5.QtWidgets import QLabel


class ParentTitle(QLabel):
	def __init__(self, default_fontsize=1):
		super().__init__()
		self.default_width = 1
		self.default_height = 1
		self.default_fontsize = default_fontsize
		self.setStyleSheet("font: bold %ipx;color:white;" % self.default_fontsize)

	def width(self):
		return self.fontMetrics().boundingRect(self.text).width() * 2

	def height(self):
		return self.fontMetrics().boundingRect(self.text).height() * 2

	def setFixedHeight(self, p_int):
		scale = p_int / self.default_height
		self.setStyleSheet("font-size: %ipx; font-weight: bold; color: white;" % int(scale * self.default_fontsize))
		super().setFixedHeight(p_int)

	def updatevalue(self):
		pass


class Titles(ParentTitle):
	def __init__(self, title, pixmap=None, parent=None):
		self.default_fontsize = 24
		super().__init__(self.default_fontsize)
		self.text = title + "   "
		self.setText(title)
		font = self.font()
		font.setPointSize(100)
		self.setFont(font)

		self.default_width = super().width()
		self.default_height = super().height()


class Small_Titles(ParentTitle):
	def __init__(self, title, parent=None):
		self.default_fontsize = 14
		super().__init__(self.default_fontsize)
		self.text = title + "   "
		self.setText(title)

		self.default_width = super().width()
		self.default_height = super().height()

