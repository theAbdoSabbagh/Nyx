import os
import sys
import multiprocessing
from PyQt5 import QtWidgets, QtCore, QtGui

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from backend.logger import Logger
from backend.error_dumper import ErrorDumper
from backend.utils import Utils
from backend.nyx_base import NyxBase
from backend.timer import Timer
from frontend.nyx import Nyx

# Ensure high DPI scaling attributes are set before creating QApplication
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class AppRunner:
    def __init__(self):
        # Initialize the mutex to check for existing instances
        self.mutex = QtCore.QSharedMemory("unique_application_key")
        if self.mutex.attach(QtCore.QSharedMemory.ReadOnly):
            # Only show notification if this is the main instance
            if not hasattr(sys, '_called_from_test'):
                self.show_instance_notification()
            sys.exit(0)  # Exit if another instance is running
        
        # Try to create the mutex
        if not self.mutex.create(1):
            print("Failed to create mutex.")
            sys.exit(1)

        with Timer(__class__.__name__):
            self.app = QtWidgets.QApplication(sys.argv)
            self.logger = Logger()
            self.utils = Utils()
            self.nyx_base = NyxBase()
            self.nyx_path, self.error_logs_path = self.utils.create_nyx_folders()
            self.error_dumper = ErrorDumper(self.error_logs_path)
            # Set the custom excepthook
            sys.excepthook = self._custom_excepthook
            self.tray_icon = None
            self.start_minimized = "--minimized" in sys.argv  # Add this line

    def _custom_excepthook(self, exception_type, exception_value, traceback):
        self.error_dumper.dump_error(exception_type.__name__, str(exception_value))

    def show_instance_notification(self):
        # Create a QApplication instance to show the notification
        notification_app = QtWidgets.QApplication(sys.argv)
        
        # Create a QDialog to show the message
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setText("Another instance of Nyx is already running.")
        msg_box.setInformativeText("Check the system tray for the running instance.")
        msg_box.setWindowTitle("Nyx Already Running")
        msg_box.setModal(True)
        msg_box.exec_()
        
        # Close the notification application
        notification_app.quit()

    def calculate_scale_factor(self, app):
        screen = app.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        base_dpi = self.nyx_base.get_dpi()
        
        # Calculate the DPI scale factor
        dpi_scale_factor = dpi / base_dpi

        # Get the screen's current resolution
        screen_resolution = screen.size()
        base_resolution = self.nyx_base.get_screen_resolution()

        # Calculate the resolution scale factor
        res_scale_factor_width = screen_resolution.width() / base_resolution[0]
        res_scale_factor_height = screen_resolution.height() / base_resolution[1]

        # Use the smaller scale factor to ensure proper scaling
        res_scale_factor = min(res_scale_factor_width, res_scale_factor_height)

        # Calculate the final scale factor
        scale_factor = dpi_scale_factor * res_scale_factor

        return scale_factor

    def hide_window(self):
        self.main_window.hide()
        if self.tray_icon:
            self.tray_icon.setVisible(True)

    def show_window(self):
        self.main_window.showNormal()
        self.main_window.activateWindow()
        if self.tray_icon:
            self.tray_icon.setVisible(False)

    def exit_app(self):
        if self.tray_icon:
            self.tray_icon.setVisible(False)
        QtWidgets.QApplication.quit()

    def create_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(sys.argv[0]), "frontend/icons/nyx.png")
        if not os.path.exists(icon_path):
            if hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(sys._MEIPASS, "frontend/icons/nyx.png")
        
        icon = QtGui.QIcon(icon_path)
        self.tray_icon = QtWidgets.QSystemTrayIcon(icon, self.app)
        
        # Create the context menu
        tray_menu = QtWidgets.QMenu()
        show_action = tray_menu.addAction("Show")
        exit_action = tray_menu.addAction("Exit Nyx")
        
        show_action.triggered.connect(self.show_window)
        exit_action.triggered.connect(self.exit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # Connect the activated signal to handle left-click event
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show_window()

    def run(self):
        self.logger.debug("Displaying main window")

        try:
            self.scale_factor = self.calculate_scale_factor(self.app)
            self.logger.debug(f"Successful scale factor: {self.scale_factor}")
        except Exception as e:
            self.scale_factor = 1
            self.logger.debug(f"Default scale factor: {self.scale_factor}, Exception: {e}")

        self.main_window = QtWidgets.QMainWindow()
        ui = Nyx(self.app, self.scale_factor)
        ui.setupUi(self.main_window)
        self.main_window.setWindowTitle("Nyx")
        
        if self.start_minimized:  
            self.hide_window()
        else:
            self.main_window.show()

        # Override the close event
        self.main_window.closeEvent = self.close_event

        # Connect the minimize event
        self.main_window.changeEvent = self.change_event

        self.create_tray_icon()
        sys.exit(self.app.exec())

    def close_event(self, event):
        event.ignore()
        self.hide_window()

    def change_event(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.main_window.isMinimized():
                self.hide_window()

if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()

    app_runner = AppRunner()
    app_runner.run()
