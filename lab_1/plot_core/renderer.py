import math
from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QLinearGradient, QPolygonF, QFont
from PySide6.QtWidgets import QWidget
import numpy as np
import sympy as sp

from plot_core.plot_builder import PlotBuilder
from plot_core.coord_mapper import CoordinateMapper


class CanvasStyle:
    background_color = QColor("#FFFFFF")
    plot_area_color = QColor("#FAECC7")

    grid_pen = QPen(QColor("#000000"), 1, Qt.DotLine)
    label_font_pen = QPen(QColor("#4D0505"), 1, Qt.DotLine)
    naught_axis_pen = QPen(QColor("#000000"), 1)

    label_font = QFont("Segoe UI", 9)


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Init and build default-scene
        self._cached_scene = QPixmap()
        self._builder = PlotBuilder()
        self._rebuild_scene()

        self.current_plots = []

    def _rebuild_scene(self):
        self._cached_scene = QPixmap(self.width(), self.height())
        self._cached_scene.fill(CanvasStyle.background_color)

        margin_x = int(self.width() * 0.02)
        margin_y = int(self.height() * 0.02)
        plot_rect = self.contentsRect().adjusted(
            margin_x, margin_y, -margin_x, -margin_y
        )

        self._builder = PlotBuilder(
            mapper=CoordinateMapper(
                rect=plot_rect, x_min=-10, x_max=10, y_min=-10, y_max=10
            ),
            scene=self._cached_scene,
            theme=CanvasStyle,
        )

        self._builder.draw_grid()
        self._builder.draw_naught_lines_highlighting()

    def resizeEvent(self, event):
        self._rebuild_scene()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPointF(0, 0), self._cached_scene)

    def clear(self):
        self.current_plots = []
        self.resizeEvent(None)

    # def _draw_legend(self, painter: QPainter):
    #     if not self.current_plots:
    #         return

    #     font = painter.font()
    #     font.setPointSize(10)
    #     painter.setFont(font)

    #     padding = 10
    #     line_width = 30
    #     row_height = 25

    #     max_text_width = 0
    #     for plot in self.current_plots:
    #         width = painter.fontMetrics().horizontalAdvance(plot["name"])
    #         max_text_width = max(max_text_width, width)

    #     legend_width = max_text_width + line_width + padding * 3
    #     legend_height = len(self.current_plots) * row_height + padding

    #     rect = QRect(
    #         self._coord_sys.viewport.right() - legend_width - 10,
    #         self._coord_sys.viewport.top() + 10,
    #         legend_width,
    #         legend_height,
    #     )

    #     painter.setPen(QPen(Qt.black, 1))
    #     painter.setBrush(QColor(255, 255, 255, 200))
    #     painter.drawRect(rect)

    #     for i, plot in enumerate(self.current_plots):
    #         y_pos = rect.top() + padding + i * row_height + row_height // 2

    #         painter.setPen(QPen(plot["color"], 2, plot["style"]))
    #         painter.drawLine(
    #             rect.left() + padding, y_pos, rect.left() + padding + line_width, y_pos
    #         )

    #         painter.setPen(Qt.black)
    #         painter.drawText(
    #             rect.left() + line_width + padding * 2, y_pos + 5, plot["name"]
    #         )

    # def _draw_pseudo_cones(self, painter: QPainter, x_vals, y_vals, base_color):
    #     if len(x_vals) < 2:
    #         return

    #     # Calculate cone width
    #     p1 = self._coord_sys.math_to_pixels(QPointF(x_vals[0], 0))
    #     p2 = self._coord_sys.math_to_pixels(QPointF(x_vals[1], 0))
    #     cone_width = abs(p2.x() - p1.x()) * 0.8

    #     y_zero_px = self._coord_sys.math_to_pixels(QPointF(0, 0)).y()

    #     for x, y in zip(x_vals, y_vals):
    #         if not np.isfinite(y) or abs(y) < 1e-6:
    #             continue

    #         # Calculate peaks
    #         tip_px = self._coord_sys.math_to_pixels(QPointF(x, y))
    #         base_center_px = self._coord_sys.math_to_pixels(QPointF(x, 0))

    #         left_x = base_center_px.x() - cone_width / 2
    #         right_x = base_center_px.x() + cone_width / 2

    #         # Gradient
    #         grad = QLinearGradient(left_x, 0, right_x, 0)
    #         grad.setColorAt(0.0, base_color.lighter(150))
    #         grad.setColorAt(0.3, base_color)
    #         grad.setColorAt(1.0, base_color.darker(150))
    #         painter.setPen(Qt.NoPen)
    #         painter.setBrush(grad)

    #         # Cone's body
    #         cone_poly = QPolygonF(
    #             [
    #                 tip_px,  # Top peak
    #                 QPointF(left_x, y_zero_px),  # Left angle
    #                 QPointF(right_x, y_zero_px),  # Right angle
    #             ]
    #         )
    #         painter.drawPolygon(cone_poly)

    #         # Draw base with darker color
    #         ellipse_h = cone_width * 0.3
    #         ellipse_rect = QRectF(
    #             left_x, y_zero_px - ellipse_h / 2, cone_width, ellipse_h
    #         )
    #         painter.setBrush(base_color.darker(180))
    #         painter.drawEllipse(ellipse_rect)

    # def plot_func(
    #     self,
    #     func_name: str,
    #     left_x: float,
    #     right_x: float,
    #     points: int,
    #     color,
    #     style=Qt.SolidLine,
    #     use_cones=True,
    # ):
    #     self.clear()

    #     try:
    #         # Parse function
    #         x = sp.symbols("x")
    #         expr = sp.parse_expr(func_name.replace("^", "**"))
    #         f_lambda = sp.lambdify(x, expr, "numpy")

    #         # Resolve breaking-vals
    #         with np.errstate(divide="ignore", invalid="ignore"):
    #             x_vals = np.linspace(left_x, right_x, points + 1)
    #             y_raw = f_lambda(x_vals)
    #             y_vals = np.array(y_raw, dtype=float)

    #         finite_mask = np.isfinite(y_vals)
    #         finite_y = y_vals[finite_mask]

    #         if finite_y.size == 0:
    #             return

    #         # Determine left-right sides
    #         y_min_data = finite_y.min()
    #         y_max_data = finite_y.max()

    #         # Trim asymptotes
    #         y_range = y_max_data - y_min_data
    #         if y_range > 1000:
    #             y_min_data = max(y_min_data, -500)
    #             y_max_data = min(y_max_data, 500)

    #         # Set trimmed bounds
    #         self._coord_sys.set_bounds(
    #             x_min_raw=left_x,
    #             x_max_raw=right_x,
    #             y_min_raw=y_min_data,
    #             y_max_raw=y_max_data,
    #         )

    #         # Build adjusted grid
    #         self._build_axis_grid()

    #         # Prepare for plotting
    #         painter = QPainter(self._cached_pixmap)
    #         painter.setViewport(self._coord_sys.viewport)
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         painter.setClipRect(self._coord_sys.viewport)

    #         # Plotting cycle
    #         if use_cones:
    #             self._draw_pseudo_cones(painter, x_vals, y_vals, color)
    #         else:
    #             painter.setPen(QPen(color, 2, style))
    #             last_point = None

    #             for i in range(len(x_vals)):
    #                 if finite_mask[i]:
    #                     curr_point = self._coord_sys.math_to_pixels(
    #                         QPointF(x_vals[i], y_vals[i])
    #                     )
    #                     if last_point is not None:
    #                         if (
    #                             abs(y_vals[i] - y_vals[i - 1])
    #                             < (y_max_data - y_min_data) * 2
    #                         ):
    #                             painter.drawLine(last_point, curr_point)
    #                     last_point = curr_point
    #                 else:
    #                     last_point = None

    #         # Draw legend
    #         self.current_plots.append(
    #             {"name": func_name, "color": color, "style": style}
    #         )
    #         self._draw_legend(painter)

    #         # Release and paint
    #         painter.end()
    #         self.update()

    #     except Exception as e:
    #         print(f"Plot error: {e}")
