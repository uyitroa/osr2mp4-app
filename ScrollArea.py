import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
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

		layout.setGeometry(QtCore.QRect(20,20,400,250))
		styleSheet ="""


        QScrollBar::handle:vertical {
            background: transparent;
            height: 1px;
            image: url('res/SliderBall_HD.png');

        }

        QScrollBar::add-line:vertical {
            height: 1px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            height: 1px;
            subcontrol-position: top left;
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
		for i in range(10):
			self.gridLayout.addWidget(QtWidgets.QPushButton(), i, 2)