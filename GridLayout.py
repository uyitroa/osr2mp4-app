import math

from PyQt5.QtWidgets import QGridLayout


class GridLayout(QGridLayout):
	def __init__(self, QWidget):
		super().__init__(QWidget)
		self.maxwidth = 500
		self.maxheight = 500
		self.colstart = 2
		self.rowcounter = [0]

	def smart_addWidget(self, QWidget, col):

		rowspan = 1
		colspan = 1

		while col + 1 > len(self.rowcounter):
			self.rowcounter.append(self.colstart)

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