import sys
import subprocess
import threading
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QSizePolicy


class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.resize(100, 100)
		self.text = QLabel(self)
		self.text.setText("Updating...")
		self.text.setGeometry(0, -100, 300, 300)
		self.upgradelist = ["osr2mp4", "osr2mp4app"]
		self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
		self.a = threading.Thread(target=self.install)
		self.show()

	def install(self):
		for i in self.upgradelist:
			subprocess.call([sys.executable, "-m", "pip", "install", i, "--upgrade"])
		QApplication.quit()


app = QApplication([])
window = Window()
window.a.start()
app.exec_()
window.a.join()
