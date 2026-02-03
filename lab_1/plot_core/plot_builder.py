from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtGui import QPainter, Qt
from PySide6.QtCore import QPointF, QRectF
from PIL.ImageQt import QPixmap

import numpy as np
import sympy as sp

if TYPE_CHECKING:
    from plot_core.coord_mapper import CoordinateMapper
    from plot_core.renderer import CanvasStyle


class PlotBuilder:
    def __init__(
        self,
        mapper: CoordinateMapper = None,
        theme: CanvasStyle = None,
        scene: QPixmap = None,
    ):
        self._theme = theme
        self._mapper = mapper
        self._scene = scene

    def draw_grid(self):
        # Setup painter
        painter = QPainter(self._scene)
        painter.setPen(self._theme.grid_pen)
        painter.setViewport(self._mapper.viewport)

        # Draw frame
        painter.setBrush(self._theme.plot_area_color)
        painter.setPen(self._theme.grid_pen)
        painter.drawRect(self._mapper.viewport)

        # Draw vertical grid lines
        grid_dots_x = int(
            (self._mapper.x_max - self._mapper.x_min) / self._mapper.x_step
        )
        for i in range(grid_dots_x + 1):
            current_x = self._mapper.x_min + i * self._mapper.x_step

            bot_point = self._mapper.math_to_pixels(
                QPointF(current_x, self._mapper.y_min)
            )
            top_point = self._mapper.math_to_pixels(
                QPointF(current_x, self._mapper.y_max)
            )
            painter.drawLine(bot_point, top_point)

            # Labels
            painter.setPen(self._theme.label_font_pen)
            label_rect = QRectF(
                bot_point.x() - (self._mapper.px_for_x * self._mapper.x_step) / 2,
                bot_point.y(),
                self._mapper.px_for_x * self._mapper.x_step,
                self._mapper.px_for_y,
            )
            print(f"X label box size: {label_rect.size()}")
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"{current_x:.2f}",
            )

        # Draw horizontal grid lines
        grid_dots_y = int(
            (self._mapper.y_max - self._mapper.y_min) / self._mapper.y_step
        )
        for i in range(grid_dots_y + 1):
            current_y = self._mapper.y_min + i * self._mapper.y_step

            left_point = self._mapper.math_to_pixels(
                QPointF(self._mapper.x_min, current_y)
            )
            right_point = self._mapper.math_to_pixels(
                QPointF(self._mapper.x_max, current_y)
            )
            painter.drawLine(left_point, right_point)

            painter.setPen(self._theme.label_font_pen)
            label_rect = QRectF(
                left_point.x() - self._mapper.px_for_x * 1.1,
                left_point.y() - (self._mapper.y_step * self._mapper.px_for_y) / 2,
                self._mapper.px_for_x,
                self._mapper.y_step * self._mapper.px_for_y,
            )

            print(f"Y label box size: {label_rect.size()}")
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                f"{current_y:.2f}",
            )

        # Release painter
        painter.end()

    def draw_naught_lines_highlighting(self):
        painter = QPainter(self._scene)
        painter.setPen(self._theme.naught_axis_pen)
        painter.setViewport(self._mapper.viewport)

        if self._mapper.x_min <= 0 <= self._mapper.x_max:
            top_zero = self._mapper.math_to_pixels(QPointF(0, self._mapper.y_max))
            bot_zero = self._mapper.math_to_pixels(QPointF(0, self._mapper.y_min))
            painter.drawLine(top_zero, bot_zero)

        if self._mapper.y_min <= 0 <= self._mapper.y_max:
            left_zero = self._mapper.math_to_pixels(QPointF(self._mapper.x_min, 0))
            right_zero = self._mapper.math_to_pixels(QPointF(self._mapper.x_max, 0))
            painter.drawLine(left_zero, right_zero)

        # Release painter
        painter.end()

    def draw_x_labels(self, x_values):
        self.painter.setPen(self.theme.label_pen)
        for x in x_values:
            point = self.mapper.math_to_pixels(QPointF(x, self.mapper.y_min))
            # Используем self.metrics для точного расчета
            label_h = self.metrics.height()
            rect = QRectF(point.x() - 25, point.y() + 5, 50, label_h)
            self.painter.drawText(rect, Qt.AlignCenter, f"{x:.2f}")

    def parse_math_function(
        func_name: str, left_x: float, right_x: float, points_qnty: int
    ):
        x = sp.symbols("x")
        expr = sp.parse_expr(func_name.replace("^", "**"))
        lambdified_func = sp.lambdify(x, expr, "numpy")

        # Resolve breaking-vals
        with np.errstate(divide="ignore", invalid="ignore"):
            x_vals = np.linspace(left_x, right_x, points_qnty)
            y_vals: np.array = lambdified_func(x_vals)

        finite_mask = np.isfinite(y_vals)
        finite_y = y_vals[finite_mask]

        if finite_y.size == 0:
            return

        # Determine left-right sides
        y_min_data = finite_y.min()
        y_max_data = finite_y.max()

        # Trim asymptotes
        y_range = y_max_data - y_min_data
        if y_range > 1000:
            y_min_data = max(y_min_data, -500)
            y_max_data = min(y_max_data, 500)

    def plot_func(
        self,
        color,
        style=Qt.SolidLine,
        use_cones=True,
    ):
        try:
            # Parse function
            x = sp.symbols("x")
            expr = sp.parse_expr(func_name.replace("^", "**"))
            f_lambda = sp.lambdify(x, expr, "numpy")

            # Resolve breaking-vals
            with np.errstate(divide="ignore", invalid="ignore"):
                x_vals = np.linspace(left_x, right_x, points + 1)
                y_raw = f_lambda(x_vals)
                y_vals = np.array(y_raw, dtype=float)

            finite_mask = np.isfinite(y_vals)
            finite_y = y_vals[finite_mask]

            if finite_y.size == 0:
                return

            # Determine left-right sides
            y_min_data = finite_y.min()
            y_max_data = finite_y.max()

            # Trim asymptotes
            y_range = y_max_data - y_min_data
            if y_range > 1000:
                y_min_data = max(y_min_data, -500)
                y_max_data = min(y_max_data, 500)

            # Set trimmed bounds
            self._coord_sys.set_bounds(
                x_min_raw=left_x,
                x_max_raw=right_x,
                y_min_raw=y_min_data,
                y_max_raw=y_max_data,
            )

            # Build adjusted grid
            self._build_axis_grid()

            # Prepare for plotting
            painter = QPainter(self._cached_pixmap)
            painter.setViewport(self._coord_sys.viewport)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setClipRect(self._coord_sys.viewport)

            # Plotting cycle
            if use_cones:
                self._draw_pseudo_cones(painter, x_vals, y_vals, color)
            else:
                painter.setPen(QPen(color, 2, style))
                last_point = None

                for i in range(len(x_vals)):
                    if finite_mask[i]:
                        curr_point = self._coord_sys.math_to_pixels(
                            QPointF(x_vals[i], y_vals[i])
                        )
                        if last_point is not None:
                            if (
                                abs(y_vals[i] - y_vals[i - 1])
                                < (y_max_data - y_min_data) * 2
                            ):
                                painter.drawLine(last_point, curr_point)
                        last_point = curr_point
                    else:
                        last_point = None

            # Draw legend
            self.current_plots.append(
                {"name": func_name, "color": color, "style": style}
            )
            self._draw_legend(painter)

            # Release and paint
            painter.end()
            self.update()

        except Exception as e:
            print(f"Plot error: {e}")
