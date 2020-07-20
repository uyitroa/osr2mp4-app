from PyQt5.QtWidgets import QLabel

from Parents import Button


class SaveButton(Button):
	def __init__(self, parent):
		super(SaveButton, self).__init__(parent)
		self.default_x = parent.windowwidth * 0.75
		self.default_y = parent.windowheight * 0.85
		self.default_size = 0.75
		self.text_x = 40
		self.text_y = -2

		self.img_idle = "res/SmallButton.png"
		self.img_hover = "res/SmallButton hover.png"
		self.img_click = "res/SmallButton click.png"

		self.text = QLabel(self)
		self.text.setText("Save")
		self.text.setStyleSheet("QLabel{color: white; background-color: transparent;}")
		self.text.setGeometry(self.text_x, self.text_y, self.width(), self.height())

		self.setToolTip("Ctrl+S")

		super().setup()

		self.show()

	def mouseclicked(self):
		self.main_window.menu.save()


class Reset(Button):
	def __init__(self, parent):
		super(Reset, self).__init__(parent)
		self.default_x = parent.windowwidth * 0.75
		self.default_y = parent.windowheight * 0.9
		self.default_size = 0.75
		self.text_x = 40
		self.text_y = -2

		self.img_idle = "res/SmallButton.png"
		self.img_hover = "res/SmallButton hover.png"
		self.img_click = "res/SmallButton click.png"

		self.text = QLabel(self)
		self.text.setText("Reset")
		self.text.setStyleSheet("QLabel{color: white; background-color: transparent;}")
		self.text.setGeometry(self.text_x, self.text_y, self.width(), self.height())

		self.setToolTip("Ctrl+R")

		super().setup()

		self.show()

	def mouseclicked(self):
		self.main_window.menu.reset()
