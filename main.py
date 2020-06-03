from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow,QApplication, QFileDialog,QWidget,QLabel, QPushButton, QGraphicsBlurEffect,QVBoxLayout
import sys
from pathlib import Path
from progressbar_class import progress_bar
current_config = {
  '"osu! path": ': "",
  '"Skin path": ': "",
  '"Beatmap path": ': "",
  '".osr path": ': "",
  '"Default skin path": ': "",
  '"Output path": ': ""
  }
class Label(QPushButton):
        def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,clickable,center,parent=None):

                super(Label, self).__init__(parent)
                self.setMouseTracking(True)
                self.clickable = clickable
                self.width,self.height,self.file_type = width,height,file_type
                #Setting image for default start
                self.img_idle = "res/" + img
                self.img_hover = "res/" + img_hover
                #setting image for hover start
                
                self.setIcon(QtGui.QIcon(self.img_idle))
                self.setGeometry(x_pos,y_pos,width,height)
                self.setIconSize(QtCore.QSize(width,height))
                self.setFlat(True)
                if center:
                        rect = self.frameGeometry()
                        center = QDesktopWidget().availableGeometry().center()
                        rect.moveCenter(center)
                        self.move(rect.topLeft())
        def mousePressEvent(self,QEvent):

                if not self.file_type == "start":
                        self.openFileNameDialog()

                if self.file_type == "start":
                        print("Starting sex ed")
                        f = open("config.json", "w+")
                        f.write(str(current_config))
                        f.close()
        def enterEvent(self, QEvent):
                self.setIcon(QtGui.QIcon(self.img_hover))

        def leaveEvent(self, QEvent):
                self.setIcon(QtGui.QIcon(self.img_idle))
 
        def openFileNameDialog(self):
                if self.clickable:
                        if self.file_type == "Output" or  self.file_type == "Beatmap" or self.file_type == "osu!" or self.file_type == "Skin":
                                home_dir = str(Path.home())
                                fname = QFileDialog.getExistingDirectory(None, ("Select Directory"), home_dir)
                        else:
                                home_dir = str(Path.home())
                                fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type,self.file_type))
                        current_config['"{} path": '.format(self.file_type)] = fname

