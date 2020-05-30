from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow,QApplication, QFileDialog,QWidget,QLabel, QPushButton, QGraphicsBlurEffect,QVBoxLayout
import sys
from pathlib import Path
from progressbar_class import progress_bar
current_config = []
class Label(QPushButton):
	def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,clickable,center,parent=None):
		super(Label, self).__init__(parent)
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
			f.write("{\n")
			for x in current_config:
				f.write("  " + x + "\n")
			f.write("}")
			print(".confg has been generated")
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
			current_config.append('"{} path": "{}"'.format(self.file_type,fname))

class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: grey;")
		width,height = 800,600
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
		self.first_exec = True


		self.resize(width,height)
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
		
	def resizeEvent(self, event):
		ypos = 20
		
		scale = min(self.height()/469, self.width()/832)
		button_width = int(257 * scale)
		button_height = int(46 * scale)
		
		start_width = int(178 * scale)
		start_height = int(77 * scale)
		
		progressbar_width,progressbar_height = self.width() - 20,30
		progressbar_x,progressbar_y = 10,self.height()-40
		
		tmp_counter=0
		clickable = False
		x_pos,button_y = 0,20
		if not self.first_exec:
			print(" test")

			#Delete Buttons
			self.delete_buttons()

			#Load Buttons
			self.load_buttons(button_width,button_y,button_height,clickable)

			#Load Widgets
			self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,clickable)

		elif self.first_exec:
			self.delete_buttons()
			self.load_buttons(button_width,button_y,button_height,clickable)
			self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,clickable)
			self.awake()
			#self.first_exec=False

	def delete_widget(self,widget,index):
		widget.setParent(None)
		self.main_buttons.pop(index)
	def loadImg(self,img_dir,width,height):
		pixmap = QPixmap("res/" + img_dir)
		pixmap = pixmap.scaled(width,height)
		return pixmap
	def delete_buttons(self):
		for x in range(len(self.main_buttons),0,-1):
			self.delete_widget(self.main_buttons[x-1],x-1)
	def load_buttons(self,button_width,button_y,button_height,clickable):

		logo = Label(10,button_y,278,278,"osr2mp4_logo.png","osr2mp4_logo.png","",False,False,self)

		for x in range(len(self.image_listHover)):
			file_typeCounter = 0
			button = Label(self.width()-button_width,button_y,button_width,button_height,self.image_listIdle[x],self.image_listHover[x],self.file_type[file_typeCounter],clickable,False,self)
			button_width-=30
			button_y+=int(self.width()/16)
			file_typeCounter+=1
			self.main_buttons.append(button)
			if not clickable:
				blur_effect = QGraphicsBlurEffect() 
				button.setGraphicsEffect(blur_effect)
			button.show()
		logo.show()
		if not clickable:
			blur_effect0 = QGraphicsBlurEffect() 
			logo.setGraphicsEffect(blur_effect0)
		print("GG")
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
	def awake(self):
		popup = Label(0,0,800,600,"popup_1.png","popup_1.png","",False,True,self)
		output = Label(412,86,290,40,"outputf.png","outputf.png","Output",True,False,self)
		skin = Label(605,405,210,50,"skin.png","skin.png","Skin",True,False,self)
		popup.show()
		output.show()
		skin.show()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
