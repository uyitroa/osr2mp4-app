from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
import sys
from pathlib import Path

class Label(QLabel):
#fuck	
    def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,parent=None):
        super(Label, self).__init__(parent)
        self.width,self.height,self.file_type = width,height,file_type
        #Setting image for default start
        self.start_button = QPixmap("res/" + img)
        self.start_button = self.start_button.scaled(width,height)
        #setting image for hover start
        self.start_button_hover = QPixmap("res/" + img_hover)
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
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Subscribe to Raishin Aot")
        self.setStyleSheet("background-color: grey;")
        width,height = 800,600
        x_pos,button_y = 0,20
        logo = Label(10,button_y,278,278,"osr2mp4_logo.png","osr2mp4_logo.png","",self)
        self.image_list = ["select_osr.png","select_osr_hover.png","select_osu.png","select_osu_hover.png","select_skin.png","select_skin_hover.png","output.png","output_hover.png"]
        self.file_type = [".osr",".osu","folder","output"]
        

        
        self.main_buttons = []
        for x in range(0,len(self.image_list) - 1,2):
            button = QLabel()
            self.main_buttons.append(button)
        self.progressBar=Label(0,0,0,0,"","",self)
        self.start=Label(0,0,0,0,"","",self)
        #self.start = Label(progressbar_x + progressbar_width - self.start_width,height-40-self.start_height,self.start_width,self.start_height,"start.png","start_hover.png","",self)

        self.resize(width,height)
        #self.showMaximized()
        self.show()
        
    def resizeEvent(self, event):
        ypos = 20
        
        scale = min(self.height()/469, self.width()/832)
        button_width = int(257 * scale)
        button_height = int(46 * scale)
        
        start_width = int(178 * scale)
        start_height = int(77 * scale)
        
        width,height = self.width(),self.height()
        progressbar_width,progressbar_height = self.width() - 20,30
        progressbar_x,progressbar_y = 10,self.height()-40
        
        tmp_counter,file_typeCounter=0,0
        
        x_pos,button_y = 0,20
        for x in range(len(self.main_buttons),0,-1):
            self.delete_widget(self.main_buttons[x-1],x-1)
        for x in range(0,len(self.image_list) - 1,2):
            button = Label(self.width()-button_width,button_y,button_width,button_height,self.image_list[x],self.image_list[x+1],self.file_type[file_typeCounter],self)
            button_y+=70
            file_typeCounter+=1
            self.main_buttons.append(button)
            button.show()
            
        self.progressBar.setParent(None)
        self.start.setParent(None)
        
        self.progressBar = Label(progressbar_x,progressbar_y,self.width()-20,32,"progressbar.png","progressbar.png","",self)
        self.progressBar.show()
        
        self.start = Label(progressbar_x + progressbar_width - start_width,height-40-start_height,start_width,start_height,"start.png","start_hover.png","",self)
        self.start.show()
    def delete_widget(self,widget,index):
        widget.setParent(None)
        self.main_buttons.pop(index)
    def loadImg(self,img_dir,width,height):
        pixmap = QPixmap("res/" + img_dir)
        pixmap = pixmap.scaled(width,height)
        return pixmap
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
