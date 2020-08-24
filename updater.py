import sys
import subprocess
import threading
import os
import PyQt5

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QSizePolicy, QDesktopWidget, QWidget

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.left = 0
		self.top = 0
		self.width = 242
		self.height = 242

		self.label = QLabel(self)

		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setFixedSize(self.width, self.height)

		self.upgradelist = ["osr2mp4", "osr2mp4app"]
		self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
		self.a = threading.Thread(target=self.install)

		self.osrLogoUpdater()
	def osrLogoUpdater(self):
		pixmap = QPixmap('res/OsrUpdater.png')
		self.label.setPixmap(pixmap)
		self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)
		self.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)
		self.center()
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def install(self):
		for i in self.upgradelist:
			subprocess.call([sys.executable, "-m", "pip", "install", i, "--upgrade"])
		QApplication.quit()


qtpath = os.path.dirname(PyQt5.__file__)
pluginpath = os.path.join(qtpath, "Qt/plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = pluginpath


app = QApplication([])
window = Window()
window.a.start()
app.exec_()
window.a.join()
