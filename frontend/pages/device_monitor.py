import time

from typing import Optional, Callable

from PyQt5 import QtCore, QtGui, QtWidgets

from backend.nyx_base import NyxBase
from backend.utils import Utils
from backend.logger import Logger
from backend.timer import Timer
from backend.objects import Row
from backend.internal_data import InternalData

from frontend.widgets.round_progress_bar import QRoundProgressBar
from frontend.widgets.textified_progress_bar import TextifiedProgressBar

class LabelUpdater(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self, function: Callable, interval: int, parent=None):
        super().__init__(parent)
        self.function = function
        self.interval = interval

    def run(self):
        while True:
            value = self.function()
            self.update_signal.emit(str(value))
            self.msleep(self.interval)

            if self.interval == 0: # Run only once when interval is 0
                break

class DeviceMonitor(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__()
        with Timer(__class__.__name__):
            self.logger = Logger()
            self.utils = Utils()
            self.nyx_base = NyxBase()
            self.title = "Device Monitor"
            self.information_rows = {}
            self.threads = []
            
            self.setGeometry(QtCore.QRect(0, 110, 1411, 661))
            self.setStyleSheet("QFrame {background-color: #202120;}")
            self.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.setFrameShadow(QtWidgets.QFrame.Raised)
            self.setObjectName("section_deviceMonitor")
            self.setParent(parent)

            self.source_sans_3 = QtGui.QFontDatabase.applicationFontFamilies(
                QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3)
            )[0]
            self.source_sans_3_black = QtGui.QFontDatabase.applicationFontFamilies(
                QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3_black)
            )[0]

            self.computer_model = self.create_label(
                50, 40, 241, 61, "Computer Model", self.source_sans_3_black, 10, True,
                function=self.nyx_base.get_computer_model, timer_interval=0
            )
            self.cpu_usage_label = self.create_label(
                50, 100, 131, 51, "CPU Usage", self.source_sans_3, 10, True,
            )
            self.gpu_usage_label = self.create_label(
                450, 100, 131, 51, "GPU Usage", self.source_sans_3, 10, True,
            )

            self.gpu_usage_progress = QRoundProgressBar(self, font_size=30, default_color=QtGui.QColor(42, 43, 42, 255),
                progress_color=QtGui.QColor(22, 23, 22, 255), inner_background_color=QtGui.QColor(32, 33, 32, 255), width=0.175)
            self.gpu_usage_progress.setGeometry(QtCore.QRect(470, 160, 241, 241))
            gpu_usage_updater = LabelUpdater(self.nyx_base.get_gpu_usage, 1000)
            gpu_usage_updater.update_signal.connect(lambda value: self.gpu_usage_progress.set_value(int(float(value))))
            gpu_usage_updater.start()

            self.cpu_usage_progress = QRoundProgressBar(self, font_size=30, default_color=QtGui.QColor(42, 43, 42, 255),
                progress_color=QtGui.QColor(22, 23, 22, 255), inner_background_color=QtGui.QColor(32, 33, 32, 255), width=0.175)
            self.cpu_usage_progress.setGeometry(QtCore.QRect(70, 160, 241, 241))
            cpu_usage_updater = LabelUpdater(self.nyx_base.get_cpu_usage, 1000)
            cpu_usage_updater.update_signal.connect(lambda value: self.cpu_usage_progress.set_value(int(float(value))))
            cpu_usage_updater.start()

            self.harddisk_bar = TextifiedProgressBar(
                parent=self,
                value=-1,
                label_text="Disk",
                label_font_size=10,  # Adjusted font size to 10
                label_pos_x=50,
                label_pos_y=450,
                label_width=201,
                label_height=51,
                progress_bar_pos_x=80,
                progress_bar_pos_y=570,
                progress_bar_width=221,
                progress_bar_height=16,
            )
            harddisk_bar_updater = LabelUpdater(lambda: self.nyx_base.get_harddisk_info().used_percent, 60 * 1000)
            harddisk_bar_updater.update_signal.connect(lambda value: self.harddisk_bar.set_value(value))
            harddisk_bar_updater.start()
            harddisk_label_updater = LabelUpdater(lambda: self.nyx_base.get_harddisk_info().labelized, 0)
            harddisk_label_updater.update_signal.connect(lambda value: self.harddisk_bar.label.setText(value))
            harddisk_label_updater.start()
            self.memory_bar = TextifiedProgressBar(
                parent=self,
                value=-1,
                label_text="Memory",
                label_font_size=10,  # Adjusted font size to 10
                label_pos_x=450,
                label_pos_y=450,
                label_width=101,
                label_height=51,
                progress_bar_pos_x=480,
                progress_bar_pos_y=570,
                progress_bar_width=221,
                progress_bar_height=16,
            )
            memory_bar_updater = LabelUpdater(lambda: self.nyx_base.get_ram_info().used_percent, 1000)
            memory_bar_updater.update_signal.connect(lambda value: self.memory_bar.set_value(value))
            memory_bar_updater.start()

            # Creating the scrollable frame and area
            self.scroll_frame = self.create_frame(
                self, 860, 140, 541, 531,
                stylesheet="QScrollArea { border: none; }\nQScrollBar:vertical { background: transparent; width: 12px; margin: 2px 0 2px 0; border-radius: 6px; }\nQScrollBar::handle:vertical { background: rgb(90,93,90); min-height: 20px; border-radius: 6px; }\nQScrollBar::handle:vertical:hover { background: rgb(80,83,80); }\nQScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; height: 0; }\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }\n"
            )

            self.scroll_area = QtWidgets.QScrollArea(self.scroll_frame)
            self.scroll_area.setGeometry(QtCore.QRect(10, 0, 531, 501))
            self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            self.scrollable_content = QtWidgets.QWidget()
            self.scrollable_content.setGeometry(QtCore.QRect(0, -157, 519, 0))
            self.scrollable_content.setStyleSheet("background-color: transparent;")

            self.vertical_layout = QtWidgets.QVBoxLayout(self.scrollable_content)

            self.scrollable_content_frame = self.create_frame(self.scrollable_content, 0, 0, 519, 658, "transparent")
            self.scrollable_content_frame.setMinimumSize(QtCore.QSize(0, 640))

            
            self.nyx_eyes_label = QtWidgets.QLabel(self)
            self.nyx_eyes_label.setGeometry(QtCore.QRect(880, 100, 32, 33)) 
            self.nyx_eyes_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.nyx_eyes_label.setStyleSheet("QLabel { background-color: none; }")

 
            nyx_eyes_pixmap = QtGui.QPixmap("frontend/img/eyes.png")
            self.nyx_eyes_label.setPixmap(nyx_eyes_pixmap)
            self.nyx_eyes_label.setScaledContents(True)  
         
            self.this_computer_label = self.create_label(
                840, 100, 300, 30, "System Stats", self.source_sans_3_black, 14, True, underline=True
            )

            cpu_info_row = self.create_info_row("Loading", function=self.nyx_base.get_cpu_name)
            gpu_info_row = self.create_info_row("Loading", function=self.nyx_base.get_gpu_name)
            cpu_temperature_info_row = self.create_info_row(
                "CPU Temperature", "?°C",
                function=lambda: f"{round(self.nyx_base.get_cpu_temperature(), 1)}°C",
                timer_interval=2500)
            gpu_temperature_info_row = self.create_info_row(
                "GPU Temperature", "?°C",
                function=lambda: f"{round(self.nyx_base.get_gpu_temperature(), 1)}°C",
                timer_interval=2500)
            ram_info_row = self.create_info_row("RAM", "Loading", function=lambda: f"{self.nyx_base.get_ram_info().total} GB")
            disk_info_row = self.create_info_row("Disk", "Loading", function=lambda: f"{self.nyx_base.get_disk_io_percentage():.2f}%")
            wifi_download_info_row = self.create_info_row("WiFi (Download)", "? Bytes/s", function=lambda: f"{self.nyx_base.get_network_speed('Wi-Fi').download_labelized}", timer_interval=250)
            wifi_upload_info_row = self.create_info_row("WiFi (Upload)", "? Bytes/s", function=lambda: f"{self.nyx_base.get_network_speed('Wi-Fi').upload_labelized}", timer_interval=250)
            lan_download_info_row = self.create_info_row("LAN (Download)", "? Bytes/s", function=lambda: f"{self.nyx_base.get_network_speed('Ethernet').download_labelized}", timer_interval=250)
            lan_upload_info_row = self.create_info_row("LAN (Upload)", "? Bytes/s", function=lambda: f"{self.nyx_base.get_network_speed('Ethernet').upload_labelized}", timer_interval=250)
            gpu_clock_info_row = self.create_info_row("GPU Clock", "? MHz", function=lambda: f"{self.nyx_base.get_gpu_clock()} MHZ", timer_interval=10000)
            vram_clock_info_row = self.create_info_row("VRAM Clock", "? MHz", function=lambda: f"{int(self.nyx_base.get_ram_info().clock)} MHZ", timer_interval=10000)
            power_plan_info_row = self.create_info_row("Power Plan", "Loading", function=self.nyx_base.get_power_plan)

            # Adding the content frame to the layout
            self.vertical_layout.addWidget(self.scrollable_content_frame)
            self.scroll_area.setWidget(self.scrollable_content)

    def create_label(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        text: str,
        font_name: str,
        font_size: int = 10,  # Adjusted font size to 10
        is_bold: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        function: Optional[Callable] = None,
        timer_interval: int = 0,
        underline: bool = False,  # Added underline parameter
    ):
        label = QtWidgets.QLabel(parent or self)
        label.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        font = QtGui.QFont()
        font.setFamily(font_name)
        font.setPointSize(font_size)
        font.setBold(is_bold)
        font.setUnderline(underline)  # Set underline
        font.setWeight(75 if is_bold else 50)
        label.setFont(font)
        label.setStyleSheet("QLabel { background-color: none; color: white; }")
        label.setAlignment(alignment)
        label.setText(text)

        if function:
            label_updater = LabelUpdater(function, timer_interval)
            label_updater.update_signal.connect(lambda value: label.setText(value))
            label_updater.start()
            self.threads.append(label_updater)

        return label

    def create_frame(
        self,
        parent,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        bg_color: str = "transparent",
        border: str = "none",
        stylesheet: Optional[str] = None,
    ):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        if stylesheet:
            frame.setStyleSheet(stylesheet)
        else:
            frame.setStyleSheet(f"QFrame {{ background-color: {bg_color}; border: {border}; }}")
        return frame

    def create_info_row(
        self,
        label_text: str,
        value_text: str = "",
        index: int = -1,
        function: Optional[Callable] = None,
        timer_interval: int = 0,
    ):
        if index == -1:
            index = len(self.information_rows)
        
        assert index not in self.information_rows, "Index already exists in information rows"

        double_label = True if value_text else False
        dark = index != 0 and (index + 1) % 2 == 0
        
        # Creating the frame
        self.information_rows[index] = self.create_frame(
            parent=self.scrollable_content_frame,
            x_position=0,
            y_position=-10 if index == 0 else index * 50,
            width=481,
            height=51,
            bg_color="rgb(42, 43, 42)" if dark else "transparent",
        )

        # Creating the label
        first_label = self.create_label(
            x_position=10,
            y_position=0,
            width=211 if double_label else 471,
            height=51,
            text=label_text,
            font_name=self.source_sans_3,
            font_size=10,  # Adjusted font size to 10
            is_bold=False,
            parent=self.information_rows[index],
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,  # type: ignore
        )

        if double_label:
            second_label = self.create_label(
                x_position=260,
                y_position=0,
                width=211,
                height=51,
                text=value_text,  # type: ignore
                font_name=self.source_sans_3,
                font_size=10,  # Adjusted font size to 10
                is_bold=False,
                parent=self.information_rows[index],
                alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,  # type: ignore
            )

        if function:
            label_updater = LabelUpdater(function, timer_interval)
            if double_label:
                label_updater.update_signal.connect(lambda value: second_label.setText(value))
            else:
                label_updater.update_signal.connect(lambda value: first_label.setText(value))
            label_updater.start()  # Start the thread
            self.threads.append(label_updater)

        # Update scrollable_content height
        self.scrollable_content.setMinimumSize(QtCore.QSize(0, (index + 1) * 50 + 15))

        return Row(
            label_text=label_text,
            value_text=value_text,
            dark=dark,
            index=index,
        )
