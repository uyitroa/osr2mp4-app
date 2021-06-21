from PyQt5 import QtWidgets
from HomeComponents.SelectOsr import SelectOsr
from HomeComponents.SelectBeatmap import SelectBeatmap
from HomeComponents.Osr2mp4Logo import Osr2mp4Logo
from HomeComponents.FilesPath import MapPath, OsrPath
from HomeComponents.AutoReplayCheckBox import AutoReplayCheckBox
from HomeComponents.SkinDropDown import SkinDropDown
from PopupComponents.PopupWindow import PopupWindow
from PopupComponents.SelectOsuFolder import SelectOsuFolder

from Custom.CustomQtFunctions import blur_widget
from Custom.CustomFunctions import check_data_paths
import os


class MyWidget(QtWidgets.QWidget):
    def __init__(self, ):
        super().__init__()

        window_width, window_height = 832, 469
        self.window_startingpoint = 0
        self.setGeometry(self.window_startingpoint, self.window_startingpoint, window_width, window_height)
        self.app_directory = os.path.abspath(os.getcwd())
        self.main_layout = QtWidgets.QGridLayout(self)
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


        self.setStyleSheet("background-color: rgb(30, 30, 33);")

        self.center()
        self.show()

    def resizeEvent(self, event):
        pass

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
