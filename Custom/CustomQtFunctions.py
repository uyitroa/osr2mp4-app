from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os


def blur_widget(widgets):
    for widget in widgets:
        blur_effect = QGraphicsBlurEffect()
        widget.setGraphicsEffect(blur_effect)

