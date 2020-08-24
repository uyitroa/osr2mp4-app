import glob
import json
import os

from PyQt5.QtWidgets import QLabel
from autologging import traced, logged
from BaseComponents.ComboBox import ComboBox
from abspath import abspath
import logging

from config_data import current_config
from helper.datahelper import save


@logged(logging.getLogger(__name__))
@traced("changesize", "blur_me", exclude=True)
class LanguageDropDown(ComboBox):
	def __init__(self, parent):
		super().__init__(parent)

		self.text = QLabel(self)

		self.default_x = 5
		self.default_y = 5
		self.default_width = 0.4
		self.default_height = 0.5

		self.langnames = {}

		super().setup()
		self.get_langs()

		langpath = os.path.join(abspath, "langs", "en")
		with open(os.path.join(langpath, "tooltips.json")) as f:
			self.default_tooltips = json.load(f)

		with open(os.path.join(langpath, "options.json")) as f:
			self.default_options = json.load(f)

		with open(os.path.join(langpath, "options_headers.json")) as f:
			self.default_headers = json.load(f)

		with open(os.path.join(langpath, "options_setup.json")) as f:
			self.default_setup = json.load(f)

		language = current_config.get("Language", "English")
		self.setCurrentIndex(self.findText(language))

	def activated_(self, index):
		current_config["Language"] = self.itemText(index)
		self.main_window.hidesettings()
		self.main_window.popup_window.reload_popupwindow()
		self.main_window.settingspage.reload_settings()
		save()

	def loadlang(self, filename, defaultvalues):
		try:
			with open(filename, encoding='utf-8') as f:
				options = json.load(f)
		except Exception as e:
			logging.error("from languagedropdown getlangs", repr(e))
			options = defaultvalues

		for key in defaultvalues:
			if key not in options:
				options[key] = defaultvalues[key]
		return options
	
	def changesize(self):
		pass

	def getlang(self):
		langpath = os.path.join(abspath, "langs", self.langnames.get(self.currentText(), "en"))
		tooltips = self.loadlang(os.path.join(langpath, "tooltips.json"), self.default_tooltips)
		options = self.loadlang(os.path.join(langpath, "options.json"), self.default_options)
		headers = self.loadlang(os.path.join(langpath, "options_headers.json"), self.default_headers)

		return options, tooltips, headers

	def getlang_popupwindow(self):
		langpath = os.path.join(abspath, "langs", self.langnames.get(self.currentText(), "en"))
		setup = self.loadlang(os.path.join(langpath, "options_setup.json"), self.default_setup)

		return setup


	def get_langs(self):
		langlist = [f for f in glob.glob(os.path.join(abspath, "langs/*"))]
		for x in langlist:
			try:
				langsh = os.path.basename(x)
				with open(os.path.join(x, "lang.txt"), "r", encoding="utf-8") as f:
					langname = f.read().strip()
				self.addItem(langname)
				self.langnames[langname] = langsh
			except Exception as e:
				logging.error("from get_langs", repr(e))
		self.setCurrentIndex(self.findText("en"))


