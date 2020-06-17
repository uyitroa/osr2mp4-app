import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
class Scroll_Class():
	def __init__(self,parent):
		super().__init__()
		
		layout = QtWidgets.QHBoxLayout(parent)
		scrollArea = QtWidgets.QScrollArea(parent)
		scrollArea.setWidgetResizable(True)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		self.gridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
		scrollArea.setWidget(scrollAreaWidgetContents)
		layout.addWidget(scrollArea)

		layout.setGeometry(QtCore.QRect(20,20,550,450))
		styleSheet ="""

		QScrollBar::handle:vertical {
			height: 1px;
			image: url('res/SliderBall_HD.png');
			border:none;

		}

		QScrollBar::add-line:vertical {
			height: 1px;
			subcontrol-position: top;
			subcontrol-origin: margin;
		}

		QScrollBar::sub-line:vertical {
			height: 1px;
			subcontrol-origin: margin;
			position: absolute;
			image: url('res/scroll_back.png');
		}

		QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {

		   image: url('res/scroll_back.png');
		}

		QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
			background: transparent;
		}
				  """
		scrollArea.verticalScrollBar().setStyleSheet(styleSheet)
		scrollArea.verticalScrollBar().setValue(0)
		render_ = QtWidgets.QLabel("Render Options1111")
		render_.setStyleSheet("""font: bold 24px;color:white;""")

		separator = QtWidgets.QLabel()
		separator_img = QtGui.QPixmap('res/Separator.png')
		separator_img = separator_img.scaled(550, 10, QtCore.Qt.KeepAspectRatio)
		separator.setPixmap(separator_img)

		self.gridLayout.addWidget(render_, 0, 2)
		self.gridLayout.addWidget(separator, 1, 2)
		for x in range(2,10,1):
			self.gridLayout.addWidget(QtWidgets.QLabel("Test"), x, 2)
		


