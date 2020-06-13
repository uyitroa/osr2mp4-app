from osr2mp4.osr2mp4 import Osr2mp4

converter = Osr2mp4(filedata="config.json", filesettings="settings.json")
converter.startall()
converter.joinall()