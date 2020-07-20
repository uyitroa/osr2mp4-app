import json

from PyQt5.QtWidgets import QPushButton

from config_data import current_ppsettings


from osr2mp4.osr2mp4 import defaultppconfig


class SaveButton(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		windowheight = parent.windowheight
		imagewidth = parent.ppsample.settings.width

		self.setGeometry(imagewidth, windowheight * 0.92, 100, 50)
		self.setText("Save")

	def mousePressEvent(self, event):
		try:
			ppsettings = json.loads(self.parent.hugetextbox.toPlainText())
		except Exception as e:
			logging.error(repr(e))
			return

		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]
		self.parent.ppsample.ppcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.ppcounter.loadimg()
		self.parent.ppsample.hitresultcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.hitresultcounter.loadimg()
		self.parent.updatepp()
		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()


class Reset(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		windowheight = parent.windowheight
		imagewidth = parent.ppsample.settings.width

		self.setGeometry(imagewidth + 100, windowheight * 0.92, 100, 50)
		self.setText("Reset")

	def mousePressEvent(self, event):
		ppsettings = defaultppconfig
		for k in ppsettings.keys():
			current_ppsettings[k] = ppsettings[k]
		self.parent.ppsample.ppcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.ppcounter.loadimg()
		self.parent.ppsample.hitresultcounter.loadsettings(current_ppsettings)
		self.parent.ppsample.hitresultcounter.loadimg()
		self.parent.hugetextbox.setPlainText(json.dumps(current_ppsettings, indent=4))
		self.parent.updatepp()
		with open(pppath, 'w+') as f:
			json.dump(current_ppsettings, f, indent=4)
			f.close()

