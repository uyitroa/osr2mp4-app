from PyQt5 import QtCore
from PyQt5.QtCore import QFileSystemWatcher

from Parents import Button
from PyQt5.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
	def __init__(self, parent):
		super(ProgressBar, self).__init__(parent)
		self.setGeometry(200, 100, 400, 60) 
  
		self.setAlignment(QtCore.Qt.AlignCenter) 

		self.setStyleSheet("""
QProgressBar {
    border: 2px solid grey;
    border-radius: 5px;
}

QProgressBar::chunk {
    background-color: #05B8CC;
    width: 20px;
}""")
		'''self.default_x = 20
		self.default_y = 430
		self.default_size = 4.2

		self.img_idle = "res/progressbar.png"
		self.img_hover = "res/progressbar.png"
		self.img_click = "res/progressbar.png"

		super().setup()'''



	def directory_changed(self, path):
		print('Directory Changed:', path)
		

	def file_changed(self, path):
		f = open(path, "r")
		a = f.readline()
		self.setValue(int(a))
		f.close()
		
