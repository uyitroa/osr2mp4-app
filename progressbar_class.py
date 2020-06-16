from Parents import Button

class progress_bar(Button):
    def __init__(self, parent):
        super(progress_bar, self).__init__(parent)

        self.default_x = 20
        self.default_y = 430
        self.default_size = 4.2

        self.img_idle = "res/progressbar.png"
        self.img_hover = "res/progressbar.png"
        self.img_click = "res/progressbar.png"

        super().setup()

