from PyQt5.QtWidgets import QFileDialog

from SettingComponents.Components.Textbox import ParentTextbox


class PathBox(ParentTextbox):
	def __init__(self, key=None, jsondata=None, datadict=None, func=None):
		super().__init__(key=key, jsondata=jsondata, datadict=datadict)

		self.default_width = 250
		self.default_height = 10

		self.setFixedWidth(self.default_width)
		self.setReadOnly(True)

		file_type = jsondata["filetype"]
		self.file_type = ""
		self.func = func  # function to call after choosing path (most of the time it will be none anyway except for pp custom)
		if type(file_type).__name__ == "list":
			for i in file_type:
				self.file_type += "*" + i + " "
		else:
			self.file_type = "*" + file_type

		self.browsepath = "home"

	def updatevalue(self):
		self.setToolTip(str(self.current_data[self.key]))
		self.setText(str(self.current_data[self.key]))
		if self.func is not None:
			self.func()

	def mousePressEvent(self, event):
		if self.file_type == "*Folder":
			filename = QFileDialog.getExistingDirectory(None, "Select Directory", self.browsepath)
		else:
			filename = QFileDialog.getOpenFileName(self, 'Open file', self.browsepath, "A files ({})".format(self.file_type))[0]

		if filename == "":
			return

		self.current_data[self.key] = filename
		self.updatevalue()

