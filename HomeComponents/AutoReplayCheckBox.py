from PyQt5 import QtWidgets, QtCore


class AutoReplayCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent):
        super(AutoReplayCheckBox, self).__init__(parent)
        self.setText("Auto Replay")
        self.checked_img = "images/checked.png"
        self.unchecked_img = "images/unchecked.png"
        self.setMinimumSize(QtCore.QSize(50, 21))
        self.setGeometry(518, 144, 185, 21)
        #self.setStyleSheet("color: white;font-size:15pt;")
        self.setStyleSheet("""
                QCheckBox {
                color: white;font-size:15pt;
                }
                QCheckBox::indicator {
                    width: 25;
                    height: 25;
		        }
        		QCheckBox::indicator:checked {
        		    border-image: url(%s);
        		}
        		QCheckBox::indicator:unchecked {
        		    border-image: url(%s);
        		}
        					""" % (self.checked_img, self.unchecked_img))