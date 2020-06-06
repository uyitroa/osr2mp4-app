from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow,QApplication, QFileDialog,QWidget,QLabel, QPushButton, QGraphicsBlurEffect,QVBoxLayout
import sys
from pathlib import Path
from progressbar_class import progress_bar
import json
current_config = {
"osu! path": r"",
"Skin path": r"C:\Users\Shiho\Downloads\Totori-2018-04-01",
"Beatmap path": "",
".osr path": "",
"Default skin path": r"C:\Users\Shiho\Downloads\Totori-2018-04-01",
"Output path": "",
"Width": 600,
"Height": 400,
"FPS": 60,
"Start time": 210,
"End time": -1,
"Video codec": "XVID",
"Process": 0,
"ffmpeg path": "ffmpeg"
}
class Label(QPushButton):
	def __init__(self,x_pos,y_pos,width,height,img,img_hover,file_type,clickable,center,parent):

			super(Label, self).__init__(parent)
	
			self.window = parent


			self.clickable = clickable
			self.width,self.height,self.file_type = width,height,file_type
			#Setting image for default start
			self.img_idle = "res/" + img
			self.img_hover = "res/" + img_hover
			#setting image for hover start
			self.setIcon(QtGui.QIcon(self.img_idle))
			self.setIconSize(QtCore.QSize(width,height))
			self.setGeometry(x_pos,y_pos,width,height)
			
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
				with open('config.json', 'w+') as f:
					f.write(json.dumps(current_config))
				print(current_config)

				import run_osu.py

	def enterEvent(self, QEvent):
			self.setIcon(QtGui.QIcon(self.img_hover))

	def leaveEvent(self, QEvent):
			self.setIcon(QtGui.QIcon(self.img_idle))

	def openFileNameDialog(self):
		tmp_bool = False
		if self.clickable:
				if self.file_type == "osu!":
						self.window.selected_osu = True

						
				if self.file_type == "Output" or  self.file_type == "Beatmap" or self.file_type == "osu!":

						home_dir = str(Path.home())
						fname = QFileDialog.getExistingDirectory(None, ("Select Directory"), home_dir)
						if self.file_type == "Output":
							self.window.selected_output = True
							fname += "/output.avi"
				else:
						tmp_bool = True
						home_dir = str(Path.home())
						fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type,self.file_type))
						self.window.selected_osr = True
				current_config["{} path".format(self.file_type)] =  fname[0] if tmp_bool == True else fname
				print(self.file_type)
				if self.window.selected_output and self.window.selected_osu:
						self.window.gay()
				if self.window.selected_osr:
					self.window.update_osrPath(fname[0])


