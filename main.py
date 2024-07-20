import os, sys, multiprocessing
from PyQt5 import QtWidgets, QtCore
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

    def _custom_excepthook(self, exception_type, exception_value, traceback):
        self.error_dumper.dump_error(
            exception_type.__name__,
            str(exception_value),
        )

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

    def run(self):
        self.logger.debug("Displaying main window")
        self.app = None
        self.app = QtWidgets.QApplication(sys.argv)

        try:
            self.scale_factor = self.calculate_scale_factor(self.app)
            self.logger.debug(f"Successful scale factor: {self.scale_factor}")
        except Exception as e:
            self.scale_factor = 1
            self.logger.debug(f"Default scale factor: {self.scale_factor}, Exception: {e}")

        MainWindow = QtWidgets.QMainWindow()
        ui = Nyx(self.app, self.scale_factor)
        ui.setupUi(MainWindow)
        MainWindow.setWindowTitle("Nyx")
        MainWindow.show()
        sys.exit(self.app.exec() + 69)

if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()

    app_runner = AppRunner()
    app_runner.run()
