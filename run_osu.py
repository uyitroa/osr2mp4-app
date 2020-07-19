import inspect
import os
import sys
import time


class Dummy: pass

#
# def fixpath():
# 	newpath = ['']
# 	for i in sys.path:
# 		if os.path.dirname(sys.executable) in i:
# 			newpath.append(i)
# 	print(sys.path, "\n", newpath)
# 	return newpath


def run():
	from osr2mp4.osr2mp4 import Osr2mp4
	abspath = os.path.dirname(os.path.abspath(inspect.getsourcefile(Dummy)))
	execpath = sys.argv[1]
	logpath = os.path.join(execpath, "Logs/")

	fprogress = open(os.path.join(abspath, "progress.txt"), "w")
	fprogress.write("0")
	fprogress.close()

	logpath = os.path.join(logpath, "core.log")
	config = os.path.join(abspath, "config.json")
	settings = os.path.join(abspath, "settings.json")
	ppsettings = os.path.join(abspath, "ppsettings.json")
	if not os.path.isfile(ppsettings):
		ppsettings = None

	converter = Osr2mp4(filedata=config, filesettings=settings, filepp=ppsettings, logtofile=True, logpath=logpath)
	converter.startall()

	curprogress = 0
	while curprogress < 99:
		curprogress = converter.getprogress()

		a = False

		if converter.writers is None:
			break

		for i in range(len(converter.writers)):
			if converter.writers[i].is_alive():
				a = True
			if converter.writers[i].exitcode is not None and converter.writers[i].exitcode != 0:
				return
			if converter.drawers[i].exitcode is not None and converter.drawers[i].exitcode != 0:
				return
			if converter.audio is not None:
				if converter.audio.exitcode is not None and converter.audio.exitcode != 0:
					return
		if not a:
			curprogress = 99

		fprogress = open(os.path.join(abspath, "progress.txt"), "w")
		fprogress.write(str(curprogress))
		fprogress.close()
		print(curprogress)
		time.sleep(1)
	converter.joinall()

	fprogress = open(os.path.join(abspath, "progress.txt"), "w")
	fprogress.write("100")
	fprogress.close()
	time.sleep(0.5)


if __name__ == "__main__":
	try:
		# sys.path = fixpath()
		run()
	except Exception as e:
		abspath = os.path.dirname(os.path.abspath(inspect.getsourcefile(Dummy)))
		ferror = open(os.path.join( "error.txt"), "w")
		ferror.write(repr(e) + str(e))
		ferror.close()

	abspath = os.path.dirname(os.path.abspath(inspect.getsourcefile(Dummy)))
	fprogress = open(os.path.join(abspath, "progress.txt"), "w")
	fprogress.write("done")
	fprogress.close()
