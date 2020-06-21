import inspect
import os


class Dummy: pass


abspath = os.path.dirname(os.path.abspath(inspect.getsourcefile(Dummy)))
