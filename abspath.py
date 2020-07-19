import inspect
import os


oldpath = os.path.join


def newpath(path, *paths):
	a = oldpath(path, *paths)
	return a.replace("\\", "/")


os.path.join = newpath


class Dummy: pass


abspath = os.path.dirname(os.path.relpath(inspect.getsourcefile(Dummy)))
abspath = abspath.replace("\\", "/")

configpath = os.path.join(abspath, "config.json")
settingspath = os.path.join(abspath, "settings.json")
pppath = os.path.join(abspath, "ppsettings.json")
optionconfigpath = os.path.join(abspath, 'options_config.json')


class Log:
	apppath = "app.log"
	runosupath = "runosu.log"
