import PyQt5
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
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication
import os
from PPComponents.Buttons import SaveButton, Reset
from PPComponents.Layout import PPLayout
from PPComponents.Menu import PPMenu
from abspath import abspath
from config_data import current_ppsettings
import logging


class PPSample:
	def __init__(self, width, ppsettings):
		self.background = Image.open(os.path.join(abspath, "res/pppp.png"))
		ratio = self.background.size[1]/self.background.size[0]
		newheight = int(width * ratio)
		self.background = self.background.resize((width, newheight), Image.ANTIALIAS)
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


class PPwindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("PP option")
		self.windowwidth = self.default_width = 800
		self.windowheight = self.default_height = 720
		self.setFixedSize(QSize(self.windowwidth, self.windowheight))
		self.ppsample = PPSample(self.windowwidth, current_ppsettings)
		self.optionpath = os.path.join(os.path.dirname(__file__), "ppoptions_config.json")
		self.setStyleSheet("background-color: rgb(30, 30, 33);")

		self.label = QLabel(self)

		self.pplayout = PPLayout(self, self)
		self.pplayout.load_settings(current_ppsettings)
		self.savebutton = SaveButton(self)
		self.reset = Reset(self)

		self.menu = PPMenu(self)

		self.label = QLabel(self)
		self.updatepp()
		self.label.setGeometry(0, 0, self.ppsample.settings.width, self.ppsample.settings.height)

		self.show()

	def updatepp(self):
		try:
			self.ppsample.draw()
		except Exception as e:
			logging.error(repr(e))
			return
		pixmap = QPixmap(self.ppsample.outputpath)
		self.label.setPixmap(pixmap)


def excepthook(exc_type, exc_value, exc_tb):
	tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
	logging.exception(tb)
	print(tb)
	QApplication.quit()


def main(execpath="."):
	sys.excepthook = excepthook

	qtpath = os.path.dirname(PyQt5.__file__)
	pluginpath = os.path.join(qtpath, "Qt/plugins")
	os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = pluginpath

	logpath = os.path.join(execpath, "Logs", "custompp.log")
	logging.basicConfig(level=logging.DEBUG, filename=logpath, filemode="w",
	                    format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")

	app = QApplication([])
	window = PPwindow()
	app.exec_()


if __name__ == "__main__":
	main()