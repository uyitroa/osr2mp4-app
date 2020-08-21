import os
import webbrowser

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QCheckBox

from SettingComponents.Components.ToolTip import ClickableTooltip
from abspath import abspath
from config_data import current_config, current_settings


class CheckBox(QCheckBox):
	def __init__(self, key=None, jsondata=None, datadict=None):
		super().__init__()

		self.img_uncheck = os.path.join(abspath, "res/Uncheck_HD.png")
		self.img_check = os.path.join(abspath, "res/Check_HD.png")

		self.box_width = 20
		self.box_height = 20
		self.default_fontsize = 14
		self.cur_size = 1

		textstr = jsondata.get("name", key)
		self.text = "  " + textstr + "     "
		self.setText(textstr)
		self.curfont = self.font()

		self.default_width = self.box_width * 1.1 + self.textwidth()
		self.default_height = self.box_height * 1.1

		self.key = key

		if datadict is not None:
			self.current_data = datadict
		else:
			if key in current_config:
				self.current_data = current_config
			else:
				self.current_data = current_settings

		if self.key not in self.current_data:
			self.current_data[self.key] = False

		if bool(self.current_data[self.key]):
			self.setCheckState(QtCore.Qt.Checked)
		else:
			self.setCheckState(QtCore.Qt.Unchecked)

		tip = jsondata.get("desc", "")
		self.setToolTip(tip)
		self.installEventFilter(self)

		super().stateChanged.connect(self.stateChanged)

	def textwidth(self):
		return self.fontMetrics().boundingRect(self.text).width() * 2

	def textheight(self):
		return self.fontMetrics().boundingRect(self.text).height() * 2

	def updatevalue(self):
		if bool(self.current_data[self.key]):
			self.setCheckState(QtCore.Qt.Checked)
		else:
			self.setCheckState(QtCore.Qt.Unchecked)

	def setFixedWidth(self, p_int):
		scale = p_int / self.default_width
		self.cur_size = scale

		self.setStyleSheet("""
		QCheckBox {
			font-weight: bold;
			color: white;
		}
		QCheckBox::indicator {
		    width: %fpx;
		    height: %fpx;
		}
		QCheckBox::indicator:unchecked {
		    border-image: url(%s);
		    color: blue;
		}
		QCheckBox::indicator:checked {
		    border-image: url(%s);
		}
					""" % (self.box_width * scale, self.box_height * scale, self.img_uncheck, self.img_check))

		self.curfont.setPointSize(self.default_fontsize * scale)
		self.setFont(self.curfont)

		super().setFixedWidth(p_int)

	@QtCore.pyqtSlot(int)
	def stateChanged(self, p_int):
		if p_int == 2:
			self.current_data[self.key] = True
		else:
			self.current_data[self.key] = False

	def tooltip_link_clicked(self, url):
		webbrowser.open(url)

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.ToolTip and source.toolTip():
			toolTip = ClickableTooltip.showText(
				QtGui.QCursor.pos(), source.toolTip(), source)
			toolTip.linkActivated.connect(self.tooltip_link_clicked)
			return True
		return super().eventFilter(source, event)
