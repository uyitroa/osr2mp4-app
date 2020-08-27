import os
import osr2mp4
import subprocess
import sys
try:
	import Cython
except (ModuleNotFoundError, ImportError):
	subprocess.check_call([sys.executable, "-m", "pip", "install", "cython"])



class cd:
	"""Context manager for changing the current working directory"""

	def __init__(self, newPath):
		self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)


osr2mp4folder = os.path.dirname(osr2mp4.__file__)
curvepath = os.path.join(osr2mp4folder, "ImageProcess/Curves/libcurves/")
with cd(curvepath):
	subprocess.check_call([sys.executable, "setup.py", "build_ext", "--inplace"])

print("\nDone compiling ccurves module. osr2mp4 should run properly now.\n")
print("Trying to compile optional feature ffmpeg video writer...")
ffmpegpath = os.path.join(osr2mp4folder, "VideoProcess/FFmpegWriter/")
with cd(ffmpegpath):
	subprocess.check_call([sys.executable, "setup.py", "build_ext", "--inplace"])
