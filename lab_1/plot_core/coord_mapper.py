import math
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import QRect, QPointF
from PySide6.QtGui import Qt


class CoordinateMapper:

    def __init__(self, x_min, x_max, y_min, y_max):
        self.viewport = QRect()
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

        self.px_for_x = 0.0
        self.px_for_y = 0.0
        self.x_step = 0.0
        self.y_step = 0.0

    def remap(
        self,
        theme,
        new_rect=None,
        new_x_min=None,
        new_x_max=None,
        new_y_min=None,
        new_y_max=None,
    ):
        if new_rect is not None:
            self.viewport = new_rect

        if new_x_min is not None:
            self.x_min = new_x_min

        if new_x_max is not None:
            self.x_max = new_x_max

        if new_y_min is not None:
            self.y_min = new_y_min

        if new_y_max is not None:
            self.y_max = new_y_max

        raw_dx = (self.x_max - self.x_min) if self.x_max != self.x_min else 1.0
        raw_dy = (self.y_max - self.y_min) if self.y_max != self.y_min else 1.0

        self.x_step, self.y_step = self._calculate_optimal_steps_xy(
            raw_dx, raw_dy, theme
        )

        self.x_min, self.x_max = self._round_grid_borders(
            self.x_min, self.x_max, self.x_step
        )
        self.y_min, self.y_max = self._round_grid_borders(
            self.y_min, self.y_max, self.y_step, True
        )

        beauty_dx = self.x_max - self.x_min
        beauty_dy = self.y_max - self.y_min

        self.px_for_x = self.viewport.width() / beauty_dx
        self.px_for_y = self.viewport.height() / beauty_dy

    def _round_grid_borders(self, raw_min, raw_max, step, y_axis=False):
        round_min = math.floor(raw_min / step) * step
        round_max = math.ceil(raw_max / step) * step

        if y_axis:
            if (raw_max - round_max) > -(step * 0.1):  # If within 10% of the edge
                round_max += step
            if (raw_min - round_min) < (step * 0.1):
                round_min -= step

        return round_min, round_max

    def _calculate_optimal_steps_xy(self, dx, dy, theme):
        def get_human_centric_step(raw_step):
            if raw_step == 0:
                return 1

            magnitude = 10 ** math.floor(math.log10(raw_step))
            res = raw_step / magnitude

            if res < 1.25:
                res = 1
            elif res < 2.25:
                res = 2
            elif res < 3.25:
                res = 2.5
            elif res < 4.5:
                res = 4
            elif res < 6.25:
                res = 5
            elif res < 8.75:
                res = 7.5
            else:
                res = 10
            return res * magnitude

        width_gap_px = 60
        font = theme.label_font
        metrics = QFontMetrics(font)
        height_gap_px = metrics.height() * 3

        # Calculate labels quantity that fit current screen
        x_gaps_cnt = max(1, self.viewport.width() // width_gap_px)
        y_gaps_cnt = max(1, self.viewport.height() // height_gap_px)

        x_raw_step = dx / x_gaps_cnt
        y_raw_step = dy / y_gaps_cnt

        x_nice_step = get_human_centric_step(x_raw_step)
        y_nice_step = get_human_centric_step(y_raw_step)

        return x_nice_step, y_nice_step

    def math_to_pixels(self, point: QPointF) -> QPointF:
        x_px = self.viewport.left() + (point.x() - self.x_min) * self.px_for_x
        y_px = self.viewport.bottom() - (point.y() - self.y_min) * self.px_for_y
        return QPointF(x_px, y_px)

    def pixels_to_math(self, point: QPointF) -> QPointF:
        x_math = self.x_min + (point.x() - self.viewport.left()) / self.px_for_x
        y_math = self.y_min + (self.viewport.bottom() - point.y()) / self.px_for_y
        return QPointF(x_math, y_math)
