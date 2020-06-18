import os

import cv2
from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollArea

from PyQt5.QtWidgets import QSlider


def scale(val, src, dst):
	"""
	Scale the given value from the scale of src to the scale of dst.
	"""
	return int(((val - src[0]) / float(src[1]-src[0])) * (dst[1]-dst[0]) + dst[0])



class CustomScrolbar(QSlider):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent)

		super().valueChanged.connect(self.valueChanged)

		self.default_width, self.default_height = 20, 350
		self.default_x, self.default_y = 625, 10
		self.resized = False

		self.img_handle = "res/SliderBall_HD.png"
		self.img_scroll = "res/scroll_back.png"

		self.setScrollStyle()
		self.setTracking(True)

		self.setMaximum(0)
		self.setMinimum(-50)

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)

	def setScrollStyle(self):
		self.setStyleSheet("""
QSlider::groove:vertical {
    border-image:url(%s);
}

QSlider::handle:vertical {
    image: url(%s);
    height:30px;
}

		""" % (self.img_scroll, self.img_handle))

	@QtCore.pyqtSlot(int)
	def valueChanged(self, p_int):
		try:
			scrollbar = self.parent().verticalScrollBar()
			val = scale(self.value(), (self.maximum(), self.minimum()), (scrollbar.minimum(), scrollbar.maximum()))
			scrollbar.setValue(val)
		except AttributeError as e:
			print(e)
		except ZeroDivisionError as e:
			pass

	def changesize(self, scale):
		x = self.default_x * scale
		y = self.default_y * scale
		width = self.default_width * scale
		height = self.default_height * scale
		self.setGeometry(x, y, width, height)
		print(self.parent().verticalScrollBar().maximum())
		if self.parent().verticalScrollBar().maximum() == 0:
			self.hide()
		else:
			self.show()


class Scrollbar(QScrollArea):
	def __init__(self, parent, layout):
		super().__init__(parent)

		self.main_window = parent
		self.gridLayout = layout

		self.scrollsize = 30
		self.customscroll = CustomScrolbar(self)

		self.setWidgetResizable(True)
		self.setScrollStyle()
		self.setStyleSheet("background: transparent;border: none;")


	def setScrollStyle(self):
		# scroll_handle = self.fixsize(self.img_handle)

		styleSheet = """
 QScrollBar:vertical {
     width: 0px;
     height: 0px;
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
     width: 0px;
     height: 0px;
     background: none;
 }

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     background: none;
 }
 """
		self.verticalScrollBar().setStyleSheet(styleSheet)



	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height
		self.customscroll.changesize(scale)

	def fixsize(self, filename):
		self.np_handle = cv2.imread(filename, -1)
		scaley = self.gridLayout.rowcounter[0] / self.scrollsize
		return self.resizehandle(filename, scaley)

	def resizehandle(self, filename, scaley):
		scaley = max(0.01, scaley)
		img = cv2.resize(self.np_handle, (0, 0), fx=1, fy=scaley)
		filename, ext = os.path.splitext(filename)
		filename = filename + "1" + ext
		cv2.imwrite(filename, img)
		return filename

	def wheelEvent(self, QWheelEvent):

		try:
			scrollbar = self.verticalScrollBar()

			val = scale(scrollbar.value(), (scrollbar.minimum(), scrollbar.maximum()), (self.customscroll.maximum(), self.customscroll.minimum()))
			self.customscroll.setValue(val)
		except AttributeError as e:
			pass
		except ZeroDivisionError as e:
			pass

		return super().wheelEvent(QWheelEvent)
