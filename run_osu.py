from osr2mp4.osr2mp4 import Osr2mp4
import time


def run():
	for x in range(101):
	  b = open("progress.txt", "w")
	  b.write(str(x))
	  b.close()
	  time.sleep(0.1)
	'''fprogress = open("progress.txt", "w")
				fprogress.seek(0)
				fprogress.write("0")
				fprogress.truncate()
			
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
			
					fprogress.seek(0)
					fprogress.write(str(curprogress))
					fprogress.truncate()
					print(curprogress)
					time.sleep(2)
				converter.joinall()'''


	'''fprogress = open("progress.txt", "w")
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
		time.sleep(0.2)
	converter.joinall()'''

if __name__ == "__main__":
	run()
