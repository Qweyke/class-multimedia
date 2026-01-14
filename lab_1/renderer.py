import math
from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QPoint, QSize, QRectF
from PySide6.QtGui import QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget
import numpy as np


class CoordinateSystem:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.viewport = QRect()

        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self._recalculate_pixels_for_xy()

        self.grid_step = 1

    def _recalculate_pixels_for_xy(self):
        self.px_for_x = self.viewport.width() / (self.x_max - self.x_min)
        self.px_for_y = self.viewport.height() / (self.y_max - self.y_min)

    def set_viewport(self, rect: QRect):
        self.viewport = rect
        self._recalculate_pixels_for_xy()

    def set_bounds(self, x_min, x_max, y_min, y_max):
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self._recalculate_pixels_for_xy()

    def math_to_pixels(self, point: QPointF) -> QPointF:
        x_px = self.viewport.left() + (point.x() - self.x_min) * self.px_for_x
        y_px = self.viewport.bottom() - (point.y() - self.y_min) * self.px_for_y
        return QPointF(x_px, y_px)


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._cached_pixmap = QPixmap()
        self._coord_sys = CoordinateSystem(x_min=-10, x_max=10, y_min=-10, y_max=10)

    def resizeEvent(self, event):
        # Define plotting area inside pixmap
        margin_x = int(self.width() * 0.05)
        margin_y = int(self.height() * 0.05)
        plot_rect = self.contentsRect().adjusted(
            margin_x, margin_y, -margin_x, -margin_y
        )
        self._coord_sys.set_viewport(plot_rect)
        self._coord_sys.set_bounds(x_min=-10, x_max=10, y_min=-10, y_max=10)

        self._build_axis_grid()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPointF(0, 0), self._cached_pixmap)

    def clear(self):
        self.resizeEvent(None)

    def _build_axis_grid(self):
        # Initialize drawing cache, fill it in with mono-color
        self._cached_pixmap = QPixmap(self.width(), self.height())
        self._cached_pixmap.fill(QColor(255, 255, 255))

        # Setup painter
        painter = QPainter(self._cached_pixmap)
        painter.setViewport(self._coord_sys.viewport)

        # Init pens
        frame_pen = QPen(Qt.black, 1, Qt.SolidLine)
        axis_pen = QPen(Qt.gray, 1, Qt.DotLine)

        # Draw frame
        painter.setBrush(QColor(255, 255, 225))
        painter.setPen(frame_pen)
        painter.drawRect(self._coord_sys.viewport)

        # Draw vertical grid lines
        grid_dots_qnty = int(
            (self._coord_sys.x_max - self._coord_sys.x_min) / self._coord_sys.grid_step
        )
        print(grid_dots_qnty)
        for i in range(grid_dots_qnty + 1):
            current_x = self._coord_sys.x_min + i * self._coord_sys.grid_step

            bot_point = self._coord_sys.math_to_pixels(
                QPointF(current_x, self._coord_sys.y_min)
            )
            top_point = self._coord_sys.math_to_pixels(
                QPointF(current_x, self._coord_sys.y_max)
            )

            painter.setPen(axis_pen)
            painter.drawLine(bot_point, top_point)

            # Labels
            painter.setPen(frame_pen)
            label_rect = QRectF(
                bot_point.x()
                - (self._coord_sys.px_for_x * self._coord_sys.grid_step) / 2,
                bot_point.y(),
                self._coord_sys.px_for_x * self._coord_sys.grid_step,
                self._coord_sys.px_for_y,
            )
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"{current_x}",
            )

        # Draw horizontal grid lines
        grid_dots_qnty = int(
            (self._coord_sys.y_max - self._coord_sys.y_min) / self._coord_sys.grid_step
        )
        print(grid_dots_qnty)
        for i in range(grid_dots_qnty + 1):
            current_y = self._coord_sys.y_min + i * self._coord_sys.grid_step

            left_point = self._coord_sys.math_to_pixels(
                QPointF(self._coord_sys.x_min, current_y)
            )
            right_point = self._coord_sys.math_to_pixels(
                QPointF(self._coord_sys.x_max, current_y)
            )

            painter.setPen(axis_pen)
            painter.drawLine(left_point, right_point)

            painter.setPen(frame_pen)
            label_rect = QRectF(
                left_point.x() - self._coord_sys.px_for_x * 1.1,
                left_point.y()
                - (self._coord_sys.grid_step * self._coord_sys.px_for_y) / 2,
                self._coord_sys.px_for_x,
                self._coord_sys.grid_step * self._coord_sys.px_for_y,
            )

            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                f"{current_y:.2f}",
            )

        # Release painter
        painter.end()

    def plot_func(self, left_x: float, right_x: float, points: int, grid_step: float):
        print(f"Plotting {left_x} {right_x}")
        self._coord_sys.grid_step = grid_step

        x_vals = np.linspace(left_x, right_x, points + 1)
        y_vals = np.cos(x_vals)
        padding = self._coord_sys.grid_step

        self._coord_sys.set_bounds(
            x_min=left_x - padding,
            x_max=right_x + padding,
            y_min=y_vals.min() - padding,
            y_max=y_vals.max() + padding,
        )

        self._build_axis_grid()

        pixel_points = [
            self._coord_sys.math_to_pixels(QPointF(x, y))
            for x, y in zip(x_vals, y_vals)
        ]

        painter = QPainter(self._cached_pixmap)
        painter.setViewport(self._coord_sys.viewport)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))

        for i in range(len(pixel_points) - 1):
            painter.drawLine(pixel_points[i], pixel_points[i + 1])

        painter.end()
        self.update()
