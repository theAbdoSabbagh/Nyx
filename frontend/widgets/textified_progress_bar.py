from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel
from PyQt5.QtGui import QFontMetrics, QFont

from backend.internal_data import InternalData

class TextifiedProgressBar(QWidget):
    def __init__(
        self,
        parent,
        value: int,
        label_text: str,
        label_font_size: int,
        label_pos_x: int,
        label_pos_y: int,
        label_width: int,
        label_height: int,
        progress_bar_pos_x: int,
        progress_bar_pos_y: int,
        progress_bar_width: int,
        progress_bar_height: int,
    ):
        super().__init__(parent)
        # First, load the fonts
        self.source_sans_3 = QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3)
        )[0]
        self.source_sans_3_black = QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFontFromData(InternalData.source_sans_3_black)
        )[0]

        # Second we initialize the indentifier text
        self.label = self.create_label(
            label_pos_x, label_pos_y, label_width, label_height, label_text, self.source_sans_3_black, label_font_size, False)

        # Third we initiate the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(progress_bar_pos_x, progress_bar_pos_y, progress_bar_width, progress_bar_height)
        self.progress_bar.setStyleSheet("QProgressBar{\n	background-color: rgb(42, 43, 42);\n    border: 0px;\n}\n\nQProgressBar::chunk {\n    background-color: rgb(22, 23, 22);\n}\n")
        self.progress_bar.setValue(0 if value < 0 else 100 if value > 100 else value)
        self.progress_bar.setTextVisible(False)

        # Now we create the text above the progress bar
        # There are two text labels here, the number which is big, and the percent sign which is small

        # Number label
        number_text = str(value) if value >= 0 else "?"
        self.number_label = QLabel(number_text, self)
        number_font = QFont(self.source_sans_3_black)
        number_font_size = int(label_font_size * 1.733)
        number_font.setPointSize(number_font_size)
        self.number_label.setFont(number_font)
        self.number_label.setStyleSheet("QLabel {\n	background-color: none;\n	color: white;\n}")

        # Calculate the width and height of the label text
        number_font_metrics = QFontMetrics(number_font)
        number_text_width = number_font_metrics.horizontalAdvance(number_text)
        number_text_height = number_font_metrics.height()

        # Calculate the X position to center the label above the progress bar
        number_label_x = int(progress_bar_pos_x + (progress_bar_width - number_text_width) / 2)

        self.number_label.setGeometry(
            number_label_x,
            progress_bar_pos_y - number_text_height - 5,
            number_text_width,
            number_text_height
        )

        # Percent label
        self.percent_label = QLabel("%", self)
        percent_font = QFont(self.source_sans_3)
        percent_font_size = int(number_font_size * 0.5)
        percent_font.setPointSize(percent_font_size)
        self.percent_label.setFont(percent_font)
        self.percent_label.setStyleSheet("QLabel {\n	background-color: none;\n	color: white;\n}")

        # Calculate the width and height of the label text
        percent_font_metrics = QFontMetrics(percent_font)
        percent_text_width = percent_font_metrics.horizontalAdvance("%")
        percent_text_height = percent_font_metrics.height()

        # Calculate the X position to center the label above the progress bar
        percent_label_x = number_label_x + number_text_width + 3

        self.percent_label.setGeometry(
            percent_label_x,
            int(progress_bar_pos_y / 1.06),
            percent_text_width,
            percent_text_height
        )
    
    def set_value(self, value: float, leave_as_float: bool = False):
        if leave_as_float:
            # Get first decimal place only
            value = round(float(value), 1)
            # If the value is 0.0, we set it to 0
            if value == 0.0:
                value = 0
            self.progress_bar.setValue(int(float(value)))
            self.number_label.setText(str(value))
        else:
            self.progress_bar.setValue(int(float(value)))
            self.number_label.setText(str(int(float(value))))

        # Update the position of the number label
        if leave_as_float:
            number_text = str(value)
        else:
            number_text = str(int(float(value)))
        number_font = self.number_label.font()
        number_font_metrics = QFontMetrics(number_font)
        number_text_width = number_font_metrics.horizontalAdvance(number_text)
        number_text_height = number_font_metrics.height()
        number_label_x = int(self.progress_bar.x() + (self.progress_bar.width() - number_text_width) / 2)
        self.number_label.setGeometry(
            number_label_x,
            self.progress_bar.y() - number_text_height - 5,
            number_text_width,
            number_text_height
        )

        # Update the position of the percent label
        percent_font = self.percent_label.font()
        percent_font_metrics = QFontMetrics(percent_font)
        percent_text_width = percent_font_metrics.horizontalAdvance("%")
        percent_text_height = percent_font_metrics.height()
        percent_label_x = number_label_x + number_text_width + 3
        self.percent_label.setGeometry(
            percent_label_x,
            int(self.progress_bar.y() / 1.06),
            percent_text_width,
            percent_text_height
        )

    def create_label(
        self,
        x_position: int,
        y_position: int,
        width: int,
        height: int,
        text: str,
        font_name: str,
        font_size: int,
        is_bold: bool = False,
    ):
        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        font = QtGui.QFont()
        font.setFamily(font_name)
        font.setPointSize(font_size)
        font.setBold(is_bold)
        font.setWeight(75 if is_bold else 50)
        label.setFont(font)
        label.setStyleSheet("QLabel {\n	background-color: none;\n	color: white;\n}")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft) # type: ignore
        label.setText(text)

        return label
