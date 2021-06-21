from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
from Custom.CustomQtFunctions import set_pixmap
import os


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))
        self.setScaledContents(True)

    def setup(self):
        pixmap = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.pixmap_idle)).scaled(self.default_scale[0], self.default_scale[1],QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setGeometry(self.default_coordinates[0], self.default_coordinates[1], self.default_scale[0], self.default_scale[1])
        self.setPixmap(pixmap)
        self.main_window.main_layout.addWidget(self, self.row, self.col)


class CustomButtons(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))
        self.setScaledContents(True)

    def setup(self):
        self.setGeometry(self.default_coordinates[0], self.default_coordinates[1], self.default_scale[0], self.default_scale[1])
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, self.default_scale)
        self.main_window.main_layout.addWidget(self, self.row, self.col)

    def enterEvent(self, event):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_hover, self.default_scale)

    def leaveEvent(self, event):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, self.default_scale)

    def mousePressEvent(self, event):
        pixmap = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.pixmap_clicked)).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        home_dir = str(Path.home())
        if self.file_extension == "folder":
            beatmap_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Beatmap Folder ', home_dir)
            print(beatmap_path)
        elif self.file_extension == ".osr":
            replay_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', home_dir, ".osr (*.osr)")

    def mouseReleaseEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_idle).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    '''
    def resize(self):
        scale = self.main_window.height() / 469

        x = self.default_coordinates[0] * scale
        y = self.default_coordinates[1] * scale

        width = self.default_scale[0] * scale
        height = self.default_scale[1] * scale


        _pixmap = QtGui.QPixmap(self.pixmap_idle)
        self.setPixmap(_pixmap.scaled(
            width, height,
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.setGeometry(x, y, width, height)
        '''



