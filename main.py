from PyQt5 import QtWidgets, QtCore
from HomeComponents.SelectOsr import SelectOsr
from HomeComponents.SelectBeatmap import SelectBeatmap
from HomeComponents.Osr2mp4Logo import Osr2mp4Logo
from HomeComponents.FilesPath import MapPath, OsrPath
from HomeComponents.AutoReplayCheckBox import AutoReplayCheckBox
from HomeComponents.SkinDropDown import SkinDropDown
from PopupComponents.PopupWindow import PopupWindow
from PopupComponents.SelectOsuFolder import SelectOsuFolder
from PopupComponents.SelectOutputFolder import SelectOutputFolder
from Custom.CustomFunctions import check_data_paths
from Custom.CustomQtFunctions import unblur_widget
import os
import json


class MyWidget(QtWidgets.QWidget):
    def __init__(self, ):
        super().__init__()
        window_width, window_height, window_starting_point = 832, 469, 0

        self.setGeometry(window_starting_point, window_starting_point, window_width, window_height)
        self.app_directory = os.path.abspath(os.getcwd())
        self.popupable_bool = True
        self.setup_config()
        self.create_layouts()
        self.setup_layouts()
        self.osu_logo = Osr2mp4Logo(self)

        self.osr_button = SelectOsr(self)
        self.latest_beatmap_text = ""
        self.map_button = SelectBeatmap(self)

        self.osr_path = OsrPath(self)
        self.map_path = MapPath(self)

        self.auto_replay = AutoReplayCheckBox(self)
        self.skin_drop = SkinDropDown(self)

        self.home_widgets = [self.osu_logo, self.osr_button, self.map_button, self.map_path, self.osr_path]
        self.popup_widgets = []
        self.hidden_widgets = []
        check_data_paths(self)


        self.setStyleSheet("background-color: rgb(33, 30, 33);")

        self.center()
        self.show()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self)
        self.sub_horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.button_vertical_layout = QtWidgets.QVBoxLayout(self)

        self.auto_replay_layout = QtWidgets.QHBoxLayout(self)
        self.auto_replay_layout_checkbox = QtWidgets.QHBoxLayout(self)

        self.path_box_storage = QtWidgets.QVBoxLayout(self)
        self.path_vertical_layout = QtWidgets.QVBoxLayout(self)

        self.skin_layout = QtWidgets.QHBoxLayout(self)
        self.skin_layout_dropdown = QtWidgets.QHBoxLayout(self)

        self.logo_horizontal = QtWidgets.QHBoxLayout(self)

    def setup_layouts(self):

        self.main_layout.addLayout(self.logo_horizontal, 5)
        self.main_layout.addLayout(self.main_vertical_layout, 3)
        self.main_vertical_layout.addLayout(self.button_vertical_layout, 1)

        #for auto_replay checkbox's horizontal padding
        self.auto_replay_layout.addWidget(QtWidgets.QLabel(self), 1)
        self.auto_replay_layout.addLayout(self.auto_replay_layout_checkbox, 50)

        self.main_vertical_layout.addLayout(self.auto_replay_layout, 1)
        self.path_box_storage.addLayout(self.path_vertical_layout, 3)
        #padding for the 2 pathbox
        self.path_box_storage.addWidget(QtWidgets.QLabel(self), 10)
        self.sub_horizontal_layout.addWidget(QtWidgets.QLabel(self), 4)
        self.sub_horizontal_layout.addLayout(self.path_box_storage, 25)
        self.main_vertical_layout.addLayout(self.sub_horizontal_layout, 3)

        #for skin dropdown padding
        self.skin_layout.addWidget(QtWidgets.QLabel(self), 1)
        self.skin_layout.addLayout(self.skin_layout_dropdown, 2)
        self.main_vertical_layout.addLayout(self.skin_layout, 1)

    def resizeEvent(self, event):
        if self.popupable_bool:
            self.popup_window.resize_()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def setup_config(self):
        data_directory = os.path.join(self.app_directory, "data/config.json")
        with open(data_directory, 'r') as f:
            self.current_config = json.load(f)

    def show_popups(self):
        self.popup_window = PopupWindow(self)
        self.select_osu_folder = SelectOsuFolder(self)
        self.select_output_folder = SelectOutputFolder(self)
        self.popup_widgets.extend([self.popup_window, self.select_osu_folder, self.select_output_folder])

    def delete_popups(self):
        for widget in self.popup_widgets:
            widget.visible = False
            widget.deleteLater()

    def unblur_home_components(self):
        unblur_widget(self.home_widgets)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MyWidget()
    w.show()
    app.exec()
