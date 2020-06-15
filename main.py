from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QComboBox,QLabel, QPushButton, QGraphicsBlurEffect
import os,json,sys,glob,os.path,configparser,io,subprocess
from progressbar_class import progress_bar
from find_beatmap import find_beatmap_
from PyQt5 import QtCore,  QtGui
from PyQt5.QtGui import QPixmap, QIcon
from pathlib import Path
from config_data import current_config, user_data
import threading
		
	
class ComboBox(QComboBox):
	def __init__(self,parent):
		super(ComboBox, self).__init__(parent)
		self. activated.connect(self.activated_)
		self.window = parent
		self.counter = 0
	def activated_(self,index):
		current_config["Skin path"] = current_config["osu! path"] + "/Skins/" + self.window.skin_dropdown.itemText(index)
		print(current_config["Skin path"])

	def get_skins(self,path):
		self.window.skin_dropdown.addItems(self.window.skins_directory)
		self.get_configInfo(path)

	def get_configInfo(self,path):
		if path != "":
			cfg =  glob.glob(path + "/*.cfg")
			props = read_properties_file(cfg[1])
			name = props['skin']
			
			self.window.skin_dropdown.setCurrentIndex(self.window.skin_dropdown.findText(name))

			current_config["Skin path"] = current_config["osu! path"] + "/Skins/" + name
			skin_list = [f for f in glob.glob(current_config["osu! path"] + "/Skins/*", recursive=True)]
			for x in skin_list:
				index = find_lastIndex(x,"/")
				index2 = find_lastIndex(x,"\\")
				if index > index2:
					self.window.skin_dropdown.addItems([x[index+1:len(x)]])
					print(x[index+1:len(x)])
				else:
					self.window.skin_dropdown.addItems([x[index2+1:len(x)]])
					print(x[index2+1:len(x)])
			
			#rint(self.window.skin_dropdown.findText(name))

class Button(QPushButton):
	def __init__(self,x_pos,y_pos,width,height,img,img_hover,img_click,file_type,clickable,parent):
		self.main_window = parent
		super(Button, self).__init__(parent)
		#Button Properties
		self.clickable = clickable
		self.width,self.height,self.file_type = width,height,file_type

		#Setting image for default start
		self.img_idle = "res/" + img
		self.img_hover = "res/" + img_hover
		self.img_click = "res/" + img_click

		self.setIcon(QtGui.QIcon(self.img_idle))
		self.setIconSize(QtCore.QSize(width,height))
		self.setGeometry(x_pos,y_pos,width,height)
		self.setFlat(True)

		self.openable_filetype = [".osr", "Beatmap", "Output", "osu!"]
		self.folder_type = ["Beatmap", "Output", "osu!"]
		self.displayable_path = [".osr", "Beatmap"]
		self.hoverable_widgets = [".osr", "start", "Beatmap"]

		#Setting up blur effects for button
		self.blur_effect = QGraphicsBlurEffect() 	
		self.blur_effect.setBlurRadius(0) 
		self.setGraphicsEffect(self.blur_effect)

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25) 
		else:
			self.blur_effect.setBlurRadius(0) 

	def run_osu(self):
		from osr2mp4.osr2mp4 import Osr2mp4
		converter = Osr2mp4(filedata="config.json", filesettings="settings.json")
		converter.startall()
		converter.joinall()
	def mousePressEvent(self,QEvent):
		if self.file_type in self.hoverable_widgets:
			self.setIcon(QtGui.QIcon(self.img_click))
		if self.file_type == "start":
			with open('config.json', 'w+') as f:
				json.dump(current_config, f, indent=4)
				f.close()
			print(current_config)	
			func = threading.Thread(target=self.run_osu)
			func.start()
			'''p = subprocess.Popen([sys.executable or "python", "/home/shiho/Desktop/osr-gui/run_osu.py"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			p.wait()'''
			#p = subprocess.Popen("/home/shiho/Desktop/osr-gui/run_osu.py",shell=True)
			#subprocess.check_call([sys.executable or "python", "/home/shiho/Desktop/osr-gui/run_osu.py"], shell=True)
			#os.system("/home/shiho/Desktop/osr-gui/run_osu.py")

	def mouseReleaseEvent(self, event):
		if self.file_type in self.openable_filetype:
			print("F")
			self.openFileNameDialog()
		if self.file_type in self.hoverable_widgets:
			self.setIcon(QtGui.QIcon(self.img_hover))


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
				if self.file_type == "Output":
					file_name += "/output.avi"
			else:
				home_dir = str(Path.home())
				file_name = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "{} files (*{})".format(self.file_type,self.file_type))[0]
				#if file_name == '':
					#file_name = r"C:\Program Files\osu!\Replays\osu! - SPYAIR - Sakura Mitsutsuki (TV Size) [Aurora] (2020-06-15) Osu.osr"
			current_config[self.file_type + " path"] = file_name


		if current_config["Output path"] != "" and current_config["osu! path"] != "":
			self.main_window.delete_popup()
			self.main_window.popup_bool = False
			
			user_data["Output path"], user_data["osu! path"] = current_config["Output path"], current_config["osu! path"]
			self.main_window.check_replay_map()
			self.main_window.resizeEvent(True)
			self.main_window	.skin_dropdown.get_configInfo(current_config["osu! path"])
			with open('user_data.json', 'w+') as f:
				json.dump(user_data, f, indent=4)
				f.close()
		if self.file_type in self.displayable_path:
			osr,beatmap = False,False
			if self.file_type == ".osr":
				osr = True 
				slash,backslash = find_lastIndex(file_name,"/"),find_lastIndex(file_name,"\\")
				if slash != 0: 
					replay_name = file_name[slash+1:len(file_name)]  
				else:
					replay_name = file_name[backslash+1:len(file_name)]
				try:
					self.main_window.find_latestMap(replay_name)
				except:
					pass
				self.main_window.set_path_gui(True,False,replay_name)
				self.main_window.resizeEvent(True)



