from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QComboBox,QLabel, QPushButton, QGraphicsBlurEffect
import os,json,sys,glob,os.path,configparser,io,subprocess
from progressbar_class import progress_bar
from find_beatmap import find_beatmap_
from PyQt5 import QtCore,  QtGui
from PyQt5.QtGui import QPixmap, QIcon
from pathlib import Path
from config_data import current_config, user_data




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

		self.setIcon(QtGui.QIcon(self.img_idle))
		self.setIconSize(QtCore.QSize(width,height))
		self.setGeometry(x_pos,y_pos,width,height)
		self.setFlat(True)

		self.openable_filetype = [".osr", "Beatmap", "Output", "osu!"]
		self.folder_type = ["Beatmap", "Output", "osu!"]
		self.displayable_path = [".osr", "Beatmap"]

		#Setting up blur effects for button
		self.blur_effect = QGraphicsBlurEffect() 	
		self.blur_effect.setBlurRadius(0) 
		self.setGraphicsEffect(self.blur_effect)



	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25) 
		else:
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

		if current_config["Output path"] != "" and current_config["osu! path"] != "":
			self.main_window.delete_popup()
			self.main_window.popup_bool = False
			self.main_window.resizeEvent(True)
			user_data["Output path"], user_data["osu! path"] = current_config["Output path"], current_config["osu! path"]
			self.main_window.check_replay_map()
			with open('user_data.json', 'w+') as f:
				json.dump(user_data, f, indent=4)
				f.close()
		if self.file_type in self.displayable_path:
			osr,beatmap = False,False
			if self.file_type == ".osr":
				osr = True 
			else:
				beatmap = True
			self.main_window.set_path_gui(osr,beatmap,file_name)

		if self.file_type == "start":
			with open('config.json', 'w+') as f:
				json.dump(current_config, f, indent=4)
				f.close()
		print(current_config)

