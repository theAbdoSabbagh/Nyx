from typing import Optional
from base64 import b64decode

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from backend.utils import Utils

class MinimizeButton(QLabel):
    def __init__(
        self,
        father,
        m_w: Optional[QMainWindow] = None,
    ):
        super().__init__()
        self.father = father
        self.m_w = m_w

        self.utils = Utils()
        self.clicked_and_hovering = False
        self.hovering = False

        self.setAlignment(Qt.AlignCenter) # type: ignore
        pixmap = QPixmap()
        pixmap.loadFromData(b64decode(self.utils.get_icon_b64("minus")))
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton: # type: ignore
            self.setStyleSheet("background-color: rgb(90,93,90);")
            return
        self.setStyleSheet("background-color: rgb(80,83,80);")
        self.clicked_and_hovering = True

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor) # type: ignore
        self.hovering = True
        if not self.clicked_and_hovering:
            self.setStyleSheet("background-color: rgb(90,93,90);")

    def leaveEvent(self, event):
        if not self.clicked_and_hovering:
            self.setStyleSheet("background-color: none;")
        self.hovering = False

    def mouseReleaseEvent(self, event):
        if self.clicked_and_hovering and self.rect().contains(event.pos()):
            if self.m_w is not None:
                self.m_w.showMinimized()
            else:
                self.father.showMinimized()
        self.clicked_and_hovering = False
        if event.button() == Qt.RightButton: # type: ignore
            self.setStyleSheet("background-color: rgb(90,93,90);")
            return
        self.setStyleSheet("background-color: none;")
