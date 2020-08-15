from PyQt5.QtWidgets import QLabel, QGraphicsBlurEffect

from BaseComponents.Buttons import Button


class PathBox(Button):
	def __init__(self, parent):
		super(PathBox, self).__init__(parent)
		self.img_idle = self.img_hover = self.img_click = None
		self.text = QLabel(parent)
		self.text.setText("")
		self.default_fontsize = 150
		self.offset = 225

	def setup(self):
		self.img_idle = self.img_hover = self.img_click = self.img
		super().setup()
		self.textblur_effect = QGraphicsBlurEffect()
		self.textblur_effect.setBlurRadius(0)
		self.text.setGraphicsEffect(self.textblur_effect)

	def blur_me(self, blur):
		super().blur_me(blur)
		if blur:
			self.textblur_effect.setBlurRadius(10)
		else:
			self.textblur_effect.setBlurRadius(0)

	def setText(self, text):
		self.text.setToolTip(text)
		self.setToolTip(text)
		self.text.setText(text)
		self.main_window.settingspage.updatevalue()

	def changesize(self):
		super().changesize()

		scale = self.height() / self.main_window.default_height

		x = self.x() + scale * self.offset
		y = self.y() + scale * self.offset

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet(
			"QLabel{font-size: %ipt; font-weight: bold; color: white; background-color: transparent;}QToolTip { background-color:white;color: black; }" % (fontsize))
		self.text.setGeometry(x, y, self.width() * 0.95, self.height() * 0.5)