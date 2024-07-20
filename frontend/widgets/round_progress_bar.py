from PyQt5.QtCore import pyqtSlot, Qt, QRectF
from PyQt5.QtGui import (QBrush, QColor, QFont, QPainter,
                         QPen, QPainterPath, QImage, QPaintEvent)
from PyQt5.QtWidgets import QWidget

class QRoundProgressBar(QWidget):
    def __init__(
        self,
        parent = None,
        font_size: int = 10,
        default_color: QColor = QColor(255, 255, 255, 255),
        progress_color: QColor = QColor(0, 0, 0),
        background_color: QColor = QColor(255, 255, 255, 0),
        inner_background_color: QColor = QColor(0, 0, 0),
        inner_radius: float = 0.75,
        width: float = 0.1,  # New argument to control the width of the bar
    ):
        super().__init__(parent)
        self.current_value = 0
        self.start_position = 90
        self.font_size = font_size
        self.default_color = default_color
        self.progress_color = progress_color
        self.background_color = background_color
        self.inner_background_color = inner_background_color
        self.inner_radius = inner_radius
        self.width_ = width  # Initialize the width attribute

    @pyqtSlot(int)
    def set_value(self, val: int):
        self.current_value = val if 0 <= val <= 100 else 0 if val < 0 else 100
        self.update()

    def paintEvent(self, event: QPaintEvent):
        widget_dimensions = min(self.width(), self.height())
        widget_container = QRectF(1, 1, widget_dimensions - 2, widget_dimensions - 2)
        progress_bar = QImage(
            widget_dimensions,
            widget_dimensions,
            QImage.Format_ARGB32_Premultiplied  # A format that supports transparency
        )

        painter = QPainter(progress_bar)  # Create a painter to draw the progress bar
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing for smoother drawing

        # Clear the image with a transparent background
        progress_bar.fill(Qt.GlobalColor.transparent)

        # Draw the default color of the progress bar
        self.draw_default_color(painter, widget_container)
        # Draw the progress bar
        self.draw_progress(painter, widget_container, self.current_value)

        # Calculate the inner rectangle and radius for the progress bar
        inner_rect, inner_radius = self.calculate_inner_rect(widget_dimensions)

        # Draw the inner background of the progress bar
        self.draw_inner_background(painter, inner_rect)

        # Draw the text on the progress bar
        self.draw_text(painter, inner_rect, self.current_value)

        # Finish drawing on the buffer image
        painter.end()

        # Create a painter to draw on the widget
        main_painter = QPainter(self)

        # Make the background of the widget transparent
        main_painter.fillRect(widget_container, Qt.GlobalColor.transparent)

        # Draw the progress bar on the widget
        main_painter.drawImage(0, 0, progress_bar)

    def draw_progress(self, painter: QPainter, widget_container: QRectF, value: float):
        data_path = QPainterPath()
        data_path.setFillRule(Qt.FillRule.WindingFill)

        arc_length = 360 * (value / 100.0)  # Calculate the length of the arc

        # Draw the progress bar arc
        data_path.moveTo(widget_container.center())
        outer_rect = widget_container.adjusted(-1, -1, 1, 1)
        data_path.arcTo(outer_rect, self.start_position, -arc_length)
        data_path.lineTo(widget_container.center())

        painter.setBrush(QBrush(self.progress_color))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawPath(data_path)

    def draw_default_color(self, painter: QPainter, widget_container: QRectF):
        data_path = QPainterPath()
        data_path.setFillRule(Qt.FillRule.WindingFill)

        # Outer ellipse for default color
        data_path.addEllipse(widget_container)

        painter.setBrush(QBrush(self.default_color))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawPath(data_path)

    def calculate_inner_rect(self, widget_dimensions: float):
        # This is the area inside the progress bar
        outer_radius = widget_dimensions / 2
        inner_radius = outer_radius * (1 - self.width_)  # Adjusted to use the width argument
        delta = outer_radius - inner_radius
        inner_rect = QRectF(delta, delta, inner_radius * 2, inner_radius * 2)
        return inner_rect, inner_radius

    def draw_inner_background(self, painter: QPainter, inner_rect: QRectF):
        # This is the area inside the progress bar
        painter.setBrush(QBrush(self.inner_background_color))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawEllipse(inner_rect)

    def draw_text(self, painter: QPainter, inner_rect: QRectF, value: float):
        # Set the initial font and calculate metrics
        number_font = QFont('Source Sans 3 Black')
        number_font.setPointSize(self.font_size)
        number_font.setBold(True)
        number_font.setWeight(75)

        painter.setFont(number_font)

        # Draw the text on the progress bar and move it upwards a bit
        text_rect = QRectF(inner_rect)
        text_rect.moveTop(text_rect.top() - number_font.pointSize() * 0.2)

        # Set text color to white
        painter.setPen(QPen(QBrush(QColor(255, 255, 255)), 1))  # White color
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.value_to_text(value))

        # Draw text "%" under the value and make it smaller
        percentage_font = QFont('Source Sans 3')
        percentage_font.setPointSize(int(number_font.pointSize() / 1.75))
        painter.setFont(percentage_font)
        text_rect.moveTop(text_rect.top() + (percentage_font.pointSize() * 3) * self.inner_radius)

        # Set text color to white
        painter.setPen(QPen(QBrush(QColor(255, 255, 255)), 1))  # White color
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, '%')

    def value_to_text(self, value: float):
        text_to_draw = str(round((value - 0) / (100 - 0) * 100, 2))
        if text_to_draw.endswith('.0'):
            text_to_draw = text_to_draw[:-2]
        return text_to_draw
