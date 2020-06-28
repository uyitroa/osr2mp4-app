from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy
from PyQt5.QtCore import pyqtSignal

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(MainWindow)


class Ewindow(QMainWindow,QApplication):
    """docstring for App"""
    resized = pyqtSignal()

    def __init__(self,parent):
        super(Ewindow,self).__init__(parent=parent)
        self.setGeometry(500, 500, 800,800)
        self.setWindowTitle('Mocker')
        self.setWindowIcon(QIcon('icon.png'))
        self.setAttribute(Qt.WA_DeleteOnClose)

        ui2 = Ui_MainWindow()
        ui2.setupUi(self)
        self.resized.connect(self.readjust)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Ewindow, self).resizeEvent(event)

    def readjust(self):

        self.examForm.move(self.width()-self.examForm.width(),0)
        self.btn_skip.move(self.width()-self.btn_skip.width(),self.height()-100)
        self.btn_next.move(self.btn_showAnswers.x()+self.btn_showAnswers.width(),self.height()-100)
        self.btn_prev.move(0,self.height()-100)
        self.btn_showAnswers.move(self.btn_prev.x()+self.btn_prev.width(),self.height()-100)
        self.btn_home.move(self.width()-200,self.height()-150)

        self.lbscreen1.resize(self.width()-self.examForm.width(),self.height()-200)
        self.examForm.resize(200,self.height()-150)
        self.btn_skip.resize(self.examForm.width(),100)
        self.btn_next.resize(self.btn_prev.width(),100)
        self.btn_prev.resize(self.width()*0.25,100)
        self.btn_showAnswers.resize(self.btn_prev.width(),100)
        self.btn_home.resize(200,50)
