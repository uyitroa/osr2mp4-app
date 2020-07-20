from PyQt5.QtWidgets import QFileDialog

from SettingComponents.Components.Textbox import ParentTextbox


class PathBox(ParentTextbox):
	def __init__(self, parent=None, jsondata=None):
		super().__init__(parent=parent, jsondata=jsondata)

		self.default_width = 250
		self.default_height = 10

		self.setFixedWidth(self.default_width)
		self.setReadOnly(True)

		file_type = jsondata["option_config"]["filetype"]
		self.file_type = ""
		if type(file_type).__name__ == "list":
			for i in file_type:
				self.file_type += "*" + i + " "
		else:
			self.file_type = "*" + file_type

		self.browsepath = "home"
		print("OK", self.file_type)

	def updatevalue(self):
		self.setToolTip(str(self.current_data[self.key]))
		self.setText(str(self.current_data[self.key]))

	def mousePressEvent(self, event):
		if self.file_type == "*Folder":
			filename = QFileDialog.getExistingDirectory(None, "Select Directory", self.browsepath)
		else:
			filename = QFileDialog.getOpenFileName(self, 'Open file', self.browsepath, "A files ({})".format(self.file_type))[0]

		if filename == "":
			return

		self.current_data[self.key] = filename
		self.updatevalue()
