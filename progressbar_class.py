from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QLabel
import sys

class progress_bar(QLabel):
    def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,parent=None):
        super(progress_bar, self).__init__(parent)
        self.width,self.height,self.file_type = width,height,file_type
        #Setting image for default start
        self.start_button = QPixmap("res/" + img)
        self.start_button = self.start_button.scaled(width,height)
        #setting image for hover start
        self.start_button_hover = QPixmap("res/" + img_hover)
        self.start_button_hover = self.start_button_hover.scaled(width,height)
        self.setPixmap(self.start_button)
        
        self.setGeometry(x_pos,y_pos,width,height)
        
    def enterEvent(self, QEvent):
        self.setPixmap(self.start_button_hover)

    def leaveEvent(self, QEvent):
        self.setPixmap(self.start_button)
 

