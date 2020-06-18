from PyQt5.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
	def __init__(self, title, jsondata=None):
		super().__init__()
		self.default_width = 20
		self.default_height = 20
		self.setStyleSheet("""
QCheckBox::indicator {
    width: 20px;
    height: 20px;
}
QCheckBox::indicator:unchecked {
    image: url(res/Uncheck_HD.png);
}
QCheckBox::indicator:checked {
    image: url(res/Check_HD.png);
}
font: bold 14px;color:white
			""")
		self.setText(title)

		# Do your setStylesheet here
