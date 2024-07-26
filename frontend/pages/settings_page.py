from PyQt5 import QtWidgets, QtGui, QtCore
import winreg
import sys

class SettingsPage(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__()
        self.setGeometry(QtCore.QRect(0, 110, 1411, 661))
        self.setStyleSheet("QFrame {background-color: #202120;}")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("section_settings")
        self.setParent(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create the checkbox for Windows startup
        self.start_with_windows_checkbox = QtWidgets.QCheckBox(self)
        self.start_with_windows_checkbox.setGeometry(QtCore.QRect(30, 30, 300, 40))  # Set position and size
        self.start_with_windows_checkbox.setText("Start Nyx with Windows")
        self.start_with_windows_checkbox.setChecked(self.is_startup_enabled())
        self.start_with_windows_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.start_with_windows_checkbox.stateChanged.connect(self.toggle_startup)

    def is_startup_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "Nyx")
            return True
        except WindowsError:
            return False

    def toggle_startup(self, state):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        if state == QtCore.Qt.Checked:
            winreg.SetValueEx(key, "Nyx", 0, winreg.REG_SZ, f"{sys.executable} --minimized")
        else:
            try:
                winreg.DeleteValue(key, "Nyx")
            except WindowsError:
                pass

    def move_checkbox_container(self, x, y):
        self.start_with_windows_checkbox.move(x, y)
        self.placeholder_label.move(x, y + 40)
