import os
import sys
import multiprocessing
import pystray
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
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

    def _custom_excepthook(self, exception_type, exception_value, traceback):
        self.error_dumper.dump_error(exception_type.__name__, str(exception_value))

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
            self.tray_icon.visible = True

    def show_window(self, icon, item):
        self.main_window.showNormal()
        self.main_window.activateWindow()
        if self.tray_icon:
            self.tray_icon.visible = False

    def exit_app(self, icon, item):
        if self.tray_icon:
            self.tray_icon.visible = False
        self.app.quit()

    def create_tray_icon(self):
        # Load your custom icon
        icon_path = r"icon\nyx.png"
        image = Image.open(icon_path)
        self.tray_icon = pystray.Icon("Nyx", image, "Nyx", self.create_tray_menu())
        self.tray_icon.run()

    def create_tray_menu(self):
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit Nyx", self.exit_app)
        )
        return menu

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
