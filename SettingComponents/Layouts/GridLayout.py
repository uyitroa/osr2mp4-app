import math

from PyQt5.QtWidgets import QGridLayout


class GridLayout(QGridLayout):
	def __init__(self, QWidget, vspacing=3, hspacing=100):
		super().__init__(QWidget)
		self.maxwidth = 300
		self.maxheight = 500
		self.rowcounter = [0]
		self.headerrow = 0
		self.vertical_spacing = vspacing
		self.horizontal_spacing = hspacing
		self.setHorizontalSpacing(self.horizontal_spacing)
		self.setVerticalSpacing(self.vertical_spacing)
		

	def smart_addWidget(self, QWidget, col):

		rowspan = 1
		colspan = 1

		while col + 1 > len(self.rowcounter):
			self.rowcounter.append(self.headerrow)

		if type(QWidget).__name__ == "Separator":
			self.headerrow = self.rowcounter[col] + 1
			for x in range(len(self.rowcounter)):
				self.rowcounter[x] = self.headerrow
			self.rowcounter[col] -= 1

		row = self.rowcounter[col]

		if QWidget.width() > self.maxwidth:
			colspan = math.ceil(QWidget.width() / self.maxwidth)
		if QWidget.height() > self.maxheight:
			rowspan = math.ceil(QWidget.height() / self.maxheight)

		super().addWidget(QWidget, row, col, rowspan, colspan)

		self.rowcounter[col] += 1

	def addWidget(self, QWidget, row, col, rowspan=1, colspan=1):
		while col + 1 > len(self.rowcounter):
			self.rowcounter.append(0)

		self.rowcounter[col] += 1

		super().addWidget(QWidget, row, col, rowspan, colspan)

	def changesize(self, scale):
		for x in range(self.count()):
			item = self.itemAt(x).widget()

			if type(item).__name__ == "QLabel":
				continue

			width = item.default_width * scale
			height = item.default_height * scale
			item.setFixedWidth(width)
			item.setFixedHeight(height)

	def updatevalue(self):
		for x in range(self.count()):
			item = self.itemAt(x).widget()

			if type(item).__name__ == "QLabel":
				continue

			item.updatevalue()
