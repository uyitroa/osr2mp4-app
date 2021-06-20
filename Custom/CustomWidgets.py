from PyQt5 import QtWidgets, QtGui, QtCore


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.setMinimumSize(QtCore.QSize(50, 50))

    def setup(self):
        pixmap = QtGui.QPixmap(self.pixmap_idle).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setGeometry(self.default_coordinates[0], self.default_coordinates[1], self.default_scale[0], self.default_scale[1])
        self.setPixmap(pixmap)

    def enterEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_hover).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def leaveEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_idle).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        pixmap = QtGui.QPixmap(self.pixmap_clicked).scaled(self.default_scale[0], self.default_scale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

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



