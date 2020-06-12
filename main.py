from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QComboBox,QLabel, QPushButton, QGraphicsBlurEffect
import os,json,sys,glob,os.path,configparser,io,subprocess
from progressbar_class import progress_bar
from find_beatmap import find_beatmap_
from PyQt5 import QtCore,  QtGui
from PyQt5.QtGui import QPixmap, QIcon
from pathlib import Path
from config_data import current_config
class Button(QPushButton):
	def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,clickable,parent):
		self.main_window = parent
		super(Button, self).__init__(parent)
		#Button Properties
		self.clickable = clickable
		self.width,self.height,self.file_type = width,height,file_type

		#Setting image for default start
		self.img_idle = "res/" + img
		self.img_hover = "res/" + img_hover

		#Applying properties to buttons
		self.setIcon(QtGui.QIcon(self.img_idle))
		self.setIconSize(QtCore.QSize(width,height))
		self.setGeometry(x_pos,y_pos,width,height)
		self.setFlat(True)

		#I don't know
		self.openable_filetype = [".osr","Beatmap","Output","osu!"]
		self.folder_type = ["Beatmap","Output","osu!"]
		self.displayable_path = [".osr","Beatmap"]

		#Setting up blur effects for button
		'''self.blur_effect = QGraphicsBlurEffect() 	
		self.blur_effect.setBlurRadius(25) 
		self.setGraphicsEffect(self.blur_effect)
		self.blur_condition = True'''



	def blur_me(self,blur):
		if blur:
			self.blur_condition = True
			self.blur_effect.setBlurRadius(25) 
		else:
			self.blur_condition = False
			self.blur_effect.setBlurRadius(0) 

	def mousePressEvent(self,QEvent):
		if self.file_type in self.openable_filetype:
			self.openFileNameDialog()
	def enterEvent(self, QEvent):
		self.setIcon(QtGui.QIcon(self.img_hover))

	def leaveEvent(self, QEvent):
		self.setIcon(QtGui.QIcon(self.img_idle))

	def openFileNameDialog(self):
		file_name = ""
		if self.clickable:
			if self.file_type in self.folder_type:
				home_dir = str(Path.home())
				file_name = QFileDialog.getExistingDirectory(None, ("Select Directory"), home_dir)
			else:
				home_dir = str(Path.home())
				file_name = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type,self.file_type))[0]
			current_config[self.file_type + " path"] = file_name

		if self.file_type in self.displayable_path:
			osr,beatmap = False,False
			if self.file_type == ".osr":
				osr = True 
			else:
				beatmap = True
			self.main_window.set_path_gui(osr,beatmap,file_name)
