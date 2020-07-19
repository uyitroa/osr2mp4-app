import json
import sys
import traceback

import osr2mp4
from PIL import Image
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from osr2mp4.ImageProcess.Objects.Scores.PPCounter import PPCounter
from osr2mp4.ImageProcess.Objects.Scores.HitresultCounter import HitresultCounter
from osr2mp4.Utils.Resolution import get_screensize
from osr2mp4.global_var import Settings
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPlainTextEdit, QPushButton
import os
from osr2mp4.osr2mp4 import defaultppconfig
from abspath import pppath, abspath
from config_data import current_ppsettings
import logging


class PPSample:
	def __init__(self, height, ppsettings):
		self.background = Image.open(os.path.join(abspath, "res/pppp.png"))
		ratio = self.background.size[0]/self.background.size[1]
		newwidth = int(height * ratio)
		self.background = self.background.resize((newwidth, height), Image.ANTIALIAS)
		self.outputpath = os.path.join(abspath, "ppsample.png")

		settings = Settings()
		settings.path = os.path.dirname(osr2mp4.__file__) + "/"
		width, height = self.background.size
		playfield_scale, playfield_width, playfield_height, scale, move_right, move_down = get_screensize(width, height)
		settings.scale = scale
		settings.width = width
		settings.height = height
		settings.settings["Enable PP counter"] = True
		settings.ppsettings = ppsettings
		self.ppcounter = PPCounter(settings)
		self.ppcounter.set(727.27)

		self.hitresultcounter = HitresultCounter(settings)
		self.hitresultcounter.set({100: 17, 50: 70, 0: 13})
		self.settings = settings

	def draw(self):
		background = self.background.copy()
		self.ppcounter.add_to_frame(background)
		self.hitresultcounter.add_to_frame(background)
		background.save(self.outputpath)


class PPTextBox(QPlainTextEdit):
	def __init__(self, parent, ppoption):
		super().__init__(parent)

		self.setStyleSheet("""
		QPlainTextEdit {
		 border: 2px solid white;
		 border-radius: 6px;
		}
		""")

		windowwidth = parent.windowwidth
		windowheight = parent.windowheight
		imagewidth = parent.ppsample.settings.width

		width = windowwidth - imagewidth - 10
		self.setGeometry(imagewidth + 5, 10, width, windowheight * 0.9)
		self.setPlainText(json.dumps(ppoption, indent=4))


class SaveButton(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		windowheight = parent.windowheight
		imagewidth = parent.ppsample.settings.width

		self.setGeometry(imagewidth, windowheight * 0.92, 100, 50)
		self.setText("Save")

	def mousePressEvent(self, event):
		ppsettings = json.loads(self.parent.hugetextbox.toPlainText())
		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]
		self.parent.ppsample.ppcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.ppcounter.loadimg()
		self.parent.ppsample.hitresultcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.hitresultcounter.loadimg()
		self.parent.updatepp()
		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()


class Reset(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		windowheight = parent.windowheight
		imagewidth = parent.ppsample.settings.width

		self.setGeometry(imagewidth + 100, windowheight * 0.92, 100, 50)
		self.setText("Reset")

	def mousePressEvent(self, event):
		ppsettings = defaultppconfig
		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]
		self.parent.ppsample.ppcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.ppcounter.loadimg()
		self.parent.ppsample.hitresultcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.hitresultcounter.loadimg()
		self.parent.hugetextbox.setPlainText(json.dumps(current_ppsettings, indent=4))
		self.parent.updatepp()
		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()


class PPwindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("PP option")
		self.windowwidth = 1270
		self.windowheight = 600
		self.setFixedSize(QSize(self.windowwidth, self.windowheight))
		self.ppsample = PPSample(self.windowheight, current_ppsettings)

		self.label = QLabel(self)
		self.updatepp()
		self.label.setGeometry(0, 0, self.ppsample.settings.width, self.ppsample.settings.height)

		self.hugetextbox = PPTextBox(self, current_ppsettings)
		self.savebutton = SaveButton(self)
		self.reset = Reset(self)

		self.show()

	def updatepp(self):
		self.ppsample.draw()
		pixmap = QPixmap(self.ppsample.outputpath)
		self.label.setPixmap(pixmap)


def excepthook(exc_type, exc_value, exc_tb):
	tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
	logging.exception(tb)
	print(tb)
	QApplication.quit()


def main(execpath="."):
	sys.excepthook = excepthook

	logpath = os.path.join(execpath, "Logs", "custompp.log")
	logging.basicConfig(level=logging.DEBUG, filename=logpath, filemode="w",
	                    format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")

	app = QApplication([])
	window = PPwindow()
	app.exec_()


if __name__ == "__main__":
	main()