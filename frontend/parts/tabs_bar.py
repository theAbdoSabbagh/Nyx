import sys
import os
from typing import Optional
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from backend.logger import Logger
from backend.utils import Utils
from base64 import b64decode

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TabsBar(QtWidgets.QFrame):
    def __init__(self, father):
        super().__init__()
        self.logger = Logger()
        self.father = father
        self.utils = Utils()
        
        sound_path = resource_path('frontend/sounds/UIClick.wav')
        self.click_sound = QtMultimedia.QSoundEffect()
        self.click_sound.setSource(QtCore.QUrl.fromLocalFile(sound_path))
        self.click_sound.setVolume(0.5)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # type: ignore
        self.setGeometry(QtCore.QRect(0, 50, 1411, 61))
        self.setStyleSheet("QFrame {background-color: #202120;}")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame")

        self.device_monitor_button = self.create_push_button(50, 0, 281, 61, "Device Monitor", 14, "chart", False)
        self.settings_button = self.create_push_button(370, 0, 201, 61, "Settings", 14, "cog", False)
        

        self.last_button = None
        self.choose_button(self.device_monitor_button)

        # Connect buttons to their respective functions
        self.device_monitor_button.clicked.connect(self.on_device_monitor_clicked)
        self.settings_button.clicked.connect(self.on_settings_clicked)

    def create_push_button(self, x_position: int, y_position: int, width: int, height: int, text: str, font_size: int, icon_name: Optional[str] = None, interactive_hover: bool = False) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(self)
        button.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        font = QtGui.QFont()
        font.setFamily("source_sans_3_black")
        font.setPointSize(font_size)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setText(text)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        if icon_name:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(b64decode(self.utils.get_icon_b64(icon_name)))  # type: ignore
            icon = QtGui.QIcon()
            icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIconSize(QtCore.QSize(100, 100))
            button.setIcon(icon)

        stylesheet = "QPushButton {\n\tborder: 0px;\n\tborder-bottom: 2px solid transparent;\n\tcolor: white;\n\tbackground-color: transparent;\n\tfont-weight: bold;\n}"
        if interactive_hover:
            stylesheet = "QPushButton {\n    border: 0px;\n    border-bottom: 2px solid transparent;\n    color: rgb(255, 255, 255);\n    background-color: transparent;\n    font-weight: bold;\n}\n\nQPushButton:hover {\n    color: rgba(255, 255, 255, 0.9);\n}\n\nQPushButton:pressed {\n    color: rgba(255, 255, 255, 0.7);\n}\n"
            button.setStyleSheet(stylesheet)
        else:
            button.setStyleSheet(stylesheet)

        button.clicked.connect(lambda: self.handle_button_click(button))
        return button

    def handle_button_click(self, button: QtWidgets.QPushButton):
        self.click_sound.play()
        self.choose_button(button)

    def choose_button(self, button: QtWidgets.QPushButton):
        if self.last_button:
            stylesheet = "QPushButton {\n\tborder: 0px;\n\tborder-bottom: 2px solid transparent;\n\tcolor: white;\n\tbackground-color: transparent;\n\tfont-weight: bold;\n}"
            self.last_button.setStyleSheet(stylesheet)

        stylesheet = "QPushButton {\n\tborder: 0px;\n\tborder-bottom: 2px solid white;\n\tcolor: white;\n\tbackground-color: transparent;\n\tfont-weight: bold;\n}"
        button.setStyleSheet(stylesheet)
        self.logger.debug(f"Chose {button.text()}")
        self.last_button = button

    def on_settings_clicked(self):
        self.father.show_settings_page()

    def on_device_monitor_clicked(self):
        self.father.show_device_monitor_page()
