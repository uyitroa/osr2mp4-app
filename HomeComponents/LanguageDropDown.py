import glob
import json
import os
from autologging import traced, logged
from BaseComponents.ComboBox import ComboBox
from abspath import abspath
import logging

from config_data import current_config


@logged(logging.getLogger(__name__))
@traced("changesize", "blur_me", exclude=True)
class LanguageDropDown(ComboBox):
	def __init__(self, parent):
		super().__init__(parent)

		self.default_x = 10
		self.default_y = 10
		self.default_width = 0.4
		self.default_height = 0.5

		super().setup()
		self.get_langs()

		langpath = os.path.join(abspath, "langs", "English")
		with open(os.path.join(langpath, "tooltips.json")) as f:
			self.default_tooltips = json.load(f)

		with open(os.path.join(langpath, "options.json")) as f:
			self.default_options = json.load(f)

		with open(os.path.join(langpath, "options_headers.json")) as f:
			self.default_headers = json.load(f)

		language = current_config.get("Language", "English")
		self.setCurrentIndex(self.findText(language))

	def activated_(self, index):
		current_config["Language"] = self.itemText(index)
		self.main_window.hidesettings()
		self.main_window.settingspage.reload_settings()

	def loadlang(self, filename, defaultvalues):
		try:
			with open(filename) as f:
				options = json.load(f)
		except Exception as e:
			logging.error("from languagedropdown getlangs", repr(e))
			options = defaultvalues

		for key in defaultvalues:
			if key not in options:
				options[key] = defaultvalues[key]
		return options

	def getlang(self):
		langpath = os.path.join(abspath, "langs", self.currentText())
		tooltips = self.loadlang(os.path.join(langpath, "tooltips.json"), self.default_tooltips)
		options = self.loadlang(os.path.join(langpath, "options.json"), self.default_options)
		headers = self.loadlang(os.path.join(langpath, "options_headers.json"), self.default_headers)

		return options, tooltips, headers

	def get_langs(self):
		langlist = [f for f in glob.glob(os.path.join(abspath, "langs/*"))]
		for x in langlist:
			langname = os.path.basename(x)
			self.addItem(langname)
		self.setCurrentIndex(0)
