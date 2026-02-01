from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF, QRectF
from PIL.ImageQt import QPixmap
from coord_mapper import CoordinateMapper
from renderer import CanvasStyle


class ScenePlotter:
    def __init__(self, mapper: CoordinateMapper, theme: CanvasStyle, scene: QPixmap):
        self.theme = theme
        self.mapper = mapper
        self.scene = scene

    def draw_grid(self):
        # Setup painter
        painter = QPainter(self.scene)
        painter.setPen(self.theme.grid_pen)
        painter.setViewport(self.mapper.viewport)

        # Draw frame
        painter.setBrush(self.theme.plot_area_color)
        painter.setPen(self.theme.grid_pen)
        painter.drawRect(self.mapper.viewport)

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
                left=bot_point.x()
                - (self._coord_sys.px_for_x * self._coord_sys.grid_step_x) / 2,
                top=bot_point.y(),
                width=self._coord_sys.px_for_x * self._coord_sys.grid_step_x,
                heitgh=self._coord_sys.px_for_y,
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
        # Release painter
        painter.end()

    def draw_naught_lines(self):
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

    def draw_x_labels(self, x_values):
        self.painter.setPen(self.theme.label_pen)
        for x in x_values:
            point = self.mapper.math_to_pixels(QPointF(x, self.mapper.y_min))
            # Используем self.metrics для точного расчета
            label_h = self.metrics.height()
            rect = QRectF(point.x() - 25, point.y() + 5, 50, label_h)
            self.painter.drawText(rect, Qt.AlignCenter, f"{x:.2f}")
