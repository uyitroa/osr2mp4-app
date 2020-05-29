from osr2mp4.osr2mp4 import Osr2mp4

converter = Osr2mp4(filedata="path/to/config.json", filesettings="path/to/settings.json")
converter.startall()
converter.joinall()