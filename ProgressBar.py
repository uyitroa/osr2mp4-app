from PyQt5 import QtCore
from PyQt5.QtCore import QFileSystemWatcher

from Parents import Button


class ProgressBar(Button):
	def __init__(self, parent):
		super(ProgressBar, self).__init__(parent)

		self.default_x = 20
		self.default_y = 430
		self.default_size = 4.2

		self.img_idle = "res/progressbar.png"
		self.img_hover = "res/progressbar.png"
		self.img_click = "res/progressbar.png"

		super().setup()

		'''watcher = QFileSystemWatcher()
		watcher.addPath("progress.txt")
		watcher.directoryChanged.connect(self.directoryChanged)'''

		watcher = QtCore.QFileSystemWatcher(['progress.txt'])
		watcher.directoryChanged.connect(directory_changed)
		watcher.fileChanged.connect(file_changed)


def directory_changed(path):
	print('Directory Changed:', path)


def file_changed(path):
	print('File Changed: ', path)
