from Custom.CustomWidgets import DefaultLabel
from PyQt5.QtCore import QSize
from helper.datahelper import load_name

class StartButton(DefaultLabel):
    def __init__(self, parent):
        super(StartButton, self).__init__(parent)
        self.main_window = parent
        self.img_idle = "images/StartIdle.png"
        self.img_hover = "images/StartHover.png"
        self.layout = self.main_window.start_layout_button
        self.text = None
        super().setup()

    def on_clicked(self):
        filename = load_name(self.main_window.current_config)
        return
        #save(filename)
        if self.proc is None or self.proc.poll() is not None:
            outputfile = open(Log.runosupath, "w")
            self.proc = subprocess.Popen(
                [sys.executable, os.path.join(abspath, "run_osu.py"), self.main_window.execpath], stdout=outputfile,
                stderr=outputfile)
            self.main_window.progressbar.show()