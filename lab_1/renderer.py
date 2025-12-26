from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QPoint, QSize, QRectF
from PySide6.QtGui import QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._cached_pixmap = QPixmap()
        self._plot_area = QRect()

        self._px_per_x_unit = 1
        self._px_per_y_unit = 1

        self._x_min = -10
        self._y_min = -5
        self._x_max = 10
        self._y_max = 5
        self._dots_qnty = 20

    def resizeEvent(self, event):
        self._build_axis_grid()
        self.update()

    def paintEvent(self, event):
        if self._cached_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(QPointF(0, 0), self._cached_pixmap)

    def _math_point_to_pixels(self, point: QPointF):
        px = self._plot_area.left() + (point.x() - self._x_min) * self._px_per_x_unit
        py = self._plot_area.bottom() - (point.y() - self._y_min) * self._px_per_y_unit

        return QPointF(px, py)

    def _build_axis_grid(self):
        # Initialize drawing cache, fill it in with mono-color
        self._cached_pixmap = QPixmap(self.width(), self.height())
        self._cached_pixmap.fill(QColor(255, 255, 255))

        # Define plotting area inside pixmap
        x_margin = int(self.width() * 0.05)
        y_margin = int(self.height() * 0.05)
        rect_start_point = QPoint(x_margin, y_margin)
        rect_size = QSize((self.width() - 2 * x_margin), (self.height() - 2 * y_margin))
        self._plot_area = QRect(rect_start_point, rect_size)

        # Calculate x, y units sizes in pixels
        self._px_per_x_unit = self._plot_area.width() / (self._x_max - self._x_min)
        self._px_per_y_unit = self._plot_area.height() / (self._y_max - self._y_min)

        # Setup painter
        painter = QPainter(self._cached_pixmap)
        painter.setViewport(self._plot_area)

        # Init pens
        frame_pen = QPen(Qt.black, 1, Qt.SolidLine)
        axis_pen = QPen(Qt.gray, 1, Qt.DotLine)

        # Draw frame
        painter.setBrush(QColor(255, 255, 225))
        painter.setPen(frame_pen)
        painter.drawRect(self._plot_area)

        # Draw vertical grid lines
        step_x = (self._x_max - self._x_min) / self._dots_qnty
        for i in range(self._dots_qnty + 1):
            current_x = self._x_min + i * step_x

            bot_point = self._math_point_to_pixels(QPointF(current_x, self._y_min))
            top_point = self._math_point_to_pixels(QPointF(current_x, self._y_max))

            painter.setPen(axis_pen)
            painter.drawLine(bot_point, top_point)

            # Labels
            painter.setPen(frame_pen)
            label_rect = QRectF(
                bot_point.x() - (self._px_per_x_unit * step_x) / 2,
                bot_point.y(),
                self._px_per_x_unit * step_x,
                self._px_per_y_unit,
            )
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"{current_x}",
            )

        # Draw horizontal grid lines
        step_y = (self._y_max - self._y_min) / self._dots_qnty
        for i in range(self._dots_qnty + 1):
            current_y = self._y_min + i * step_y

            left_point = self._math_point_to_pixels(QPointF(self._x_min, current_y))
            right_point = self._math_point_to_pixels(QPointF(self._x_max, current_y))

            painter.setPen(axis_pen)
            painter.drawLine(left_point, right_point)

            painter.setPen(frame_pen)
            label_rect = QRectF(
                left_point.x() - self._px_per_x_unit * 1.1,
                left_point.y() - (step_y * self._px_per_y_unit) / 2,
                self._px_per_x_unit,
                step_y * self._px_per_y_unit,
            )

            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                f"{current_y}",
            )

        # Release painter
        painter.end()

    def plot_func(self):
        painter = QPainter(self._cached_pixmap)
        painter.setViewport(self._plot_area)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        first = self._math_point_to_pixels(QPointF(0, 2))
        second = self._math_point_to_pixels(QPointF(5, 2))

        center = self._math_point_to_pixels(QPointF(0, 0))

        print(f"First: {first}, second: {second}")

        painter.drawLine(first, second)

        painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
        painter.drawPoint(center)

        painter.end()
        self.update()
