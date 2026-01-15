import math
from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QLinearGradient, QPolygonF
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

        margin_y = self.grid_step_y * 0.05
        self.y_min = (
            math.floor((y_min_raw - margin_y) / self.grid_step_y) * self.grid_step_y
        )
        self.y_max = (
            math.ceil((y_max_raw + margin_y) / self.grid_step_y) * self.grid_step_y
        )

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

    def _draw_pseudo_cones(self, painter: QPainter, x_vals, y_vals, base_color):
        if len(x_vals) < 2:
            return

        # Calculate cone width
        p1 = self._coord_sys.math_to_pixels(QPointF(x_vals[0], 0))
        p2 = self._coord_sys.math_to_pixels(QPointF(x_vals[1], 0))
        cone_width = abs(p2.x() - p1.x()) * 0.8

        y_zero_px = self._coord_sys.math_to_pixels(QPointF(0, 0)).y()

        for x, y in zip(x_vals, y_vals):
            if not np.isfinite(y) or abs(y) < 1e-6:
                continue

            # Calculate peaks
            tip_px = self._coord_sys.math_to_pixels(QPointF(x, y))
            base_center_px = self._coord_sys.math_to_pixels(QPointF(x, 0))

            left_x = base_center_px.x() - cone_width / 2
            right_x = base_center_px.x() + cone_width / 2

            # Gradient
            grad = QLinearGradient(left_x, 0, right_x, 0)
            grad.setColorAt(0.0, base_color.lighter(150))
            grad.setColorAt(0.3, base_color)
            grad.setColorAt(1.0, base_color.darker(150))
            painter.setPen(Qt.NoPen)
            painter.setBrush(grad)

            # Cone's body
            cone_poly = QPolygonF(
                [
                    tip_px,  # Top peak
                    QPointF(left_x, y_zero_px),  # Left angle
                    QPointF(right_x, y_zero_px),  # Right angle
                ]
            )
            painter.drawPolygon(cone_poly)

            # Draw base with darker color
            ellipse_h = cone_width * 0.3
            ellipse_rect = QRectF(
                left_x, y_zero_px - ellipse_h / 2, cone_width, ellipse_h
            )
            painter.setBrush(base_color.darker(180))
            painter.drawEllipse(ellipse_rect)

    def plot_func_1(
        self,
        func_name: str,
        left_x: float,
        right_x: float,
        points: int,
        color,
        style=Qt.SolidLine,
        use_cones=True,
    ):
        # Clear previous
        self.clear()

        # Parse function
        x = sp.symbols("x")
        expr = sp.parse_expr(func_name)
        f_lambda = sp.lambdify(x, expr, "numpy")

        x_vals = np.linspace(left_x, right_x, points + 1)
        y_vals = np.array(f_lambda(x_vals), dtype=float)
        finite_y = y_vals[np.isfinite(y_vals)]

        if finite_y.size == 0:
            return

        y_min_data = finite_y.min()
        y_max_data = finite_y.max()

        self._coord_sys.set_bounds(
            x_min_raw=left_x,
            x_max_raw=right_x,
            y_min_raw=y_min_data,
            y_max_raw=y_max_data,
        )

        self._build_axis_grid()

        # Start drawing
        painter = QPainter(self._cached_pixmap)
        painter.setViewport(self._coord_sys.viewport)
        painter.setClipRect(self._coord_sys.viewport)
        painter.setRenderHint(QPainter.Antialiasing)

        if use_cones:
            self._draw_pseudo_cones(painter, x_vals, y_vals, color)

        else:
            painter.setPen(QPen(color, 2))
            pixel_points = [
                self._coord_sys.math_to_pixels(QPointF(x, y))
                for x, y in zip(x_vals, y_vals)
            ]
            for i in range(len(pixel_points) - 1):
                painter.drawLine(pixel_points[i], pixel_points[i + 1])

            pixel_points = [
                self._coord_sys.math_to_pixels(QPointF(x, y))
                for x, y in zip(x_vals, y_vals)
            ]

        # Draw legend
        self.current_plots.append({"name": func_name, "color": color, "style": style})
        self._draw_legend(painter)

        painter.end()
        self.update()

    def plot_func(
        self,
        func_name: str,
        left_x: float,
        right_x: float,
        points: int,
        color,
        style=Qt.SolidLine,
        use_cones=True,
    ):
        self.clear()

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
