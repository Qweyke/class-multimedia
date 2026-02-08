from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtGui import QPainter, Qt, QPen
from PySide6.QtCore import QPointF, QRectF
from PIL.ImageQt import QPixmap

if TYPE_CHECKING:
    from plot_core.coord_mapper import CoordinateMapper
    from plot_core.renderer import CanvasStyle


class PlotBuilder:
    @staticmethod
    def draw_grid(scene: QPixmap, mapper: CoordinateMapper, theme: CanvasStyle):
        # Setup painter
        painter = QPainter(scene)
        painter.setPen(theme.grid_pen)
        painter.setViewport(mapper.viewport)

        # Draw frame
        painter.setBrush(theme.plot_area_color)
        painter.drawRect(mapper.viewport)
        font_metrics = painter.fontMetrics()

        # Draw vertical grid lines
        # left_line_x = math.ceil(mapper.x_min / mapper.x_step) * mapper.x_step
        # right_line_x = math.floor(mapper.x_max / mapper.x_step) * mapper.x_step

        left_line_x = mapper.x_min
        right_line_x = mapper.x_max
        while left_line_x <= right_line_x + (mapper.x_step / 2):
            bot_point = mapper.math_to_pixels(QPointF(left_line_x, mapper.y_min))
            top_point = mapper.math_to_pixels(QPointF(left_line_x, mapper.y_max))

            painter.setPen(theme.grid_pen)
            painter.drawLine(bot_point, top_point)

            # Label for x-lines
            label_text = f"{left_line_x:.5g}"
            text_width = font_metrics.horizontalAdvance(label_text)
            label_text_rect = QRectF(
                bot_point.x() - (text_width / 2),
                bot_point.y(),
                text_width,
                font_metrics.height(),
            )

            painter.setPen(theme.label_font_pen)
            painter.drawText(
                label_text_rect,
                Qt.AlignmentFlag.AlignHCenter,
                label_text,
            )

            left_line_x += mapper.x_step

        # Draw horizontal grid lines
        # bottom_line_y = math.ceil(mapper.y_min / mapper.y_step) * mapper.y_step
        # top_line_y = math.floor(mapper.y_max / mapper.y_step) * mapper.y_step

        bottom_line_y = mapper.y_min
        top_line_y = mapper.y_max
        while bottom_line_y <= top_line_y + (mapper.y_step / 2):
            left_point = mapper.math_to_pixels(QPointF(mapper.x_min, bottom_line_y))
            right_point = mapper.math_to_pixels(QPointF(mapper.x_max, bottom_line_y))
            painter.setPen(theme.grid_pen)
            painter.drawLine(left_point, right_point)

            bottom_line_y += mapper.y_step

        # Release painter
        painter.end()

    # @staticmethod
    # def draw_axis_labels(scene: QPixmap, mapper: CoordinateMapper, theme: CanvasStyle):
    #     # Setup painter
    #     painter = QPainter(scene)
    #     painter.setPen(theme.label_font_pen)
    #     painter.setViewport(mapper.viewport)

    #     metrics = painter.fontMetrics()
    #     label_text = f"{current_x:.2f}"

    #     # Labels
    #     label_rect = QRectF(
    #         bot_point.x() - (mapper.px_for_x * mapper.x_step) / 2,
    #         bot_point.y(),
    #         mapper.px_for_x * mapper.x_step,
    #         mapper.px_for_y,
    #     )
    #     print(f"X label box size: {label_rect.size()}")
    #     painter.drawText(
    #         label_rect,
    #         Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
    #         f"{current_x:.2f}",
    #     )

    #     label_rect = QRectF(
    #         left_point.x() - mapper.px_for_x * 1.1,
    #         left_point.y() - (mapper.y_step * mapper.px_for_y) / 2,
    #         mapper.px_for_x,
    #         mapper.y_step * mapper.px_for_y,
    #     )

    #     print(f"Y label box size: {label_rect.size()}")
    #     painter.drawText(
    #         label_rect,
    #         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
    #         f"{current_y:.2f}",
    #     )

    @staticmethod
    def draw_naught_lines_highlighting(
        scene: QPixmap, mapper: CoordinateMapper, theme: CanvasStyle
    ):
        painter = QPainter(scene)
        painter.setPen(theme.naught_axis_pen)
        painter.setViewport(mapper.viewport)

        if mapper.x_min <= 0 <= mapper.x_max:
            top_zero = mapper.math_to_pixels(QPointF(0, mapper.y_max))
            bot_zero = mapper.math_to_pixels(QPointF(0, mapper.y_min))
            painter.drawLine(top_zero, bot_zero)

        if mapper.y_min <= 0 <= mapper.y_max:
            left_zero = mapper.math_to_pixels(QPointF(mapper.x_min, 0))
            right_zero = mapper.math_to_pixels(QPointF(mapper.x_max, 0))
            painter.drawLine(left_zero, right_zero)

        # Release painter
        painter.end()

    @staticmethod
    def draw_function(
        scene: QPixmap,
        mapper: CoordinateMapper,
        color,
        x_vals,
        y_vals,
        use_cones=False,
    ):
        try:
            # Prepare for plotting
            painter = QPainter(scene)
            painter.setViewport(mapper.viewport)
            painter.setRenderHint(QPainter.Antialiasing)

            # Cut outside-values
            painter.setClipRect(mapper.viewport)

            # Plotting cycle
            if use_cones:
                # self._draw_pseudo_cones(painter, x_vals, y_vals, color)
                pass
            else:
                painter.setPen(QPen(color, 2))
                last_point = None

                for i in range(len(x_vals)):
                    curr_point = mapper.math_to_pixels(QPointF(x_vals[i], y_vals[i]))

                    if last_point is not None:
                        painter.drawLine(last_point, curr_point)

                    last_point = curr_point

            # Release and paint
            painter.end()

        except Exception as e:
            print(f"Plot error: {e}")