class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		#Main Window Propeties
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: grey;")
		window_width,window_height = 1000,600
		self.resize(window_width,window_height)

		#Main Buttons Properties/Variables(Osr button, Mapset button)
		image_listIdle = ["osr idle.png","mapset idle.png"]
		image_listHover = ["osr hover.png","mapset hover.png"]
		file_type = [".osr","Beatmap"]
		self.current_path = ["res/osr_pathIdle.png","res/mapset_pathIdle.png"]
		self.main_buttons = []
		self.osr_path,self.map_path = QLabel(),QLabel()

		#Load osu logo
		self.logo = Button(0,0,0,0,"osr2mp4_logo.png","osr2mp4_logo.png","",False,self)

		#Applying properties to buttons
		for x in range(len(file_type)):
			btn = Button(0,0,0,0,image_listIdle[x],image_listHover[x],file_type[x],False,self)
			self.main_buttons.append(btn)

		#Load osr path gui
		self.osr_idle = Button(0,0,0,0,"osr_pathIdle.png","osr_pathIdle.png","",False,self)

		#Load map path gui
		self.map_idle = Button(0,0,0,0,"mapset_pathIdle.png","mapset_pathIdle.png","",False,self)
		
		#Load the popup widget
		self.popup_window = Button(0,0,0,0,"popup_1.png","popup_1.png","",False,self)

		#Load output widget
		self.output_window = Button(0,0,0,0,"output_idle.png","output_hover.png","Output",True,self)

		#Load skin widget
		self.osu_window = Button(0,0,0,0,"osufolder idle.png","osufolder hover.png","Output",True,self)

		self.show()

	def resizeEvent(self, event):
		#Buttons scaling
		logo_w,logo_h = get_scale(1280,668,700,500,self.width(),self.height())
		main_buttonW,main_buttonH = get_scale(832,469,357,65,self.width(),self.height())

		osr_width,osr_height = get_scale(832,469,280,80,self.width(),self.height())
		osr_x,osr_y = get_coordinates(832,469,self.width(),self.height(),525,150)

		map_width,map_height = get_scale(832,469,280,80,self.width(),self.height())
		map_x,map_y = get_coordinates(832,469,self.width(),self.height(),525,200)

		osr_pathX,osr_pathY = get_coordinates(1000,600,self.width(),self.height(),635,240)
		osr_pathWidth,osr_pathHeight = get_scale(1000,600,336,12,self.width(),self.height())

		map_pathX,map_pathY = get_coordinates(1000,600,self.width(),self.height(),635,305)
		map_pathWidth,map_pathHeight = get_scale(1000,600,336,12,self.width(),self.height())

		popup_width,popup_height = get_scale(1000,600,750,550,self.width(),self.height())
		popup_x,popup_y = get_coordinates(1000,600,self.width(),self.height(),125,60)

		output_width, output_height = get_scale(1000,600,260,200,self.width(), self.height())
		output_x,output_y = get_coordinates(1000,600,self.width(),self.height(),250, 350)
		

		osu_width, osu_height = get_scale(1000,600,260,200,self.width(), self.height())
		osu_x,osu_y = get_coordinates(1000,600,self.width(),self.height(),485, 350)
		


		#Changing buttons properties(Osr button,Mapset Button)
		main_buttonY = 50
		for x in self.main_buttons:
			x.setGeometry(self.width()-main_buttonW,main_buttonY,main_buttonW,main_buttonH)
			x.setIconSize(QtCore.QSize(main_buttonW,main_buttonH))
			x.clickable=True
			main_buttonY +=self.width()//14

		self.logo.setGeometry(-50,50,logo_w,logo_h)
		self.logo.setIconSize(QtCore.QSize(logo_w,logo_h))

		self.osr_idle.setGeometry(osr_x,osr_y,osr_width,osr_height)
		self.osr_idle.setIconSize(QtCore.QSize(osr_width,osr_height))

		self.map_idle.setGeometry(map_x,map_y,map_width,map_height)
		self.map_idle.setIconSize(QtCore.QSize(map_width,map_height))

		self.osr_path.setGeometry(osr_pathX,osr_pathY,osr_pathWidth,osr_pathHeight)
		self.map_path.setGeometry(map_pathX,map_pathY,map_pathWidth,map_pathHeight)

		self.popup_window.setGeometry(popup_x,popup_y,popup_width,popup_height)
		self.popup_window.setIconSize(QtCore.QSize(popup_width,popup_height))

		self.output_window.setGeometry(output_x,output_y,output_width,output_height)
		self.output_window.setIconSize(QtCore.QSize(output_width,output_height))

		self.osu_window.setGeometry(osu_x,osu_y,osu_width,osu_height)
		self.osu_window.setIconSize(QtCore.QSize(osu_width,osu_height))

	def set_path_gui(self,osr,mapset,text):
		if osr:
			osr_x,osr_y = get_coordinates(1000,600,self.width(),self.height(),635,240)
			osr_width,osr_height = get_scale(1000,600,336,12,self.width(),self.height())
			
			self.osr_path = QLabel(self)
			self.osr_path.setText(text)
			self.osr_path.setStyleSheet("font-weight: bold; color: white")
			self.osr_path.setGeometry(osr_x,osr_y,osr_width,osr_height)
			self.osr_idle.img_hover = "res/osr_pathDetected.png"
			self.osr_idle.img_idle = "res/osr_pathDetected.png"
			#To reload the button image
			self.osr_idle.enterEvent(True)
			self.osr_path.show()
		elif mapset:
			map_x,map_y = get_coordinates(1000,600,self.width(),self.height(),635,305)
			map_width,map_height = get_scale(1000,600,336,12,self.width(),self.height())
			self.map_path = QLabel(self)
			self.map_path.setText(text)
			self.map_path.setStyleSheet("font-weight: bold; color: white")
			self.map_path.setGeometry(map_x,map_y,map_width,map_height)
			self.map_idle.img_hover = "res/mapset_pathDetected.png"
			self.map_idle.img_idle = "res/mapset_pathDetected.png"
			#To reload the button image
			self.map_idle.enterEvent(True)
			self.map_path.show()
			

def get_scale(w,h,widW,widH,window_width,window_height):
	scale = min(window_height/h, window_width/w)

	width = int(widW * scale)
	height = int(widH * scale)
	return width,height
def get_coordinates(w,h,window_width,window_height,base_x,base_y):
	x_pos = base_x * (window_width / w)
	y_pos = base_y * (window_height / h)
	x_pos = int(x_pos)
	y_pos = int(y_pos)
	return x_pos,y_pos

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())