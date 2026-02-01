import math
from PySide6.QtCore import QRect, QPointF


class CoordinateMapper:
    def __init__(self, rect: QRect, x_min, x_max, y_min, y_max):
        self.viewport = rect
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

        dx = (x_max - x_min) if x_max != x_min else 1.0
        dy = (y_max - y_min) if y_max != y_min else 1.0

        self.px_for_x = self.viewport.width() / dx
        self.px_for_y = self.viewport.height() / dy

    def math_to_pixels(self, point: QPointF) -> QPointF:
        x_px = self.viewport.left() + (point.x() - self.x_min) * self.px_for_x
        y_px = self.viewport.bottom() - (point.y() - self.y_min) * self.px_for_y
        return QPointF(x_px, y_px)

    def pixels_to_math(self, point: QPointF) -> QPointF:
        x_math = self.x_min + (point.x() - self.viewport.left()) / self.px_for_x
        y_math = self.y_min + (self.viewport.bottom() - point.y()) / self.px_for_y
        return QPointF(x_math, y_math)

    def _to_nice_number(self, raw_step):
        if raw_step == 0:
            return 1
        magnitude = 10 ** math.floor(math.log10(raw_step))
        res = raw_step / magnitude
        if res < 1.5:
            res = 1
        elif res < 3:
            res = 2
        elif res < 7:
            res = 5
        else:
            res = 10
        return res * magnitude

    def calculate_optimal_step(self):
        min_pixels_per_label = 100

        max_x_labels_сnt = max(1, self.viewport.width() // min_pixels_per_label)

        math_range = self.x_max - self.x_min
        raw_step = math_range / max_x_labels_сnt

        nice_step = self._to_nice_number(raw_step)

        return nice_step

    """Dump"""

    # def _recalculate_pixels_for_xy(self):
    #     self.px_for_x = self.viewport.width() / (self.x_max - self.x_min)
    #     self.px_for_y = self.viewport.height() / (self.y_max - self.y_min)

    # def _calculate_nice_grid_step(self, axis_range):
    #     if axis_range <= 0:
    #         return 0.1

    #     target_ticks = 20
    #     raw_step = axis_range / target_ticks

    #     magnitude = 10 ** math.floor(math.log10(raw_step))
    #     residual = raw_step / magnitude

    #     if residual < 1.2:
    #         step = 1.0 * magnitude
    #     elif residual < 2.5:
    #         step = 2.0 * magnitude
    #     elif residual < 6.0:
    #         step = 5.0 * magnitude
    #     else:
    #         step = 10.0 * magnitude

    #     print(f"Step {step}")
    #     return step

    # def set_viewport(self, rect: QRect):
    #     self.viewport = rect
    #     self._recalculate_pixels_for_xy()

    # def set_bounds(self, x_min_raw, x_max_raw, y_min_raw, y_max_raw):
    #     self.grid_step_x = self._calculate_nice_grid_step(x_max_raw - x_min_raw)
    #     self.grid_step_y = self._calculate_nice_grid_step(y_max_raw - y_min_raw)

    #     self.x_min = math.floor(x_min_raw / self.grid_step_x) * self.grid_step_x
    #     self.x_max = math.ceil(x_max_raw / self.grid_step_x) * self.grid_step_x

    #     margin_y = self.grid_step_y * 0.05
    #     self.y_min = (
    #         math.floor((y_min_raw - margin_y) / self.grid_step_y) * self.grid_step_y
    #     )
    #     self.y_max = (
    #         math.ceil((y_max_raw + margin_y) / self.grid_step_y) * self.grid_step_y
    #     )

    #     if self.y_min == self.y_max:
    #         self.y_min -= self.grid_step_y
    #         self.y_max += self.grid_step_y

    #     self._recalculate_pixels_for_xy()

    # def update_auto_steps(self):
    #     self.grid_step_x = self._calculate_nice_grid_step(self.x_max - self.x_min)
    #     self.grid_step_y = self._calculate_nice_grid_step(self.y_max - self.y_min)
