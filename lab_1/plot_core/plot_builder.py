from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtGui import QPainter, Qt
from PySide6.QtCore import QPointF, QRectF
from PIL.ImageQt import QPixmap

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

    # def draw_naught_lines(self):
    #     # Zero lines
    #     zero_pen = QPen(Qt.black, 1.5, Qt.SolidLine)
    #     painter.setPen(zero_pen)
    #     if self._mapper.x_min <= 0 <= self._mapper.x_max:
    #         top_zero = self._mapper.math_to_pixels(QPointF(0, self._mapper.y_max))
    #         bot_zero = self._mapper.math_to_pixels(QPointF(0, self._mapper.y_min))
    #         painter.drawLine(top_zero, bot_zero)

    #     if self._mapper.y_min <= 0 <= self._mapper.y_max:
    #         left_zero = self._mapper.math_to_pixels(QPointF(self._mapper.x_min, 0))
    #         right_zero = self._mapper.math_to_pixels(QPointF(self._mapper.x_max, 0))
    #         painter.drawLine(left_zero, right_zero)

    #     # Release painter
    #     painter.end()

    # def draw_x_labels(self, x_values):
    #     self.painter.setPen(self.theme.label_pen)
    #     for x in x_values:
    #         point = self.mapper.math_to_pixels(QPointF(x, self.mapper.y_min))
    #         # Используем self.metrics для точного расчета
    #         label_h = self.metrics.height()
    #         rect = QRectF(point.x() - 25, point.y() + 5, 50, label_h)
    #         self.painter.drawText(rect, Qt.AlignCenter, f"{x:.2f}")
