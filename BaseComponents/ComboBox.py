import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QGraphicsBlurEffect

from abspath import abspath
from helper.helper import getsize, changesize


class ComboBox(QComboBox):
	def __init__(self, parent):
		super().__init__(parent)
		self.img_drop = os.path.join(abspath, "res/Drop_Scale.png")
		self.img_listview = os.path.join(abspath, "res/listview.png")
		self.setToolTip("Skin that will be used in the video")
		self.default_width = 0.6
		self.default_height = 0.6

		self.activated.connect(self.activated_)
		self.main_window = parent
		self.setStyleSheet("""
		QComboBox {
			 border-image : url(%s);
			 color: white;
			 font-size: 9pt;
		}

		QComboBox::drop-down {
			 border-bottom-right-radius: 1px;
		}

		QListView {
			 outline: none;
			 color: white;
			 font: bold;
			 border-image : url(%s);
		}

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
		QTextEdit, QListView {
		background-color: rgba(0, 0, 0, 0);
		background-attachment: scroll;
		}

			 """ % (self.img_drop, self.img_listview))

	def setup(self):
		width, height = getsize(self.img_drop)
		self.default_width *= width
		self.default_height *= height

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)
		self.setIconSize(QtCore.QSize(self.default_width, self.default_height))
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden
		self.setMaxVisibleItems(7)

		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

	def activated_(self, index):
		pass

	def changesize(self):
		changesize(self)
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25)
		else:
			self.blur_effect.setBlurRadius(0)
