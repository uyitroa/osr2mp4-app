from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
from Custom.CustomQtFunctions import set_pixmap
import os


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))

    def setup(self):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, [self.width(), self.height()])
        self.main_window.path_vertical_layout.addWidget(self)

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_idle)
        self.setPixmap(pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class Logo(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))

    def setup(self):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, [self.width(), self.height()])
        self.main_window.logo_horizontal.addWidget(self)

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_idle)
        self.setPixmap(pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class CustomButtons(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))
        #self.setScaledContents(True)

    def setup(self):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, [self.width(), self.height()])
        self.main_window.button_vertical_layout.addWidget(self)

    def enterEvent(self, event):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_hover, [self.width(), self.height()])

    def leaveEvent(self, event):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, [self.width(), self.height()])

    def mouseReleaseEvent(self, event):
        set_pixmap(self, self.main_window.app_directory, self.pixmap_idle, [self.width(), self.height()])

    def mousePressEvent(self, event):
        pixmap = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.pixmap_clicked)).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        home_dir = str(Path.home())
        if self.file_extension == "folder":
            beatmap_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Beatmap Folder ', home_dir)
            print(beatmap_path)
        elif self.file_extension == ".osr":
            replay_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', home_dir, ".osr (*.osr)")



    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_idle)
        self.setPixmap(pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
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



