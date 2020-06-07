from osr2mp4.osr2mp4 import Osr2mp4

def run_osu_():

	converter = Osr2mp4(filedata="config.json", filesettings="settings.json")
	converter.startall()
	converter.joinall()