class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QtGui.QIcon("icon.png"))
		self.setWindowTitle("Subscribe to Raishin Aot")
		self.setStyleSheet("background-color: grey;")
		window_width,window_height = 832,469
		self.resize(window_width,window_height)
		#Booleans and list for deleting widget and default scales
		self.button_1_coordinates = [832, 468, 458, 178]
		self.previous_resolution = [0, 0]
		self.minimum_resolution = [640, 360]
		self.skins_list = []
		self.popup_bool = True
		self.popup_widgets = []
		self.paths_defaultScale = [832,469,270,12]
		self.osr_pathCoordinates = [635,270]
		self.map_defaultScale = [832,469,280,80]
		self.map_defaultCoordinates = [832,469,525,230]
		self.map_pathCoordinates = [635,220]
		self.logo_defaultScale = [1280,668,700,500]
		self.button_default_scale = [832,469,400,70]
		self.button_shadow_scale = [832,469,430,103]
		self.osr_defaultScale = [832,469,280,80]
		self.osr_defaultcoordinates = [832,469,525,180]
		self.start_defaultScale = [832,469,220,100]
		#Main Buttons Properties/Variables(Osr button, Mapset button)
		image_listIdle = ["B1_Idle.png","B2_Idle.png"]
		image_listHover = ["B1_Hover.png","B2_Hover.png"]
		image_listClick = ["B1_Click.png", "B2_Click.png"]
		file_type = [".osr","Beatmap"]
		self.current_path = ["res/osr_pathIdle.png","res/mapset_pathIdle.png"]
		self.main_buttons = []
		self.osr_path,self.map_path = QLabel(self),QLabel(self)

		self.logo = Button(0,0,0,0,"osr2mp4_logo.png","osr2mp4_logo.png","", "",False,self)

		#Applying properties to buttons
		for x in range(len(file_type)):
			btn = Button(0,0,0,0,image_listIdle[x],image_listHover[x],image_listClick[x], file_type[x],False,self)
			self.main_buttons.append(btn)

		self.osr_idle = Button(0,0,0,0,"osr_pathIdle.png","osr_pathIdle.png","osr click.png", "",False,self)

		self.map_idle = Button(0,0,0,0,"mapset_pathIdle.png","mapset_pathIdle.png","mapset click.png", "",False,self)
		
		self.popup_window = Button(0,0,0,0,"popup_1.png","popup_1.png","", "",False,self)
		self.popup_shadow = Button(0,0,0,0,"popup_shadow.png","popup_shadow.png","", "",False,self)

		self.output_window = Button(0,0,0,0,"output_idle.png","output_hover.png","output_click.png", "Output",True,self)
		self.output_shadow = Button(0,0,0,0,"output_shadow.png","output_shadow.png","output_shadow.png", "",True,self)

		self.osu_window = Button(0,0,0,0,"osufolder idle.png","osufolder hover.png","osufolder click.png", "osu!",True,self)
		self.osu_shadow = Button(0,0,0,0,"osufolder shadow.png","osufolder shadow.png","osufolder shadow.png", "",True,self)
		
		self.b1_shadow = Button(0,0,0,0,"B1_Shadow.png","B1_Shadow.png","B1_Shadow.png", "",True,self)
		self.b2_shadow = Button(0,0,0,0,"B2_Shadow.png","B2_Shadow.png","B2_Shadow.png", "",True,self)


		progressbar_width, progressbar_height, progressbar_x, progressbar_y = self.load_progressbar()
		self.progress_bar = progress_bar(progressbar_x,progressbar_y,self.width()-20,progressbar_height,"progressbar.png","progressbar.png","",self)

		self.start_btn = Button(0,0,0,0,"start.png","start_hover.png","start_click.png", "start",True,self)
		self.start_btn.lower()

		self.popup_widgets.extend((self.popup_window,self.output_window,self.osu_window,self.popup_shadow,self.osu_shadow, self.output_shadow))

		self.blurrable_widgets = [self.logo,self.start_btn,self.osr_idle,self.map_idle]
		for x in self.main_buttons:
			self.blurrable_widgets.append(x)

		self.skin_dropdown = ComboBox(self) 
		self.skin_dropdown.addItems(["Default Skin"])


		self.check_osuPath()
		self.check_replay_map()
		self.skin_dropdown.get_configInfo(current_config["osu! path"])
		self.show()


	def resizeEvent(self, event):
		height = self.width() * 9/16 
		self.resize(self.width(),height)
		if self.width() < self.minimum_resolution[0] and self.height() < self.minimum_resolution[1]:
			self.resize(self.previous_resolution[0],self.previous_resolution[1])
		#Buttons scaling

		logo_w,logo_h = get_scale(self.logo_defaultScale[0],self.logo_defaultScale[1],self.logo_defaultScale[2],self.logo_defaultScale[3],self.width(),self.height())
		main_buttonW,main_buttonH = get_scale(self.button_default_scale[0],self.button_default_scale[1],self.button_default_scale[2],self.button_default_scale[3],self.width(),self.height())

		main_shadowW,main_shadowH = get_scale(self.button_shadow_scale[0],self.button_shadow_scale[1],self.button_shadow_scale[2],self.button_shadow_scale[3],self.width(),self.height())
		
		button1_x,button1_y = get_scale(self.button_1_coordinates[0],self.button_1_coordinates[1],self.button_1_coordinates[2],self.button_1_coordinates[3],self.width(),self.height())

		osr_width,osr_height = get_scale(self.osr_defaultScale[0],self.osr_defaultScale[1],self.osr_defaultScale[2],self.osr_defaultScale[3],self.width(),self.height())
		osr_x,osr_y = get_coordinates(self.osr_defaultcoordinates[0],self.osr_defaultcoordinates[1],self.width(),self.height(),self.osr_defaultcoordinates[2],self.osr_defaultcoordinates[3])
		osr_x = self.width()-osr_width-30
		map_width,map_height = get_scale(self.map_defaultScale[0],self.map_defaultScale[1],self.map_defaultScale[2],self.map_defaultScale[3],self.width(),self.height())
		map_x,map_y = get_coordinates(self.map_defaultCoordinates[0],self.map_defaultCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])


		osr_pathX,osr_pathY = get_coordinates(832,469,self.width(),self.height(),self.osr_pathCoordinates[0],self.osr_pathCoordinates[1])
		osr_pathWidth,osr_pathHeight = get_scale(self.paths_defaultScale[0],self.paths_defaultScale[1],self.paths_defaultScale[2],self.paths_defaultScale[3],self.width(),self.height())

		map_pathX,map_pathY = get_coordinates(832,469,self.width(),self.height(),self.map_pathCoordinates[0],self.map_pathCoordinates[1])
		map_pathWidth,map_pathHeight = get_scale(self.paths_defaultScale[0],self.paths_defaultScale[1],self.paths_defaultScale[2],self.paths_defaultScale[3],self.width(),self.height())

		progressbar_width,progressbar_height = self.width() - 20,30
		progressbar_x,progressbar_y = 10,self.height()-40


		start_width, start_height = get_scale(self.start_defaultScale[0],self.start_defaultScale[1],self.start_defaultScale[2],self.start_defaultScale[3],self.width(),self.height())
		start_x = progressbar_x + progressbar_width - start_width
		start_y = progressbar_y - progressbar_height - start_height + 20

		
		if self.popup_bool:

			popup_defaultScale = [1000,600,620,430]

			popup_shadowScale = [1000,600,630,440]
			popup_shadowCoordinates = [225,95]

			popup_defaultCoordinates = [230,100]
			popup_width,popup_height = get_scale(popup_defaultScale[0],popup_defaultScale[1],popup_defaultScale[2],popup_defaultScale[3],self.width(),self.height())
			popup_x,popup_y = get_coordinates(popup_defaultScale[0],popup_defaultScale[1],self.width(),self.height(),popup_defaultCoordinates[0],popup_defaultCoordinates[1])

			popup_shadowW,popup_shadowH = get_scale(popup_shadowScale[0],popup_shadowScale[1],popup_shadowScale[2],popup_shadowScale[3],self.width(),self.height())
			popup_shadowX,popup_shadowY = get_coordinates(popup_shadowScale[0],popup_shadowScale[1],self.width(),self.height(),popup_shadowCoordinates[0],popup_shadowCoordinates[1])
			
			popup_btnScale = [1000,600,260,70]
			
			popup_btnCoordinates = [295,410]
			osr_btnCoordinates = [530,410]

			output_width, output_height = get_scale(popup_btnScale[0],popup_btnScale[1],popup_btnScale[2],popup_btnScale[3],self.width(), self.height())
			output_x,output_y = get_coordinates(popup_btnScale[0],popup_btnScale[1],self.width(),self.height(),popup_btnCoordinates[0], popup_btnCoordinates[1])
			
			
			shadow_Scale = [1000,600,280,80]
			osr_shadowCoordinates = [520,405]

			output_shadowScale = [1000,600,280,70]
			output_shadowCoordinates = [285,410]

			osu_width, osu_height = get_scale(popup_btnScale[0],popup_btnScale[1],popup_btnScale[2],popup_btnScale[3],self.width(), self.height())
			osu_shadowWidth, osu_shadowHeight = get_scale(shadow_Scale[0],shadow_Scale[1],shadow_Scale[2],shadow_Scale[3],self.width(), self.height())

			osu_x,osu_y = get_coordinates(popup_btnScale[0],popup_btnScale[1],self.width(),self.height(),osr_btnCoordinates[0], osr_btnCoordinates[1])
			osu_shadowX,osu_shadowY = get_coordinates(shadow_Scale[0],shadow_Scale[1],self.width(),self.height(),osr_shadowCoordinates[0], osr_shadowCoordinates[1])
			
			output_shadowWidth, output_shadowHeight = get_scale(output_shadowScale[0],output_shadowScale[1],output_shadowScale[2],output_shadowScale[3],self.width(), self.height())
			output_shadowX,output_shadowY = get_coordinates(output_shadowScale[0],output_shadowScale[1],self.width(),self.height(),output_shadowCoordinates[0], output_shadowCoordinates[1])

			self.blur_function(True)

		else:
			self.blur_function(False)


		#Changing buttons properties(Osr button,Mapset Button)
		main_buttonY = 50
		main_shadowY = 35
		counter = 0
		for x in self.main_buttons:
			if counter == 0:
				x.setGeometry(self.width()-main_buttonW ,main_buttonY,main_buttonW,main_buttonH)
				x.setIconSize(QtCore.QSize(main_buttonW,main_buttonH))

				self.b1_shadow.setGeometry(self.width()-main_buttonW-15 ,main_shadowY,main_shadowW,main_shadowH)
				self.b1_shadow.setIconSize(QtCore.QSize(main_shadowW,main_shadowH))
				x.raise_()
			else:
				x.setGeometry(button1_x,main_buttonY,main_buttonW-25,main_buttonH)
				x.setIconSize(QtCore.QSize(main_buttonW-25,main_buttonH))

				self.b2_shadow.setGeometry(button1_x-15,main_shadowY,main_shadowW-25,main_shadowH)
				self.b2_shadow.setIconSize(QtCore.QSize(main_shadowW-25,main_shadowH))
				x.raise_()
			if not self.popup_bool:
				x.clickable=True

			main_buttonY +=self.width()//13
			main_shadowY +=self.width()//13
			counter += 1

		self.logo.setGeometry(-50,50,logo_w,logo_h)
		self.logo.setIconSize(QtCore.QSize(logo_w,logo_h))

		self.osr_idle.setGeometry(osr_x,osr_y,osr_width,osr_height)
		self.osr_idle.setIconSize(QtCore.QSize(osr_width,osr_height))

		self.map_idle.setGeometry(osr_x,map_y,map_width,map_height)
		self.map_idle.setIconSize(QtCore.QSize(map_width,map_height))

		self.osr_path.setGeometry(osr_x,osr_pathY,osr_pathWidth,osr_pathHeight)
		self.map_path.setGeometry(osr_x,map_pathY,map_pathWidth,map_pathHeight)
		if self.popup_bool:
			self.popup_window.setGeometry(popup_x,popup_y,popup_width,popup_height)
			self.popup_window.setIconSize(QtCore.QSize(popup_width,popup_height))

			self.popup_shadow.setGeometry(popup_shadowX,popup_shadowY,popup_shadowW,popup_shadowH)
			self.popup_shadow.setIconSize(QtCore.QSize(popup_shadowW,popup_shadowH	))

			self.output_window.setGeometry(output_x,output_y,output_width,output_height)
			self.output_window.setIconSize(QtCore.QSize(output_width,output_height))

			self.osu_window.setGeometry(osu_x,osu_y,osu_width,osu_height)
			self.osu_window.setIconSize(QtCore.QSize(osu_width,osu_height))

			self.osu_shadow.setGeometry(osu_shadowX,osu_shadowY,osu_shadowWidth,osu_shadowHeight)
			self.osu_shadow.setIconSize(QtCore.QSize(osu_shadowWidth,osu_shadowHeight))

			self.output_shadow.setGeometry(output_shadowX,output_shadowY,output_shadowWidth,output_shadowHeight)
			self.output_shadow.setIconSize(QtCore.QSize(output_shadowWidth,output_shadowHeight))


			self.osu_window.raise_()
			self.output_window.raise_()
		self.progress_bar.setGeometry(progressbar_x,progressbar_y,progressbar_width,progressbar_height)
		self.progress_bar.scale_me(progressbar_width,progressbar_height)

		self.start_btn.setGeometry(start_x,start_y,start_width,start_height)
		self.start_btn.setIconSize(QtCore.QSize(start_width, start_height))
		self.previous_resolution[0] = self.width()
		self.previous_resolution[1] = self.height()
	def set_path_gui(self,osr,mapset,text):
		if osr:
			osr_x,osr_y = get_coordinates(1000,600,self.width(),self.height(),635,240)
			self.width()-self.osr_idle.frameGeometry().width()-30

			osr_width,osr_height = get_scale(1000,600,336,12,self.width(),self.height())
			
			self.osr_path.setText(text)
			self.osr_path.setStyleSheet("font-size: 8pt; font-weight: bold; color: white")
			self.osr_path.setGeometry(osr_x,osr_y,osr_width,osr_height)
			self.osr_idle.img_hover = "res/osr_pathDetected.png"
			self.osr_idle.img_idle = "res/osr_pathDetected.png"
			#To reload the button image
			self.osr_idle.enterEvent(True)
			self.osr_path.show()
		elif mapset:
			map_width,map_height = get_scale(self.map_defaultScale[0],self.map_defaultScale[1],self.map_defaultScale[2],self.map_defaultScale[3],self.width(),self.height())
			map_x,map_y = get_coordinates(self.map_defaultCoordinates[0],self.map_defaultCoordinates[1],self.width(),self.height(),self.map_defaultCoordinates[2],self.map_defaultCoordinates[3])
			map_x = self.width()-map_width-30
			self.map_path.setText(text)
			self.map_path.setStyleSheet("font-size: 8pt; font-weight: bold; color: white")
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
			current_config["Output path"] = data["Output path"] + "/output.avi"
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
				self.set_path_gui(True,False,replay_name)

			current_config[".osr path"] = replay
		

	def find_latestMap(self,replay):
		print(replay)
		if current_config["osu! path"] != "":
			beatmap_path = find_beatmap_(current_config["osu! path"] + "/Replays/" + replay,current_config["osu! path"])
			current_config["Beatmap path"] = current_config["osu! path"] + "/Songs/" + beatmap_path
			if beatmap_path != "":
				self.set_path_gui(False,True,beatmap_path)

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

def read_properties_file(file_path):
	with open(file_path) as f:
		config = io.StringIO()
		config.write('[dummy_section]\n')
		config.write(f.read().replace('%', '%%'))
		config.seek(0, os.SEEK_SET)

		cp = configparser.SafeConfigParser()
		cp.readfp(config)

		return dict(cp.items('dummy_section'))
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
