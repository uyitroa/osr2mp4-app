from PyQt5 import QtWidgets, QtCore
import os


class SkinDropDown(QtWidgets.QComboBox):
    def __init__(self, parent):
        super(SkinDropDown, self).__init__(parent)
        self.main_window = parent
        self.img_drop = os.path.join(parent.app_directory, "images/Drop_Scale.png").replace("\\", "/")
        self.img_listview = os.path.join(parent.app_directory, "images/listview.png").replace("\\", "/")
        self.setMinimumSize(QtCore.QSize(30, 30))
        self.setup()

    def setup(self):
        self.main_window.skin_layout_dropdown.addWidget(self)
        skin_path = os.path.join(self.main_window.current_config["osu! path"], r"D:\Games\osu!\Skins")
        for skin in os.listdir(skin_path):
            self.addItem(skin)

        self.setStyleSheet("""
                		QComboBox {
                			 border-image : url(%s);
                			 color: white;
                			 font-size: 9pt;
                		}

                		QComboBox::drop-down {
                			 border-bottom-right-radius: 1px;
                		}

                		QListView {
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

