import configparser
import glob
import io
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QComboBox, QAbstractItemView, QGraphicsBlurEffect

from abspath import abspath
from config_data import current_config
from helper import getsize, changesize
from PyQt5.QtGui import QColor
import logging


def read_properties_file(file_path):
	with open(file_path, encoding="utf-8") as f:

		config = "[dummy_section]\n#" + f.read().replace('%', '%%')
		cp = configparser.SafeConfigParser()
		cp.read_string(config)

		return dict(cp.items('dummy_section'))


class SkinDropDown(QComboBox):
	def __init__(self, parent):
		super(SkinDropDown, self).__init__(parent)

		self.default_x = 600
		self.default_y = 245
		self.img_drop = os.path.join(abspath, "res/Drop_Scale.png")
		self.img_listview = os.path.join(abspath, "res/listview.png")

		self.activated.connect(self.activated_)
		self.main_window = parent

		self.addEmptyItem(0)
		self.addEmptyItem(self.count() - 1)

		self.addItems(["Default Skin"])
		self.setStyleSheet("""QComboBox
			 {
			 border-image : url(%s);
			 color: white;
			 }
			 QComboBox::drop-down
			 {
			 border-bottom-right-radius: 1px;
			 }
			 QListView
			 {
			 outline: none;
			 color: white;
			 font: bold;
			 border-image : url(%s);
			 }
 QScrollBar:vertical {
	 width: 0px;
	 height: 0px;
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	 width: 0px;
	 height: 0px;
	 background: none;
 }

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	 background: none;
 }
 QTextEdit, QListView {
    background-color: rgba(0, 0, 0, 0);
    background-attachment: scroll;
}
 
			 """ % (self.img_drop, self.img_listview))
		self.setItemData(0, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setItemData(1, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setItemData(2, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setup()

	def addEmptyItem(self, index):
		self.addItems([""])
		model = self.model()
		index = model.index(index, self.modelColumn())
		item = model.itemFromIndex(index)
		item.setSelectable(False)

	def setup(self):

		self.default_width, self.default_height = getsize(self.img_drop)
		self.default_width /= 1.5
		self.default_height /= 1.5

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)
		self.setIconSize(QtCore.QSize(self.default_width, self.default_height))
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden
		self.setMaxVisibleItems(7)

		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

	def activated_(self, index):
		current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", self.itemText(index))
		logging.info(current_config["Skin path"])

	def get_skins(self, path):
		self.addItems(self.main_window.skins_directory)
		self.get_configInfo(path)

	def get_configInfo(self, path):
		if path != "":
			c = glob.glob(path + "/*.cfg")
			logging.info(c)
			if not c:
				return
			cfg = [ x for x in c if "osu!.cfg" not in x ]
			logging.info(cfg)
			props = read_properties_file(cfg[0])
			name = props['skin']

			current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", name)
			skin_list = [f for f in glob.glob(os.path.join(current_config["osu! path"],"Skins/*"), recursive=True)]
			for x in skin_list:
				index = x.rfind("/")  # find_lastIndex
				index2 = x.rfind("\\")
				if index > index2:
					self.addItems([x[index + 1:len(x)]])
				else:
					self.addItems([x[index2 + 1:len(x)]])
			self.setCurrentIndex(self.findText(name))

	def changesize(self):
		changesize(self)
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden

	def addItems(self, Iterable, p_str=None):
		super().insertItems(self.count() - 1, Iterable)

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25)
		else:
			self.blur_effect.setBlurRadius(0)
