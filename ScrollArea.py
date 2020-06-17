import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from QLabel import Titles, Small_Titles
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
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

		#Vertical
		separator = QtWidgets.QLabel()
		separator_img = QtGui.QPixmap('res/Separator.png')
		separator_img = separator_img.scaled(500, 10, QtCore.Qt.KeepAspectRatio)
		separator.setPixmap(separator_img)

		osu_pathLabel = Titles("osu! path")
		osu_pathInput = Big_Textbox()

		output_pathLabel = Titles("Output path:")
		output_pathInput = Big_Textbox()

		duration_slider = Slider() 
		duration_start = Small_Titles("Start time:")
		#Horizontal
		width_label = Small_Titles("Width:")
		width_input = Small_Textbox()

		fps_label = Small_Titles("Width:")
		fps_input = Small_Textbox()

		codec_label = Small_Titles("Video codec:")
		codec_input = Small_Textbox()

		process_label = Small_Titles("Process:")
		process_input = Small_Textbox()

		vertical_widgets = []
		horizontal_widgets = []

		vertical_widgets.extend((render_, separator, osu_pathLabel, osu_pathInput, output_pathLabel, output_pathInput, duration_start, duration_slider, process_label, process_input))
		horizontal_widgets.extend((width_label, width_input, fps_label, fps_input, codec_label, codec_input))
		for x in range(len(vertical_widgets)):
			if x == 1:
				continue
			self.gridLayout.addWidget(vertical_widgets[x], x, 0)
		self.gridLayout.addWidget(separator,1, 0, 1, 3)

		for x in range(len(horizontal_widgets)):
			self.gridLayout.addWidget(horizontal_widgets[x], x+2, 1)

		self.gridLayout.setRowStretch(100,1)
		#scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		print("settings")





