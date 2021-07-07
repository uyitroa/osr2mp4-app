from PyQt5 import QtWidgets, QtCore
import os


class AutoReplayCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent):
        super(AutoReplayCheckBox, self).__init__(parent)
        self.main_window = parent
        self.setText("Use Auto Replay")
        self.checked_img = os.path.join(parent.app_directory, "images/checked.png").replace("\\", "/")
        self.unchecked_img = os.path.join(parent.app_directory, "images/unchecked.png").replace("\\", "/")
        self.setMinimumSize(QtCore.QSize(10, 10))
        self.main_window.auto_replay_layout_checkbox.addWidget(self)
        self.setStyleSheet("""
                QCheckBox {
                color: white;font-size:15pt;
                font-weight:bold;
                }
                QCheckBox::indicator {
                    width: 25;
                    height: 25;
		        }
        		QCheckBox::indicator:checked {
        		    image: url(%s);
        		}
        		QCheckBox::indicator:unchecked {
        		    image: url(%s);
        		}
        					""" % (self.checked_img, self.unchecked_img))