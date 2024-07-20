from time import time
from typing import Optional

from PyQt5 import QtWidgets, QtGui, QtCore

from backend.logger import Logger
from backend.timer import Timer
from backend.internal_data import InternalData

from frontend.widgets.quit_button import QuitButton
from frontend.widgets.minimize_button import MinimizeButton

class TitleBar(QtWidgets.QFrame):
    def __init__(
        self,
        father, # The father that's moveable and shi is MainWindow not the whole application
    ):
        super().__init__()
        with Timer(__class__.__name__):
            self.logger = Logger()
            self.father = father

            self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # type: ignore
            self.setGeometry(QtCore.QRect(0, 0, 1411, 51))
            self.setStyleSheet("QFrame {background-color: #1A1A1A;}")
            self.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.setFrameShadow(QtWidgets.QFrame.Raised)
            self.setObjectName("frame")

            self.titlebar_nyx = self.create_label(20, 0, 61, 51, "Nyx", 16, True)
            self.titlebar_quit = QuitButton(father)
            self.titlebar_quit.setGeometry(QtCore.QRect(1340, 0, 71, 51))
            self.titlebar_quit.setParent(self)
            self.titlebar_minimize = MinimizeButton(father)
            self.titlebar_minimize.setGeometry(QtCore.QRect(1270, 0, 71, 71))
            self.titlebar_minimize.setParent(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton: # type: ignore
            self.father.moving = True
            self.father.offset = event.pos()
        if event.button() == QtCore.Qt.RightButton: # type: ignore
            self.father.moving = False

    def mouseMoveEvent(self, event):
        if self.father.moving:
            if self.titlebar_quit.hovering is True:
                return
            if self.titlebar_minimize.hovering is True:
                return
            self.father.move(event.globalPos() - self.father.offset)

    def create_label(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        text: str,
        font_size: int,
        is_bold: bool = False,
        bg_color: Optional[str] = None
    ):
        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        font = QtGui.QFont()
        source_sans_3_black = QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3_black)
        )[0]
        font.setFamily(source_sans_3_black)
        font.setPointSize(font_size)
        font.setBold(is_bold)
        font.setWeight(75 if is_bold else 50)
        label.setFont(font)
        label.setStyleSheet("QLabel {background-color: none; color: white;}" if bg_color is None else f"QLabel {{background-color: {bg_color}; color: white;}}")
        label.setAlignment(QtCore.Qt.AlignCenter) # type: ignore
        label.setObjectName("header_" + text.lower().replace(" ", "_"))

        label.setText(text)

        return label
