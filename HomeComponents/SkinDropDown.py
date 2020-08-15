import glob
import os
from autologging import traced, logged
from BaseComponents.ComboBox import ComboBox
from config_data import current_config
from helper.datahelper import save
import logging

from helper.username_parser import read_properties_file


@logged(logging.getLogger(__name__))
@traced("changesize", "blur_me", exclude=True)
class SkinDropDown(ComboBox):
	def __init__(self, parent):
		super().__init__(parent)

		self.default_x = 640
		self.default_y = 255
		self.setToolTip("Skin that will be used in the video")

		self.addItems(["Default Skin"])

		super().setup()

	def activated_(self, index):
		current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", self.itemText(index))
		save()
		logging.info(current_config["Skin path"])

	def get_skins(self):
		name = "Default Skin"
		if os.path.isdir(current_config["Skin path"]):
			name = os.path.basename(current_config["Skin path"])

		skin_list = [f for f in glob.glob(os.path.join(current_config["osu! path"], "Skins/*"))]
		for x in skin_list:
			skinname = os.path.basename(x)
			self.addItem(skinname)
		self.setCurrentIndex(self.findText(name))

	def set_skin_osu(self):
		c = glob.glob(os.path.join(current_config["osu! path"], "osu!.*.cfg"))
		logging.info(c)
		if c:
			cfg = [x for x in c if "osu!.cfg" not in x]
			logging.info(cfg)
			props = read_properties_file(cfg[0])
			name = props['skin']
			current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", name)
			self.setCurrentIndex(self.findText(name))
