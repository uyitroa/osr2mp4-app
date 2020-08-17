from BaseComponents.Buttons import Button
from helper.helper import kill, cleanupkill
import os
from abspath import abspath


class CancelButton(Button):
	def __init__(self, parent):
		super(CancelButton, self).__init__(parent)

		self.default_x = 600
		self.default_y = 330
		self.default_size = 3.5

		self.img_idle = "res/CancelButton.png"
		self.img_hover = "res/CancelButton_hover.png"
		self.img_click = "res/CancelButton_click.png"
		self.proc = None
		self.parent = parent
		super().setup()

		self.hide()

	def mouseclicked(self):
		if self.main_window.startbutton.proc is not None and self.main_window.startbutton.proc.poll() is None:
			kill(self.main_window.startbutton.proc.pid)
			cleanupkill()
		with open(os.path.join(abspath, "progress.txt"), "w") as filee:
			filee.write(".")
