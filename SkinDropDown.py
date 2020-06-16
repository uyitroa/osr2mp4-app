import configparser
import glob
import io
import os

from PyQt5.QtWidgets import QComboBox

from config_data import current_config


def read_properties_file(file_path):
	with open(file_path) as f:
		config = io.StringIO()
		config.write('[dummy_section]\n')
		config.write(f.read().replace('%', '%%'))
		config.seek(0, os.SEEK_SET)

		cp = configparser.SafeConfigParser()
		cp.readfp(config)

		return dict(cp.items('dummy_section'))


class SkinDropDown(QComboBox):
	def __init__(self, parent):
		super(SkinDropDown, self).__init__(parent)
		self.activated.connect(self.activated_)
		self.main_window = parent
		self.counter = 0
		self.addItems(["Default Skin"])
		self.setStyleSheet("""QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}""")

	def activated_(self, index):
		current_config["Skin path"] = current_config["osu! path"] + "/Skins/" + self.itemText(index)
		print(current_config["Skin path"])

	def get_skins(self, path):
		self.addItems(self.main_window.skins_directory)
		self.get_configInfo(path)

	def get_configInfo(self, path):
		if path != "":
			cfg = glob.glob(path + "/*.cfg")
			props = read_properties_file(cfg[1])
			name = props['skin']

			self.setCurrentIndex(self.findText(name))

			current_config["Skin path"] = current_config["osu! path"] + "/Skins/" + name
			skin_list = [f for f in glob.glob(current_config["osu! path"] + "/Skins/*", recursive=True)]
			for x in skin_list:
				index = x.rfind("/")  # find_lastIndex
				index2 = x.rfind("\\")
				if index > index2:
					self.addItems([x[index + 1:len(x)]])
				else:
					self.addItems([x[index2 + 1:len(x)]])
