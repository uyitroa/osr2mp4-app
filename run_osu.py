from osr2mp4.osr2mp4 import Osr2mp4
import time


def run():
	fprogress = open("progress.txt", "w")
	fprogress.write("0")
	fprogress.close()

	converter = Osr2mp4(filedata="config.json", filesettings="settings.json")
	converter.startall()

	curprogress = 0
	while curprogress < 95:
		curprogress = converter.getprogress()

		a = False
		for i in converter.writers:
			if i.is_alive():
				a = True
		if not a:
			curprogress = 100

		fprogress = open("progress.txt", "w")
		fprogress.write(str(curprogress))
		fprogress.close()
		print(curprogress)
		time.sleep(2)
	converter.joinall()

if __name__ == "__main__":
	run()
