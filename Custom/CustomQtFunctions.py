from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os


def blur_widget(widgets):
    for widget in widgets:
        blur_effect = QGraphicsBlurEffect()
        widget.setGraphicsEffect(blur_effect)


def set_pixmap(parent, app_directory, pixmap_img, scale):
    pixmap = QPixmap(os.path.join(app_directory, pixmap_img)).scaled(scale[0], scale[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    parent.setPixmap(pixmap)
