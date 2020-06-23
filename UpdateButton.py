import os
import subprocess
import sys

from PyQt5.QtWidgets import QLabel

from Parents import Button


class UpdateButton(Button):
	def __init__(self, parent):
		super(UpdateButton, self).__init__(parent)

		self.default_x = 10
		self.default_y = 430
		self.default_size = 0.8
		self.text_x = 500
		self.text_y = -10
		self.default_fontsize = 300

		self.img_idle = "res/SmallText_HD.png"
		self.img_hover = "res/SmallText_HD.png"
		self.img_click = "res/SmallText_HD.png"
		super().setup()

		self.text = QLabel(self)
		self.text.setText("Update")

	def mouseclicked(self):
		# proc = subprocess.Popen([sys.executable, "updater.py"])
		fupdate = open(os.path.join(self.main_window.execpath, "exit.txt"), "w")
		fupdate.write("1")
		fupdate.close()
		sys.exit(0)

	def changesize(self):
		super().changesize()
		scale = self.height()/self.main_window.default_height

		x = scale * self.text_x
		y = scale * self.text_y

		fontsize = scale * self.default_fontsize
		self.text.setStyleSheet("font-size: {}pt; font-weight: bold; color: white; background-color: rgba(0,0,0,0%)".format(fontsize))
		self.text.setGeometry(x, y, self.width(), self.height())
