from PyQt5 import QtWidgets, QtCore
from HomeComponents.SelectOsr import SelectOsr
from HomeComponents.SelectBeatmap import SelectBeatmap
from HomeComponents.Osr2mp4Logo import Osr2mp4Logo
from HomeComponents.FilesPath import MapPath, OsrPath
from HomeComponents.AutoReplayCheckBox import AutoReplayCheckBox
from HomeComponents.SkinDropDown import SkinDropDown
from PopupComponents.PopupWindow import PopupWindow
from PopupComponents.SelectOsuFolder import SelectOsuFolder

from Custom.CustomFunctions import check_data_paths
import os

class MyWidget(QtWidgets.QWidget):
    def __init__(self, ):
        super().__init__()

        window_width, window_height, window_starting_point = 832, 469, 0
        self.setGeometry(window_starting_point, window_starting_point, window_width, window_height)
        self.app_directory = os.path.abspath(os.getcwd())
        self.create_layouts()
        self.setup_layouts()
        self.osu_logo = Osr2mp4Logo(self)
        self.osr_button = SelectOsr(self)
        self.map_button = SelectBeatmap(self)

        self.map_path = MapPath(self)
        self.osr_path = OsrPath(self)

        #self.auto_replay = AutoReplayCheckBox(self)
        #self.skin_drop = SkinDropDown(self)

        #home_widgets = [self.osu_logo, self.osr_button, self.map_button, self.map_path, self.osr_path, self.auto_replay, self.skin_drop]
        self.hidden_widgets = []
        check_data_paths(self.app_directory, self)


        self.setStyleSheet("background-color: rgb(33, 30, 33);")

        self.center()
        self.show()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self)
        self.sub_horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.button_vertical_layout = QtWidgets.QVBoxLayout(self)

        self.path_box_padding = QtWidgets.QVBoxLayout(self)
        self.path_box_storage = QtWidgets.QVBoxLayout(self)
        self.path_box_vertical_padding = QtWidgets.QVBoxLayout(self)


        self.path_vertical_layout = QtWidgets.QVBoxLayout(self)
        self.logo_horizontal = QtWidgets.QHBoxLayout(self)



    def setup_layouts(self):
        self.main_layout.addLayout(self.logo_horizontal, 4)
        self.main_layout.addLayout(self.main_vertical_layout, 3)
        self.main_vertical_layout.addLayout(self.button_vertical_layout, 1)
        
        self.path_box_storage.addLayout(self.path_vertical_layout, 1)
        self.path_box_storage.addLayout(self.path_box_vertical_padding, 10)
        w = QtWidgets.QWidget(self)
        w.setStyleSheet("background-color:transparent;")
        self.path_box_vertical_padding.addWidget(w)

        self.sub_horizontal_layout.addLayout(self.path_box_padding, 1)
        self.sub_horizontal_layout.addLayout(self.path_box_storage, 2)

        self.main_vertical_layout.addLayout(self.sub_horizontal_layout, 3)

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def get_hidden_popup(self):
        return
        popup_window = PopupWindow(self)
        select_osu_folder = SelectOsuFolder(self)
        #self.hidden_widgets.extend([popup_window, select_osu_folder])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MyWidget()
    w.show()
    app.exec()
