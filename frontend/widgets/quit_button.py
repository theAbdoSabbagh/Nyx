from typing import Optional
from base64 import b64decode

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from backend.utils import Utils

class QuitButton(QLabel):
    def __init__(
        self,
        father,
        m_w: Optional[QMainWindow] = None,
        auto_close: bool = True
    ):
        super().__init__()
        self.father = father
        self.m_w = m_w
        self.auto_close = auto_close

        self.utils = Utils()
        self.clicked_and_hovering = False
        self.hovering = False

        self.setAlignment(Qt.AlignCenter) # type: ignore
        pixmap = QPixmap()
        pixmap.loadFromData(b64decode(self.utils.get_icon_b64("title_bar_quit"))) # type: ignore
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton: # type: ignore
            self.setStyleSheet("background-color: #e71022;")
            return
        self.setStyleSheet("background-color: #971721;")
        self.clicked_and_hovering = True

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor) # type: ignore
        self.hovering = True
        if not self.clicked_and_hovering:
            self.setStyleSheet("background-color: #e71022;")

    def leaveEvent(self, event):
        if not self.clicked_and_hovering:
            self.setStyleSheet("background-color: none;")
        self.hovering = False

    def mouseReleaseEvent(self, event):
        if self.clicked_and_hovering and self.rect().contains(event.pos()):
            if self.m_w is not None and not self.auto_close:
                self.m_w.close_the_popup = True
            else:
                self.father.close()
        self.clicked_and_hovering = False
        if event.button() == Qt.RightButton: # type: ignore
            self.setStyleSheet("background-color: #e71022;")
            return
        self.setStyleSheet("background-color: none;")