class Window(QMainWindow):
        def __init__(self):
                super().__init__()
                self.setWindowIcon(QtGui.QIcon("icon.png"))
                self.setWindowTitle("Subscribe to Raishin Aot")
                self.setStyleSheet("background-color: grey;")
                width,height = 1000,600
                x_pos,button_y = 0,20
                self.image_listIdle = ["select_osr.png","select_osu.png"]
                self.image_listHover = ["select_osr_hover.png","select_osu_hover.png"]
                self.file_type = [".osr","osu!","Beatmap","Output"]
                self.main_buttons = []
                for x in range(0,len(self.image_listHover) - 1,2):
                        button = QLabel()
                        self.main_buttons.append(button)
                self.progressBar=QLabel()
                self.start=QLabel()
                self.popupw, self.output,self.skin = QLabel(),QLabel(),QLabel()
                self.popup_widgets = []


                self.first_exec = False
                self.counter = 0
                self.resize(width,height)
                self.setMouseTracking(True)
                self.popup()
                self.popup_mode = True
                stylesheet = """
        Window {
                background-image: url("bg.jpg"); 
                background-repeat: no-repeat; 
                background-position: center;
        }
"""
                self.setStyleSheet(stylesheet)
                self.showMaximized()
                self.show()
        def mouseMoveEvent(self,event):
                if  current_config['"Output path": '] != "" and current_config['"Skin path": '] != "":  
                        self.first_exec = True
                        self.resizeEvent(True)
                        self.popupw.hide()
                        self.output.hide()
                        self.skin.hide()
                        self.setMouseTracking(False)
                        popup_mode = False

        def resizeEvent(self, event):
                print('fuck')
                ypos = 20
                
                scale = min(self.height()/469, self.width()/832)
                button_width,button_height = get_scale(832,469,257,46,self.width(),self.height())

                start_width,start_height = get_scale(832,469,178,77,self.width(),self.height())
                
                progressbar_width,progressbar_height = self.width() - 20,30
                progressbar_x,progressbar_y = 10,self.height()-40
                tmp_counter=0
                x_pos,button_y = 0,20


                if self.first_exec:
                        self.delete_widgets(self.main_buttons)
                        self.load_buttons(button_width,button_y,button_height,True)
                        self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,True)
                        if self.popup_mode:
                                self.delete_widgets(self.popup_widgets)
                                self.popup()
                else:
                        self.delete_widgets(self.main_buttons)
                        self.load_buttons(button_width,button_y,button_height,False)
                        self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,False)
                        if self.popup_mode:
                                self.delete_widgets(self.popup_widgets)
                                self.popup()



        def delete_widget(self,widget,index):
                widget.setParent(None)
                self.main_buttons.pop(index)
        def loadImg(self,img_dir,width,height):
                pixmap = QPixmap("res/" + img_dir)
                pixmap = pixmap.scaled(width,height)
                return pixmap
        def delete_widgets(self,listt):
                for x in range(len(listt),0,-1):
                        listt[x-1].setParent(None)
                        listt.pop(x-1)
        def load_buttons(self,button_width,button_y,button_height,clickable):

                logo = Label(10,button_y,278,278,"osr2mp4_logo.png","osr2mp4_logo.png","",False,False,self)

                for x in range(len(self.image_listHover)):
                        file_typeCounter = 0
                        button = Label(self.width()-button_width,button_y,button_width,button_height,self.image_listIdle[x],self.image_listHover[x],self.file_type[file_typeCounter],clickable,False,self)
                        button_width-=30
                        button_y+=int(self.width()/16)
                        file_typeCounter+=1
                        if not clickable:
                                blur_effect = QGraphicsBlurEffect() 
                                button.setGraphicsEffect(blur_effect)
                        button.show()
                        self.main_buttons.append(button)
                logo.show()
                if not clickable:
                        blur_effect0 = QGraphicsBlurEffect() 
                        logo.setGraphicsEffect(blur_effect0)
        def load_mainWidgets(self,progressbar_x,progressbar_y,progressbar_width,start_width,start_height,clickable):
                blur_effect0 = QGraphicsBlurEffect() 
                self.progressBar.setParent(None)
                self.start.setParent(None)
                
                self.progressBar = progress_bar(progressbar_x,progressbar_y,self.width()-20,32,"progressbar.png","progressbar.png","",self)
                self.progressBar.show()
                
                self.start = Label(progressbar_x + progressbar_width - start_width,self.height()-40-start_height,start_width,start_height,"start.png","start_hover.png","start",True,False,self)
                self.start.show()
                if not clickable:
                        self.start.setGraphicsEffect(blur_effect0)
                        blur_effect0 = QGraphicsBlurEffect() 
                        self.progressBar.setGraphicsEffect(blur_effect0)
        def popup(self):
                popup_width,popup_height = get_scale(1280,668,600,400,self.width(),self.height())
                output_width, output_height = get_scale(1280,668,244,52,self.width(),self.height())
                skin_width, skin_height = get_scale(1280,668,272,68,self.width(),self.height())
                self.popupw = Label(0,0,popup_width,popup_height,"popup_1.png","popup_1.png","",False,True,self)
                self.output = Label(395,440,output_width,output_height,"outputf.png","outputf.png","Output",True,False,self)
                self.skin = Label(612,430,skin_width,skin_height,"skin.png","skin.png","Skin",True,False,self)
                print(self.popupw.x(),self.popupw.y())
                self.popup_widgets.extend((self.popupw,self.output,self.skin))
                self.popupw.show()
                self.output.show()
                self.skin.show()
        def unblur(self,button):
                blur_effect = QGraphicsBlurEffect()
                blur_effect.setBlurRadius(0)
                button.setGraphicsEffect(blur_effect)
        
def get_scale(w,h,widW,widH,window_width,window_height):
        scale = min(window_height/h, window_width/w)
        width = int(widW * scale)
        height = int(widH * scale)
        return width,height

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
