import json
import logging
from copy import copy

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMenuBar, QAction
from abspath import pppath
from config_data import current_ppsettings
from osr2mp4.global_var import defaultppconfig


class PPMenu(QMenuBar):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.file = self.addMenu("PP Config")

		self.saveaction = QAction("Save", self)
		self.file.addAction(self.saveaction)
		self.saveaction.setShortcuts(QKeySequence("Ctrl+S"))
		self.saveaction.triggered.connect(self.save)

		self.resetaction = QAction("Reset", self)
		self.file.addAction(self.resetaction)
		self.resetaction.setShortcuts(QKeySequence("Ctrl+R"))
		self.resetaction.triggered.connect(self.reset)

	def save(self):
		try:
			ppsettings = copy(current_ppsettings)
			ppsettings["Rgb"] = eval(str(ppsettings["Rgb"]))
			ppsettings["Hitresult Rgb"] = eval(str(ppsettings["Hitresult Rgb"]))
			self.parent.ppsample.ppcounter.loadsettings(ppsettings)
			self.parent.ppsample.ppcounter.loadimg()
			self.parent.ppsample.hitresultcounter.loadsettings(ppsettings)
			self.parent.ppsample.hitresultcounter.loadimg()
			self.parent.updatepp()
		except Exception as e:
			print(repr(e))
			print(ppsettings)
			logging.error(repr(e))
			logging.info(ppsettings)
			return
		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]

		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()

	def reset(self):
		ppsettings = defaultppconfig
		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]
		self.parent.ppsample.ppcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.ppcounter.loadimg()
		self.parent.ppsample.hitresultcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.hitresultcounter.loadimg()
		self.parent.pplayout.updatevalue()
		self.parent.updatepp()
		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()
