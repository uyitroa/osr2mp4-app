from PyQt5 import QtWidgets, QtCore, QtGui
from HomeComponents.SelectOsr import SelectOsr
from HomeComponents.SelectBeatmap import SelectBeatmap
from HomeComponents.Osr2mp4Logo import Osr2mp4Logo
from HomeComponents.FilesPath import MapPath, OsrPath
from HomeComponents.AutoReplayCheckBox import AutoReplayCheckBox
from HomeComponents.SkinDropDown import SkinDropDown
from Custom.CustomFunctions import blur_widget

class MyWidget(QtWidgets.QMainWindow):
    def __init__(self, ):
        super().__init__()
        window_width, window_height = 832, 469
        window_startingpoint = 0
        self.setGeometry(window_startingpoint, window_startingpoint, window_width, window_height)

        self.osu_logo = Osr2mp4Logo(self)
        self.osr_button = SelectOsr(self)
        self.map_button = SelectBeatmap(self)

        self.map_path = MapPath(self)
        self.osr_path = OsrPath(self)
        self.auto_replay = AutoReplayCheckBox(self)
        self.skin_drop = SkinDropDown(self)

        home_widgets = [self.osu_logo, self.osr_button, self.map_button, self.map_path, self.osr_path, self.auto_replay, self.skin_drop]
        #blur_widget(home_widgets)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MyWidget()
    w.show()
    app.exec()
