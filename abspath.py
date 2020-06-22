import inspect
import os
import ntpath


oldpath = os.path.join

def newpath(path, *paths):
	a = oldpath(path, *paths)
	return a.replace("\\", "/")


os.path.join = newpath


class Dummy: pass


abspath = os.path.dirname(os.path.relpath(inspect.getsourcefile(Dummy)))
abspath = abspath.replace("\\", "/")
print(abspath)
