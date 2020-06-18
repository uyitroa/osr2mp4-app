from PyQt5 import QtWidgets
from PyQt5 import QtCore

from GridLayout import GridLayout
from QLabel import Titles, Small_Titles
from Scrollbar import Scrollbar
from Separator import Separator
from Textbox import Big_Textbox, Small_Textbox
from Slider import Slider
import json


class Scroll_Class:
	def __init__(self, parent):
		super().__init__()

		self.main_window = parent

		self.layout_width, self.layout_height = 550, 450
		self.layout_x, self.layout_y = 20, 20
		self.defaultspacing = 10

		self.widgetlists = {"Big_Textbox": Big_Textbox, "Small_Textbox": Small_Textbox,
		                    "Titles": Titles, "Small_Titles": Small_Titles,
		                    "Slider": Slider}

		self.layout = QtWidgets.QHBoxLayout(parent)
		scrollAreaWidgetContents = QtWidgets.QWidget()
		scrollAreaWidgetContents.setStyleSheet("background: transparent;")

		self.gridLayout = GridLayout(scrollAreaWidgetContents)

		self.scrollArea = Scrollbar(parent, self.gridLayout)
		self.scrollArea.setWidget(scrollAreaWidgetContents)

		self.layout.addWidget(self.scrollArea)

		self.layout.setGeometry(QtCore.QRect(self.layout_x, self.layout_y, self.layout_width, self.layout_height))


		with open('gui_config.json') as f:
			data = json.load(f)

		rowcounter = self.gridLayout.count
		for header in data:
			self.gridLayout.smart_addWidget(Titles(header), 0)
			self.gridLayout.smart_addWidget(Separator(), 0)
			for key in data[header]:
				column = data[header][key].get("Column", 0)  # default to 0 if column is not specified

				self.gridLayout.smart_addWidget(Small_Titles(key), column)

				widgetname = data[header][key]["type"]
				Widget = self.widgetlists[widgetname]
				self.gridLayout.smart_addWidget(Widget(jsondata=data[header][key]), column)


		for x in range(10):
			render_ = QtWidgets.QLabel("Render Options")
			render_.setStyleSheet("""font: bold 24px;color:white;""")
			self.gridLayout.addWidget(render_, rowcounter(), 0)

		self.gridLayout.setSpacing(self.defaultspacing)

		print("settings")


	def changesize(self):
		scale = self.main_window.height() / self.main_window.default_height

		self.gridLayout.setSpacing(scale * self.defaultspacing)

		x = scale * self.layout_x
		y = scale * self.layout_y
		width = scale * self.layout_width
		height = scale * self.layout_height
		self.layout.setGeometry(QtCore.QRect(x, y, width, height))

		for x in range(self.gridLayout.count()):
			item = self.gridLayout.itemAt(x).widget()

			if type(item).__name__ == "QLabel":
				continue

			width = item.default_width * scale
			height = item.default_height * scale
			item.setFixedWidth(width)
			item.setFixedHeight(height)

		self.scrollArea.changesize()
