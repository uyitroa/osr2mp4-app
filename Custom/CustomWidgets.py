from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
import os
import json

class DefaultLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(20, 20))

    def setup(self):
        if self.img_hover is not None:
            self.pixmap_hover = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_hover))
        else:
            self.pixmap_hover = None
        self.pixmap_idle = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))

        self.layout.addWidget(self)
        self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def resizeEvent(self, event):
        self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        if self.text is not None:
            self.main_window.map_path.resize_text_path()
            self.main_window.osr_path.resize_text_path()

    def enterEvent(self, event):
        if self.pixmap_hover is not None:
            self.setPixmap(self.pixmap_hover.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def leaveEvent(self, event):
        if self.pixmap_hover is not None:
            self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def mouseReleaseEvent(self, event):
        self.on_clicked()

    def on_clicked(self):
        return

class CustomButtons(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 50))
        self.blur_effect=None

    def setup(self):
        self.pixmap_idle = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        self.pixmap_hover = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_hover))
        self.pixmap_clicked = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_clicked))
        self.layout.addWidget(self)

    def enterEvent(self, event):
        self.setPixmap(self.pixmap_hover.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def leaveEvent(self, event):
        self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def mouseReleaseEvent(self, event):
        self.setPixmap(self.pixmap_clicked.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        home_dir = str(Path.home())
        if self.file_extension is not None:
            if self.file_extension == "folder":
                beatmap_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Beatmap Folder ', home_dir)
            elif self.file_extension == ".osr":
                replay_path = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', home_dir, ".osr (*.osr)")

    def mousePressEvent(self, event):
        self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def resizeEvent(self, event):
        self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class PopupLabels(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(10, 10))

    def setup(self):
        self.pixmap_idle = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_idle))
        if self.clickable:
            self.pixmap_hover = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_hover))
            self.pixmap_clicked = QtGui.QPixmap(os.path.join(self.main_window.app_directory, self.img_clicked))

    def enterEvent(self, event):
        if self.clickable:
            self.setPixmap(self.pixmap_hover.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def leaveEvent(self, event):
        if self.clickable:
            self.setPixmap(self.pixmap_idle.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        if self.clickable:
            home_dir = str(Path.home())
            if self.file_extension is not None:
                if self.file_extension == "folder":
                    try:
                        path = QtWidgets.QFileDialog.getExistingDirectory(self, self.file_name, home_dir)
                        self.main_window.current_config[self.file_name] = path
                    except Exception as e:
                        print("Error:", e.__class__, "detected.")
        if self.main_window.current_config["Output path"] != "" and self.main_window.current_config["osu! path"] != "":
            self.main_window.delete_popups()
            self.main_window.unblur_home_components()
            data_directory = os.path.join(self.main_window.app_directory, "data/config.json")
            with open(data_directory, 'w') as f:
                current_config = json.dumps(self.main_window.current_config, indent = 4)
                f.write(current_config)