class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: grey;")
		width,height = 1000,600
		x_pos,button_y = 0,20
		self.image_listIdle = ["osr idle.png","mapset idle.png"]
		self.image_listHover = ["osr hover.png","mapset hover.png"]
		self.file_type = [".osr","Beatmap","Beatmap","Output"]
		self.main_buttons,self.extra_widgets = [],[]
		for x in range(0,len(self.image_listHover) - 1,2):
				button = QLabel()
				self.main_buttons.append(button)
		self.progressBar=QLabel()
		self.start=QLabel()
		self.popupw, self.output,self.osu,self.osr_,self.osr_path = QLabel(),QLabel(),QLabel(),QLabel(),QLabel()
		self.popup_widgets = []
		self.logo = QLabel()
		self.osr_pathGui,mapset_pathGui = QLabel(),QLabel()
		self.first_exec = False
		self.selected_output,self.selected_osr = False,False
		self.selected_osu = False
		self.counter = 0
		self.resize(width,height)
		self.popup_mode = True
		self.osr_pathText = ""
		self.osr_updateIdle,self.mapset_updateIdle = True,True
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
	def gay(self):
		if  current_config["Output path"] != "" and current_config["osu! path"] != "":  
			self.first_exec = True
			self.resizeEvent(True)
			self.popupw.hide()
			self.output.hide()
			self.osu.hide()
			self.popup_mode = False
	def update_osrPath(self,path):
		if  current_config[".osr path"] != "":
			self.osr_updateIdle = False
			self.osr_pathText = path
			self.resizeEvent(True)

	def resizeEvent(self, event):
		ypos = 20
		
		scale = min(self.height()/469, self.width()/832)
		button_width,button_height = get_scale(832,469,357,60,self.width(),self.height())

		start_width,start_height = get_scale(832,469,178,77,self.width(),self.height())
		
		progressbar_width,progressbar_height = self.width() - 20,30
		progressbar_x,progressbar_y = 10,self.height()-40
		tmp_counter=0
		x_pos,button_y = 0,50

		if self.first_exec:
				self.delete_widgets(self.main_buttons)
				self.delete_widgets(self.extra_widgets)
				self.load_buttons(button_width,button_y,button_height,True)
				self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,True)
				if self.popup_mode:
						self.delete_widgets(self.popup_widgets)
						self.popup()
				self.load_logo(True)
				self.path_guiUpdate("",self.osr_updateIdle,self.main_buttons[-1].y())
		else:
				print("Lols")
				self.delete_widgets(self.main_buttons)
				self.delete_widgets(self.extra_widgets)
				self.load_buttons(button_width,button_y,button_height,False)
				self.load_mainWidgets(progressbar_x,progressbar_y,progressbar_width,start_width,start_height,False)
				if self.popup_mode:
						self.delete_widgets(self.popup_widgets)
						self.popup()
				self.load_logo(False)
				self.path_guiUpdate("",self.osr_updateIdle,self.main_buttons[-1].y())

	def loadImg(self,img_dir,width,height):
			pixmap = QPixmap("res/" + img_dir)
			pixmap = pixmap.scaled(width,height)
			return pixmap
	def delete_widgets(self,listt):	
		for x in range(len(listt),0,-1):
				listt[x-1].setParent(None)
				listt.pop(x-1)
	def load_logo(self,clickable):
		logo_w,logo_h = get_scale(1280,668,700,500,self.width(),self.height())
		self.logo = Label(-50,50,logo_w,logo_h,"osr2mp4_logo.png","osr2mp4_logo.png","",False,False,self)
		if not clickable:
			blur_effect0 = QGraphicsBlurEffect() 
			self.logo.setGraphicsEffect(blur_effect0)
		self.logo.show()
		self.logo.lower()
		self.extra_widgets.append(self.logo)
	def load_buttons(self,button_width,button_y,button_height,clickable):
		file_typeCounter = 0
		for x in range(len(self.image_listHover)):
				button = Label(self.width()-button_width,button_y,button_width,button_height,self.image_listIdle[x],self.image_listHover[x],self.file_type[file_typeCounter],clickable,False,self)
				#button_width-=30
				button_y+=int(self.width()/16)
				file_typeCounter+=1
				if not clickable:
						blur_effect = QGraphicsBlurEffect() 
						button.setGraphicsEffect(blur_effect)
				button.show()
				self.main_buttons.append(button)

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
		popup_width,popup_height = get_scale(1280,668,800,600,self.width(),self.height())
		output_width, output_height = get_scale(1280,668,244,52,self.width(),self.height())
		osu_width, osu_height = get_scale(1280,668,272,68,self.width(),self.height())
		popup_x,popup_y = self.get_center(popup_width,popup_height)
		output_x,output_y = get_coordinates(1280,668,self.width(),self.height(),395,440)
		osu_x,osu_y = get_coordinates(1280,668,self.width(),self.height(),612,430)

		self.popupw = Label(popup_x,popup_y,popup_width,popup_height,"popup_1.png","popup_1.png","",False,False,self)
		self.output = Label(output_x,output_y,output_width,output_height,"outputf.png","outputf.png","Output",True,False,self)
		self.osu = Label(osu_x,osu_y,osu_width,osu_height,"osufolder idle.png","osufolder hover.png","osu!",True,False,self)
		self.popup_widgets.extend((self.popupw,self.output,self.osu))
		self.popupw.show()
		self.output.show()
		self.osu.show()
	def get_center(self,width,height):
		center_x = self.width() / 2 - width / 2
		center_y = self.height() / 2 - height / 2
		return center_x,center_y
	def path_guiUpdate(self,path,idle,posY):
		width,height = get_scale(1280,668,400,59,self.width(),self.height())
		font_width,font_height = get_scale(1280,668,814,239, self.width(),self.height())
		tmp_x = self.main_buttons[-1].frameGeometry().width() - width
		x_pos =  self.main_buttons[-1].x() + tmp_x/2
		padding = 100
		if idle:
			self.osr_ = Label(x_pos,posY+padding,width,height,"osr_pathIdle.png","osr_pathIdle.png","",False,False,self)
		else:
			self.osr_ = Label(x_pos,posY+padding,width,height,"osr_pathDetected.png","osr_pathDetected.png","",False,False,self)
			self.osr_path = Label(x_pos,posY+padding+height/6,width,height,"","","",False,False,self)
			self.osr_path.setText(self.osr_pathText)
			self.osr_path.setStyleSheet("""QPushButton {
    font: bold 14px;
    color: white
}""")
		self.osr_.show()
		self.osr_.lower()
		self.extra_widgets.append(self.osr_)
		self.extra_widgets.append(self.osr_path)
		self.osr_path.show()
def get_scale(w,h,widW,widH,window_width,window_height):
	scale = min(window_height/h, window_width/w)
	width = int(widW * scale)
	height = int(widH * scale)
	return width,height
def get_coordinates(w,h,window_width,window_height,base_x,base_y):
	x_pos = base_x * (window_width / w)
	y_pos = base_y * (window_height / h)

	return x_pos,y_pos

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())