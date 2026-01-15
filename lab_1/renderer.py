import math
from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QPoint, QSize, QRectF
from PySide6.QtGui import QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget
import numpy as np
import sympy as sp


class CoordinateSystem:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.viewport = QRect()

        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self._recalculate_pixels_for_xy()

        self.grid_step_x = 1
        self.grid_step_y = 1
        self.update_auto_steps()

    def _recalculate_pixels_for_xy(self):
        self.px_for_x = self.viewport.width() / (self.x_max - self.x_min)
        self.px_for_y = self.viewport.height() / (self.y_max - self.y_min)

    def _calculate_nice_grid_step(self, axis_range):
        if axis_range <= 0:
            return 0.1
        target_ticks = 20
        raw_step = axis_range / target_ticks
        magnitude = 10 ** math.floor(math.log10(raw_step))
        residual = raw_step / magnitude

        if residual < 1.2:
            step = 1.0 * magnitude
        elif residual < 2.5:
            step = 2.0 * magnitude
        elif residual < 6.0:
            step = 5.0 * magnitude
        else:
            step = 10.0 * magnitude
        return step

    def set_viewport(self, rect: QRect):
        self.viewport = rect
        self._recalculate_pixels_for_xy()

    def set_bounds(self, x_min_raw, x_max_raw, y_min_raw, y_max_raw):
        self.grid_step_x = self._calculate_nice_grid_step(x_max_raw - x_min_raw)
        self.grid_step_y = self._calculate_nice_grid_step(y_max_raw - y_min_raw)

        self.x_min = math.floor(x_min_raw / self.grid_step_x) * self.grid_step_x
        self.x_max = math.ceil(x_max_raw / self.grid_step_x) * self.grid_step_x

        self.y_min = math.floor(y_min_raw / self.grid_step_y) * self.grid_step_y
        self.y_max = math.ceil(y_max_raw / self.grid_step_y) * self.grid_step_y

        if self.y_min == self.y_max:
            self.y_min -= self.grid_step_y
            self.y_max += self.grid_step_y

        self._recalculate_pixels_for_xy()

    def math_to_pixels(self, point: QPointF) -> QPointF:
        x_px = self.viewport.left() + (point.x() - self.x_min) * self.px_for_x
        y_px = self.viewport.bottom() - (point.y() - self.y_min) * self.px_for_y
        return QPointF(x_px, y_px)

    def update_auto_steps(self):
        self.grid_step_x = self._calculate_nice_grid_step(self.x_max - self.x_min)
        self.grid_step_y = self._calculate_nice_grid_step(self.y_max - self.y_min)


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._cached_pixmap = QPixmap()
        self._coord_sys = CoordinateSystem(x_min=-10, x_max=10, y_min=-10, y_max=10)

        self.current_plots = []

    def resizeEvent(self, event):
        # Define plotting area inside pixmap
        margin_x = int(self.width() * 0.02)
        margin_y = int(self.height() * 0.02)
        plot_rect = self.contentsRect().adjusted(
            margin_x, margin_y, -margin_x, -margin_y
        )
        self._coord_sys.set_viewport(plot_rect)
        self._coord_sys.set_bounds(-10, 10, -10, 10)

        self._build_axis_grid()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPointF(0, 0), self._cached_pixmap)

    def clear(self):
        self.current_plots = []
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
        grid_dots_x = int(
            (self._coord_sys.x_max - self._coord_sys.x_min)
            / self._coord_sys.grid_step_x
        )
        for i in range(grid_dots_x + 1):
            current_x = self._coord_sys.x_min + i * self._coord_sys.grid_step_x

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
                - (self._coord_sys.px_for_x * self._coord_sys.grid_step_x) / 2,
                bot_point.y(),
                self._coord_sys.px_for_x * self._coord_sys.grid_step_x,
                self._coord_sys.px_for_y,
            )
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"{current_x:.2f}",
            )

        # Draw horizontal grid lines
        grid_dots_y = int(
            (self._coord_sys.y_max - self._coord_sys.y_min)
            / self._coord_sys.grid_step_y
        )
        for i in range(grid_dots_y + 1):
            current_y = self._coord_sys.y_min + i * self._coord_sys.grid_step_y

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
                - (self._coord_sys.grid_step_y * self._coord_sys.px_for_y) / 2,
                self._coord_sys.px_for_x,
                self._coord_sys.grid_step_y * self._coord_sys.px_for_y,
            )

            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                f"{current_y:.2f}",
            )

        # Zero lines
        zero_pen = QPen(Qt.black, 1.5, Qt.SolidLine)
        painter.setPen(zero_pen)
        if self._coord_sys.x_min <= 0 <= self._coord_sys.x_max:
            top_zero = self._coord_sys.math_to_pixels(QPointF(0, self._coord_sys.y_max))
            bot_zero = self._coord_sys.math_to_pixels(QPointF(0, self._coord_sys.y_min))
            painter.drawLine(top_zero, bot_zero)

        if self._coord_sys.y_min <= 0 <= self._coord_sys.y_max:
            left_zero = self._coord_sys.math_to_pixels(
                QPointF(self._coord_sys.x_min, 0)
            )
            right_zero = self._coord_sys.math_to_pixels(
                QPointF(self._coord_sys.x_max, 0)
            )
            painter.drawLine(left_zero, right_zero)

        # Release painter
        painter.end()

    def _draw_legend(self, painter: QPainter):
        if not self.current_plots:
            return

        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        padding = 10
        line_width = 30
        row_height = 25

        max_text_width = 0
        for plot in self.current_plots:
            width = painter.fontMetrics().horizontalAdvance(plot["name"])
            max_text_width = max(max_text_width, width)

        legend_width = max_text_width + line_width + padding * 3
        legend_height = len(self.current_plots) * row_height + padding

        rect = QRect(
            self._coord_sys.viewport.right() - legend_width - 10,
            self._coord_sys.viewport.top() + 10,
            legend_width,
            legend_height,
        )

        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QColor(255, 255, 255, 200))
        painter.drawRect(rect)

        for i, plot in enumerate(self.current_plots):
            y_pos = rect.top() + padding + i * row_height + row_height // 2

            painter.setPen(QPen(plot["color"], 2, plot["style"]))
            painter.drawLine(
                rect.left() + padding, y_pos, rect.left() + padding + line_width, y_pos
            )

            painter.setPen(Qt.black)
            painter.drawText(
                rect.left() + line_width + padding * 2, y_pos + 5, plot["name"]
            )

    def plot_func(
        self,
        func_name: str,
        left_x: float,
        right_x: float,
        points: int,
        color=Qt.red,
        style=Qt.SolidLine,
    ):
        x = sp.symbols("x")
        expr = sp.parse_expr(func_name)
        f_lambda = sp.lambdify(x, expr, "numpy")

        x_vals = np.linspace(left_x, right_x, points + 1)
        y_vals = f_lambda(x_vals)

        data_range_x = right_x - left_x
        data_range_y = y_vals.max() - y_vals.min()
        if data_range_y == 0:
            data_range_y = 1.0

        padding_x = data_range_x * 0
        padding_y = data_range_y * 0.005

        self._coord_sys.set_bounds(
            x_min_raw=left_x - padding_x,
            x_max_raw=right_x + padding_x,
            y_min_raw=y_vals.min() - padding_y,
            y_max_raw=y_vals.max() + padding_y,
        )

        self.current_plots.append({"name": func_name, "color": color, "style": style})

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

        self._draw_legend(painter)
        painter.end()
        self.update()
