from PyQt5 import QtCore
from PyQt5.QtCore import QFileSystemWatcher

from Parents import Button
from PyQt5.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
	def __init__(self, parent):
		super(ProgressBar, self).__init__(parent)
		self.parent = parent
		self.setGeometry(0, 420, 830, 40) 
  
		self.setAlignment(QtCore.Qt.AlignCenter) 

		self.setStyleSheet("""
QProgressBar {
	border: 2px solid white;
	border-radius: 5px;
	color:white;	
}

QProgressBar::chunk {
	background-color: rgba(226, 107, 167, 255);
}""")




	def directory_changed(self, path):
		print('Directory Changed:', path)
		

	def file_changed(self, path):
		f = open(path, "r")
		self.setValue(max(self.value(), float("0" + f.read())))
		f.close()
		if self.value() >= 100: # don't judge me by adding if greater than 100 which is impossible. fuck just making sure. hashtag uyitroa got predicted
			self.parent.startbutton.default_y = 360
			self.parent.Options.default_y = 360
			self.setParent(None)
			print("chanfed")
