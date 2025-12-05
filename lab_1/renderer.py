from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QPoint, QSize
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QBrush, QPolygon, QTransform
from PySide6.QtWidgets import QWidget


from log.custom_logger import logger


class Renderer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._cached_pixmap = None
        self._view_port = None
        self._logical_window = None

    def resizeEvent(self, event):
        self._recalculate_painter_areas()
        self._build_axis_grid()
        self.update()

    def paintEvent(self, event):
        if self._cached_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(QPointF(0, 0), self._cached_pixmap)

    def _recalculate_painter_areas(self, x_min=-10, y_min=0, x_max=10, y_max=10):
        # Initialize drawing cache
        self._cached_pixmap = QPixmap(self.width(), self.height())

        # Define plotting area in rectangle
        x_margin = int(self.width() * 0.05)
        y_margin = int(self.height() * 0.01)
        rect_start_point = QPoint(x_margin, y_margin)
        rect_size = QSize((self.width() - 2 * x_margin), (self.height() - 2 * y_margin))
        self._view_port = QRect(rect_start_point, rect_size)

        # Set logical coordinates
        coord_start_point = QPoint(x_min, y_max)

        coord_size = QSize(
            x_max - x_min, -(y_max - y_min)
        )  # <<! invert y coord by minus before height
        self._logical_window = QRect(coord_start_point, coord_size)

    def _create_adjusted_painter(self):
        adj_painter = QPainter(self._cached_pixmap)
        adj_painter.setViewport(self._view_port)
        adj_painter.setWindow(self._logical_window)
        return adj_painter

    def _build_axis_grid(self, x_min=-10, y_min=0, x_max=10, y_max=10, dots_qnty=10):
        # Clean pixmap
        self._cached_pixmap.fill(QColor(255, 255, 225))

        painter = self._create_adjusted_painter()

        # Draw plotting frame
        painter.setPen(QPen(Qt.black, 0.05, Qt.SolidLine))
        painter.drawRect(self._logical_window)

        # Draw grid lines
        painter.setPen(QPen(Qt.black, 0, Qt.DotLine))
        step_x = (x_max - x_min) / dots_qnty
        print(step_x)
        step_y = step_x

        # Vertical
        x = x_min + step_x
        while x < x_max:
            painter.drawLine(QPointF(x, y_min), QPointF(x, y_max))
            x += step_x

        # Horizontal
        y = y_min + step_y
        while y < y_max:
            painter.drawLine(QPointF(x_min, y), QPointF(x_max, y))
            y += step_y

        painter.end()

    def _test(self):
        painter = self._create_adjusted_painter()
        # Test
        painter.setPen(QPen(Qt.red, 0, Qt.SolidLine))
        painter.drawRect(QRect(QPoint(0, 0), QSize(10, 5)))
        painter.drawLine(QPoint(0, 0), QPoint(5, 10))
