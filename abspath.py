import inspect
import os


class Dummy: pass


abspath = os.path.dirname(os.path.relpath(inspect.getsourcefile(Dummy)))