class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: grey;")
		window_width,window_height = 1000,600
		self.resize(window_width,window_height)
		#Booleans and list for deleting widget and default scales
		self.popup_bool = True
		self.popup_widgets = []
		self.paths_defaultScale = [1000,600,320,12]
		self.osr_pathCoordinates = [635,230]
		self.map_defaultScale = [832,469,280,80]
		self.map_defaultCoordinates = [832,469,525,200]
		self.map_pathCoordinates = [635,290]
		self.logo_defaultScale = [1280,668,700,500]
		self.logo_defaultCoordinates = [832,469,357,65]
		self.osr_defaultScale = [832,469,280,80]
		self.osr_defaultcoordinates = [832,469,525,150]
		self.start_defaultScale = [832,469,220,150]
		self.start_defaultCoordinates = [1000,600,726,400]

		#Main Buttons Properties/Variables(Osr button, Mapset button)
		image_listIdle = ["osr idle.png","mapset idle.png"]
		image_listHover = ["osr hover.png","mapset hover.png"]
		file_type = [".osr","Beatmap"]
		self.current_path = ["res/osr_pathIdle.png","res/mapset_pathIdle.png"]
		self.main_buttons = []
		self.osr_path,self.map_path = QLabel(self),QLabel(self)

		self.logo = Button(0,0,0,0,"osr2mp4_logo.png","osr2mp4_logo.png","",False,self)

		#Applying properties to buttons
		for x in range(len(file_type)):
			btn = Button(0,0,0,0,image_listIdle[x],image_listHover[x],file_type[x],False,self)
			self.main_buttons.append(btn)

		self.osr_idle = Button(0,0,0,0,"osr_pathIdle.png","osr_pathIdle.png","",False,self)

		self.map_idle = Button(0,0,0,0,"mapset_pathIdle.png","mapset_pathIdle.png","",False,self)
		
		self.popup_window = Button(0,0,0,0,"popup_1.png","popup_1.png","",False,self)

		self.output_window = Button(0,0,0,0,"output_idle.png","output_hover.png","Output",True,self)

		self.osu_window = Button(0,0,0,0,"osufolder idle.png","osufolder hover.png","osu!",True,self)

		progressbar_width, progressbar_height, progressbar_x, progressbar_y = self.load_progressbar()
		self.progress_bar = progress_bar(progressbar_x,progressbar_y,self.width()-20,progressbar_height,"progressbar.png","progressbar.png","",self)

		self.start_btn = Button(0,0,0,0,"start.png","start_hover.png","start",True,self)
		self.start_btn.lower()

		self.popup_widgets.extend((self.popup_window,self.output_window,self.osu_window))

		self.blurrable_widgets = [self.logo,self.start_btn,self.osr_idle,self.map_idle]
		for x in self.main_buttons:
			self.blurrable_widgets.append(x)

		self.check_osuPath()
		self.check_replay_map()
		self.show()


	def resizeEvent(self, event):
		#Buttons scaling

		logo_w,logo_h = get_scale(self.logo_defaultScale[0],self.logo_defaultScale[1],self.logo_defaultScale[2],self.logo_defaultScale[3],self.width(),self.height())
		main_buttonW,main_buttonH = get_scale(self.logo_defaultCoordinates[0],self.logo_defaultCoordinates[1],self.logo_defaultCoordinates[2],self.logo_defaultCoordinates[3],self.width(),self.height())

		osr_width,osr_height = get_scale(self.osr_defaultScale[0],self.osr_defaultScale[1],self.osr_defaultScale[2],self.osr_defaultScale[3],self.width(),self.height())
		osr_x,osr_y = get_coordinates(self.osr_defaultcoordinates[0],self.osr_defaultcoordinates[1],self.width(),self.height(),self.osr_defaultcoordinates[2],self.osr_defaultcoordinates[3])

		map_width,map_height = get_scale(self.map_defaultScale[0],self.map_defaultScale[1],self.map_defaultScale[2],self.map_defaultScale[3],self.width(),self.height())
		map_x,map_y = get_coordinates(self.map_defaultCoordinates[0],self.map_defaultCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])


		osr_pathX,osr_pathY = get_coordinates(1000,600,self.width(),self.height(),self.osr_pathCoordinates[0],self.osr_pathCoordinates[1])
		osr_pathWidth,osr_pathHeight = get_scale(self.paths_defaultScale[0],self.paths_defaultScale[1],self.paths_defaultScale[2],self.paths_defaultScale[3],self.width(),self.height())

		map_pathX,map_pathY = get_coordinates(self.paths_defaultScale[0],self.paths_defaultScale[1],self.width(),self.height(),self.map_pathCoordinates[0],self.map_pathCoordinates[1])
		map_pathWidth,map_pathHeight = get_scale(self.paths_defaultScale[0],self.paths_defaultScale[1],self.paths_defaultScale[2],self.paths_defaultScale[3],self.width(),self.height())

		progressbar_width,progressbar_height = self.width() - 20,32
		progressbar_x,progressbar_y = 10,self.height()-40


		start_width, start_height = get_scale(self.start_defaultScale[0],self.start_defaultScale[1],self.start_defaultScale[2],self.start_defaultScale[3],self.width(),self.height())
		start_x, start_y = get_coordinates(self.start_defaultCoordinates[0],self.start_defaultCoordinates[1],self.width(),self.height(),self.start_defaultCoordinates[2],self.start_defaultCoordinates[3])
		
		popup_x,popup_y, output_x, output_y, osu_x, osu_y = 0, 0,0,0,0,0
		popup_width, popup_height, output_width, output_height, osu_width, osu_height = 0,0,0,0,0,0	
		if self.popup_bool:

			popup_defaultScale = [1000,600,750,550]
			popup_defaultCoordinates = [125,60]
			popup_width,popup_height = get_scale(popup_defaultScale[0],popup_defaultScale[1],popup_defaultScale[2],popup_defaultScale[3],self.width(),self.height())
			popup_x,popup_y = get_coordinates(popup_defaultScale[0],popup_defaultScale[1],self.width(),self.height(),popup_defaultCoordinates[0],popup_defaultCoordinates[1])
			
			popup_btnScale = [1000,600,260,70]
			popup_btnCoordinates = [250,410]
			output_width, output_height = get_scale(popup_btnScale[0],popup_btnScale[1],popup_btnScale[2],popup_btnScale[3],self.width(), self.height())
			output_x,output_y = get_coordinates(popup_btnScale[0],popup_btnScale[1],self.width(),self.height(),popup_btnCoordinates[0], popup_btnCoordinates[1])
			
			osr_btnCoordinates = [485,410]
			osu_width, osu_height = get_scale(popup_btnScale[0],popup_btnScale[1],popup_btnScale[2],popup_btnScale[3],self.width(), self.height())
			osu_x,osu_y = get_coordinates(popup_btnScale[0],popup_btnScale[1],self.width(),self.height(),osr_btnCoordinates[0], osr_btnCoordinates[1])
		
			self.blur_function(True)

		else:
			self.blur_function(False)


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

		self.progress_bar.setGeometry(progressbar_x,progressbar_y,progressbar_width,progressbar_height)
		self.progress_bar.scale_me(progressbar_width,progressbar_height)

		self.start_btn.setGeometry(start_x,start_y,start_width,start_height)
		self.start_btn.setIconSize(QtCore.QSize(start_width, start_height))
	def set_path_gui(self,osr,mapset,text):
		if osr:
			osr_x,osr_y = get_coordinates(1000,600,self.width(),self.height(),635,240)
			osr_width,osr_height = get_scale(1000,600,336,12,self.width(),self.height())
			
			self.osr_path.setText(text)
			self.map_path.setStyleSheet("font-size: 9pt; font-weight: bold; color: white")
			self.osr_path.setGeometry(osr_x,osr_y,osr_width,osr_height)
			self.osr_idle.img_hover = "res/osr_pathDetected.png"
			self.osr_idle.img_idle = "res/osr_pathDetected.png"
			#To reload the button image
			self.osr_idle.enterEvent(True)
			self.osr_path.show()
		elif mapset:
			map_width,map_height = get_scale(self.map_defaultScale[0],self.map_defaultScale[1],self.map_defaultScale[2],self.map_defaultScale[3],self.width(),self.height())
			map_x,map_y = get_coordinates(self.map_defaultCoordinates[0],self.map_defaultCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])
			self.map_path.setText(text)
			self.map_path.setStyleSheet("font-size: 9pt; font-weight: bold; color: white")
			self.map_path.setGeometry(map_x,map_y,map_width,map_height)
			self.map_idle.img_hover = "res/mapset_pathDetected.png"
			self.map_idle.img_idle = "res/mapset_pathDetected.png"
			#To reload the button image
			self.map_idle.enterEvent(True)
			self.map_path.show()

	def blur_function(self,blur):
		if blur:
			for x in self.blurrable_widgets:
				x.blur_me(True)
		else:
			for x in self.blurrable_widgets:
				x.blur_me(False)

	def delete_popup(self):
		for x in self.popup_widgets:
			x.setParent(None)


	def load_progressbar(self):
		progressbar_width,progressbar_height = self.width() - 20,32
		progressbar_x,progressbar_y = 10,self.height()-40
		return progressbar_width,progressbar_height,progressbar_x,progressbar_y

	def check_osuPath(self):
		if os.path.isfile("user_data.json"): 
			with open('user_data.json') as f:
				data = json.load(f)
			current_config["Output path"] = data["Output path"]
			current_config["osu! path"] = data["osu! path"]
			if data["Output path"] != "" and data["osu! path"] != "":
				self.delete_popup()
				self.popup_bool = False
			print("Data loaded:\n{}\n{}".format(data["Output path"], data["osu! path"]))

	def find_latestReplay(self):
		if current_config["osu! path"] != "":
			path = current_config["osu! path"] + "/Replays/*.osr"
			list_of_files = glob.glob(path)
			replay = max(list_of_files, key=os.path.getctime)
			slash,backslash = find_lastIndex(replay,"/"),find_lastIndex(replay,"\\")
			replay_name = replay[max(slash,backslash)+1:len(replay)]
			self.find_latestMap(replay_name)
			if replay_name != "":
				map_x,map_y = get_coordinates(self.map_pathCoordinates[0],self.map_pathCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])
				self.osr_path.setText(replay_name)
				self.osr_path.setStyleSheet("font-size: 9pt; font-weight: bold; color: white")
				self.osr_path.setGeometry(map_x,map_y,0,0)

				self.osr_idle.img_hover = "res/osr_pathDetected.png"
				self.osr_idle.img_idle = "res/osr_pathDetected.png"
				self.osr_idle.enterEvent(True)
				self.resizeEvent(True)

			current_config[".osr path"] = replay
			print(replay_name)
		

	def find_latestMap(self,replay):
		if current_config["osu! path"] != "":
			beatmap_path = find_beatmap_(current_config["osu! path"] + "/Replays/" + replay,current_config["osu! path"])
			current_config["Beatmap path"] = current_config["osu! path"] + "/Songs/" + beatmap_path
			if beatmap_path != "":
				map_x,map_y = get_coordinates(self.map_pathCoordinates[0],self.map_pathCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])
				self.map_path.setText(beatmap_path)
				self.map_path.setStyleSheet("font-size: 9pt; font-weight: bold; color: white")
				self.map_path.setGeometry(map_x,map_y,0,0)

				self.map_idle.img_hover = "res/mapset_pathDetected.png"
				self.map_idle.img_idle = "res/mapset_pathDetected.png"
				self.map_idle.enterEvent(True)
				self.resizeEvent(True)

			current_config["Beatmap path"] = beatmap_path
			print(beatmap_path)


	def check_replay_map(self):
		self.find_latestReplay()
def get_scale(w,h,widW,widH,window_width,window_height):
	scale = min(window_height/h, window_width/w)

	width = int(widW * scale)
	height = int(widH * scale)
	return width,height
def get_coordinates(w,h,window_width,window_height,base_x,base_y):
    scale = min(window_height/h, window_width/w)
    x_pos = int(base_x * scale)
    y_pos = int(base_y * scale)
    return x_pos,y_pos


def find_lastIndex(text,item):
	index = 0
	for x in range(len(text)):
		if text[x] == item: index = x
	return index

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
