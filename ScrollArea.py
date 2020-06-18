from PyQt5 import QtWidgets
from PyQt5 import QtCore

from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Scrollbar import Scrollbar
from Separator import Separator
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
import json
from CheckBox import CheckBox


class ScrollArea:
	def __init__(self, parent):
		super().__init__()

		self.main_window = parent

		self.default_width, self.default_height = None, None
		self.default_x, self.default_y = None, None

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider, "CheckBox": CheckBox}

		self.layout = QtWidgets.QHBoxLayout(parent)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		scrollAreaWidgetContents.setStyleSheet("background: transparent;border: none;")

		self.gridLayout = GridLayout(scrollAreaWidgetContents)

		self.scrollArea = Scrollbar(parent, self.gridLayout)
		self.scrollArea.setWidget(scrollAreaWidgetContents)
		self.layout.addWidget(self.scrollArea)
		self.scrollArea.horizontalScrollBar().setEnabled(False);
		self.scrollArea.horizontalScrollBar().setEnabled(True);

	def setup(self):
		self.layout.setGeometry(QtCore.QRect(self.default_x, self.default_y, self.default_width, self.default_height))

	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.changesize(scale)

		x = scale * self.default_x
		y = scale * self.default_y
		width = scale * self.default_width
		height = scale * self.default_height
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))


		self.scrollArea.changesize()


	def load_settings(self):
		with open('gui_config.json') as f:
			data = json.load(f)

		rowcounter = self.gridLayout.count
		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified
				widgetname = data[header][key]["type"]
				Widget = self.widgetlists[widgetname]

				if widgetname == "CheckBox":
					self.gridLayout.addWidget(CheckBox(key), self.gridLayout.rowcounter[column], column)
					continue

				self.gridLayout.smart_addWidget(Small_Titles(key), column)

				
				
					
				self.gridLayout.smart_addWidget(Widget(jsondata=data[header][key]), column)


		for x in range(10):
			render_ = QtWidgets.QLabel("Render Options")
			render_.setStyleSheet("""font: bold 24px;color:white;""")
			self.gridLayout.addWidget(render_, rowcounter(), 0)

		self.scrollArea.raise_()


