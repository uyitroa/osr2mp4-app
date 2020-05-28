from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
import ctypes,sys,imagesize
from pathlib import Path

class Label(QLabel):

    def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,parent=None):
        super(Label, self).__init__(parent)
        self.width,self.height,self.file_type = width,height,file_type
        #Setting image for default start
        self.start_button = QPixmap(img)
        self.start_button = self.start_button.scaled(width,height)
        #setting image for hover start
        self.start_button_hover = QPixmap(img_hover)
        self.start_button_hover = self.start_button_hover.scaled(width,height)
        self.setPixmap(self.start_button)
        
        self.setGeometry(x_pos,y_pos,width,height)

    def mousePressEvent(self,QEvent):
        if not self.file_type == "":
            self.openFileNameDialog()
    def enterEvent(self, QEvent):
        self.setPixmap(self.start_button_hover)

    def leaveEvent(self, QEvent):
        self.setPixmap(self.start_button)
 
    def openFileNameDialog(self):
        if self.file_type != "folder" and  self.file_type != "output":
            print(self.file_type)
            home_dir = str(Path.home())
            fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type,self.file_type))
        else:
            home_dir = str(Path.home())
            fname = QFileDialog.getExistingDirectory(None, ("Select Directory"), home_dir)
        print(fname)
        return fname

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = ctypes.windll.user32
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Subscribe to Raishin Aot")
        self.setStyleSheet("background-color: grey;")
        width,height = 800,500
        x_pos,y_pos = 0,20
        logo = Label(10,y_pos,278,278,"osr2mp4_logo.png","osr2mp4_logo.png","",self)

        image_list = ["select_osr.png","select_osr_hover.png","select_osu.png","select_osu_hover.png","select_skin.png","select_skin_hover.png","output.png","output_hover.png"]
        file_type = [".osr",".osu","folder","output"]
        file_typeCounter = 0
        scale = int(height/469)
        button_width = 257 * scale
        button_height = 46 * scale

        start_width = 178 * scale
        start_height = 77 * scale
        for x in range(0,len(image_list) - 1,2):
            button = Label(width-button_width,y_pos,button_width,button_height,image_list[x],image_list[x+1],file_type[file_typeCounter],self)
            y_pos+=50
            file_typeCounter+=1

        progressbar_width,progressbar_height = width - 20,30
        progressbar_x,progressbar_y = 10,height-40
        
        progressBar = Label(progressbar_x,progressbar_y,progressbar_width,32,"progressbar.png","progressbar.png","",self)
        
        start = Label(progressbar_x + progressbar_width - start_width,height-40-start_height,start_width,start_height,"start.png","start_hover.png","",self)

        self.resize(width,height)
        #self.showMaximized()
        self.show()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
