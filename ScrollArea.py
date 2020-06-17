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
		render_ = QtWidgets.QLabel("Render Options")
		render_.setStyleSheet("""font: bold 24px;color:white;""")

		separator = QtWidgets.QLabel()
		separator_img = QtGui.QPixmap('res/Separator.png')
		separator_img = separator_img.scaled(500, 10, QtCore.Qt.KeepAspectRatio)
		separator.setPixmap(separator_img)

		paths = ["osu! path:", "Output path:"]
		osu_pathLabel = QtWidgets.QLabel(paths[0])
		osu_pathLabel.setStyleSheet("font: bold 12px;color:white;")
		osu_pathInput = QtWidgets.QLineEdit()
		osu_pathInput.setFixedWidth(300)

		output_pathLabel = QtWidgets.QLabel(paths[1])
		output_pathLabel.setStyleSheet("font: bold 12px;color:white;")
		output_pathInput = QtWidgets.QLineEdit()
		output_pathInput.setFixedWidth(300)

		width_label = QtWidgets.QLabel("Width:")
		width_label.setStyleSheet("font: bold 12px;color:white;")
		width_Input = QtWidgets.QLineEdit()

		fps_label = QtWidgets.QLabel("FPS:")
		fps_label.setStyleSheet("font: bold 12px;color:white;")
		fps_Input = QtWidgets.QLineEdit()
		fps_Input.setFixedWidth(300)

		codec_label = QtWidgets.QLabel("Video codec:")
		codec_label.setStyleSheet("font: bold 12px;color:white;")
		codec_Input = QtWidgets.QLineEdit()

		vertical_widgets = []
		horizontal_widgets = []

		vertical_widgets.extend((render_, separator, osu_pathLabel, osu_pathInput, output_pathLabel, output_pathInput))
		horizontal_widgets.extend((width_label, width_Input, fps_label, fps_Input, codec_label, codec_Input))

		for x in range(len(vertical_widgets)):
			self.gridLayout.addWidget(vertical_widgets[x], x, 0)

		for x in range(2,len(horizontal_widgets),1):
			self.gridLayout.addWidget(horizontal_widgets[x], x, 1)


		#scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


		for x in range(2,200,1):
			self.gridLayout.addWidget(QtWidgets.QLabel("Test"), 2, x)
			print("brother")




