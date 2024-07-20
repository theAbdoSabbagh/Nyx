from PyQt5 import QtCore, QtWidgets

from .parts.title_bar import TitleBar
from .parts.tabs_bar import TabsBar
from .pages.device_monitor import DeviceMonitor

from backend.logger import Logger
from backend.timer import Timer

# from .mini_dialog import NyxDialog
 
class Nyx(object):
    def __init__(self, app: QtWidgets.QApplication, scale_factor: float):
        super().__init__()
        self.app = app
        self.scale_factor = scale_factor
        self.logger = Logger()
        self.m_mouse_down = False

    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        with Timer(__class__.__name__):
            MainWindow.moving = False # Necessary for making the titlebar moveable

            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(int(1408 / self.scale_factor), int(769 / self.scale_factor))

            MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint) # type: ignore
            MainWindow.setMouseTracking(True)

            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")

            self.title_bar = TitleBar(MainWindow)
            self.title_bar.setParent(self.centralwidget)

            self.tabs_bar = TabsBar(MainWindow)
            self.tabs_bar.setParent(self.centralwidget)

            self.centralwidget.title_bar = self.title_bar

            self.device_monitor_body = DeviceMonitor(self.centralwidget)

            MainWindow.setCentralWidget(self.centralwidget)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            
            self.main_window = MainWindow

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== QtCore.Qt.LeftButton # type: ignore

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
