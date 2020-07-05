import cv2
from PyQt5 import QtCore
import logging


# logging.basicConfig(level=logging.DEBUG, stream=open(Log.apppath, "a+"), format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")


def getsize(img):
	a = cv2.imread(img, -1)
	logging.info("Image loaded: {}".format(img))
	return a.shape[1], a.shape[0]


def changesize(widget):
	scale = widget.main_window.height() / widget.main_window.default_height

	x = widget.default_x * scale
	y = widget.default_y * scale

	width = widget.default_width * scale
	height = widget.default_height * scale

	widget.setIconSize(QtCore.QSize(width, height))
	widget.setGeometry(x, y, width, height)
