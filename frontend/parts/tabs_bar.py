from time import time
from typing import Optional
from base64 import b64decode

from PyQt5 import QtWidgets, QtGui, QtCore

from backend.logger import Logger
from backend.timer import Timer
from backend.utils import Utils
from backend.internal_data import InternalData

class TabsBar(QtWidgets.QFrame):
    def __init__(
        self,
        father,
    ):
        super().__init__()
        with Timer(__class__.__name__):
            self.logger = Logger()
            self.father = father
            self.utils = Utils()

            self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # type: ignore
            self.setGeometry(QtCore.QRect(0, 50, 1411, 61))
            self.setStyleSheet("QFrame {background-color: #202120;}")
            self.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.setFrameShadow(QtWidgets.QFrame.Raised)
            self.setObjectName("frame")

            self.device_monitor_button = self.create_push_button(50, 0, 281, 61, "Device Monitor", 14, "chart", False)
            self.gaming_mode_button = self.create_push_button(370, 0, 261, 61, "Gaming Mode", 14, "joystick", False)
            self.turbo_mode_button = self.create_push_button(670, 0, 231, 61, "Turbo Mode", 14, "bolt", False)
            self.settings_button = self.create_push_button(940, 0, 201, 61, "Settings", 14, "cog", False)
            self.discord_button = self.create_push_button(1240, 0, 141, 61, "Discord", 14, "discord", True)

            self.last_button = None
            self.choose_button(self.device_monitor_button)

    def create_push_button(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        text: str,
        font_size: int,
        icon_name: Optional[str] = None,
        interactive_hover: bool = False,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(self)
        button.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        font = QtGui.QFont()
        source_sans_3_black = QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3_black)
        )[0]
        font.setFamily(source_sans_3_black)
        font.setPointSize(font_size)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setText(text)
        button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        if icon_name:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(b64decode(self.utils.get_icon_b64(icon_name))) # type: ignore
            icon = QtGui.QIcon()
            icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            button.setIconSize(QtCore.QSize(100, 100))
            button.setIcon(icon)

        stylsheet = "QPushButton {\n	border: 0px;\n	border-bottom: 2px solid transparent;\n	color: white;\n	background-color: transparent;\n	font-weight: bold;\n}"
        if interactive_hover:
            stylsheet = "QPushButton {\n    border: 0px;\n    border-bottom: 2px solid transparent;\n    color: rgb(255, 255, 255);\n    background-color: transparent;\n    font-weight: bold;\n}\n\nQPushButton:hover {\n    color: rgba(255, 255, 255, 0.9);\n}\n\nQPushButton:pressed {\n    color: rgba(255, 255, 255, 0.7);\n}\n"
            button.setStyleSheet(stylsheet)
        else:
            button.setStyleSheet(stylsheet)

        button.clicked.connect(lambda: self.choose_button(button))
        return button

    def choose_button(self, button: QtWidgets.QPushButton):
        if self.last_button:
            stylsheet = "QPushButton {\n	border: 0px;\n	border-bottom: 2px solid transparent;\n	color: white;\n	background-color: transparent;\n	font-weight: bold;\n}"
            self.last_button.setStyleSheet(stylsheet)

        stylesheet = "QPushButton {\n	border: 0px;\n	border-bottom: 2px solid white;\n	color: white;\n	background-color: transparent;\n	font-weight: bold;\n}"
        button.setStyleSheet(stylesheet)
        self.logger.debug(f"Chose {button.text()}")
        self.last_button = button
