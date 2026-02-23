from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QPixmap,
    QLinearGradient,
    QPolygonF,
    QFont,
)
from PySide6.QtWidgets import QWidget


from plot_core.function_resolver import FunctionResolver
from plot_core.plot_builder import PlotBuilder
from plot_core.coord_mapper import CoordinateMapper


class CanvasStyle:
    background_color = QColor("#FFFFFF")
    plot_area_color = QColor("#FAECC7")

    grid_pen = QPen(QColor("#C5BEBE"), 1, Qt.PenStyle.SolidLine)
    label_font_pen = QPen(QColor("#330505"), 1, Qt.PenStyle.DotLine)
    user_bounds_pen = QPen(QColor("#C5BEBE"), 2, Qt.PenStyle.DotLine)
    naught_axis_pen = QPen(QColor("#000000"), 1)

    label_font = QFont("Segoe UI", 9)


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Init and build default-scene
        self._cached_scene = QPixmap(self.width(), self.height())
        self._mapper = CoordinateMapper(x_min=-10, x_max=10, y_min=-10, y_max=10)

        self.current_plots = []

    def _rebuild_scene(self):
        PlotBuilder.draw_grid(
            mapper=self._mapper,
            scene=self._cached_scene,
            theme=CanvasStyle(),
        )
        PlotBuilder.draw_naught_lines_highlighting(
            mapper=self._mapper,
            scene=self._cached_scene,
            theme=CanvasStyle(),
        )

    def _get_plotting_rect(self):
        margin_x = int(self.width() * 0.02)
        margin_y = int(self.height() * 0.02)
        plot_rect = self.contentsRect().adjusted(
            margin_x, margin_y, -margin_x, -margin_y
        )
        return plot_rect

    def resizeEvent(self, event):
        self._cached_scene = QPixmap(self.width(), self.height())
        self._cached_scene.fill(CanvasStyle.background_color)
        self._mapper.remap(new_rect=self._get_plotting_rect(), theme=CanvasStyle)

        self._rebuild_scene()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPointF(0, 0), self._cached_scene)

    def clear(self):
        self.current_plots = []

        self._cached_scene = QPixmap(self.width(), self.height())
        self._cached_scene.fill(CanvasStyle.background_color)
        self._mapper.remap(
            theme=CanvasStyle(),
            new_x_min=-10,
            new_x_max=10,
            new_y_min=-10,
            new_y_max=10,
        )

        self._rebuild_scene()
        self.update()

    def plot_functions(self, func_items):
        pass

        self.update()

    def plot_function(
        self,
        func_name,
        left_x,
        right_x,
        points,
        color,
        use_cones,
    ):
        # Remap with new x-bounds, which will calculate extended bounds
        self._mapper.remap(
            theme=CanvasStyle(),
            new_x_min=left_x,
            new_x_max=right_x,
        )

        # Calculate values with extended bounds
        y_min, y_max, x_vals, y_vals = FunctionResolver.get_prepared_values(
            left_x=self._mapper.x_min,
            right_x=self._mapper.x_max,
            function_symbolic=func_name,
            points_qnty=points,
        )

        # Remap with calculated y-bounds
        self._mapper.remap(
            theme=CanvasStyle,
            new_y_min=y_min,
            new_y_max=y_max,
        )

        # 4. REBUILD AND DRAW
        self._cached_scene = QPixmap(self.width(), self.height())
        self._cached_scene.fill(CanvasStyle.background_color)
        self._rebuild_scene()  # Draws the grid lines based on beauty bounds

        PlotBuilder.draw_user_bounds(
            theme=CanvasStyle(),
            mapper=self._mapper,
            scene=self._cached_scene,
            left_bound=left_x,
            right_bound=right_x,
            bot_bound=self._mapper.y_min,
            top_bound=self._mapper.y_max,
        )

        PlotBuilder.draw_function(
            x_vals=x_vals,
            y_vals=y_vals,
            mapper=self._mapper,
            scene=self._cached_scene,
            color=color,
            use_cones=use_cones,
        )

        self.update()

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
