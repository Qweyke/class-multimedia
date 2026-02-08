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

        # self.x_min, self.x_max = self._beautify_grid_borders(self.x_min, self.x_max)
        # self.y_min, self.y_max = self._beautify_grid_borders(self.y_min, self.y_max)

        dx = (self.x_max - self.x_min) if self.x_max != self.x_min else 1.0
        dy = (self.y_max - self.y_min) if self.y_max != self.y_min else 1.0

        self.x_step, self.y_step = self._calculate_optimal_steps_xy(dx, dy, theme)

        self.px_for_x = self.viewport.width() / dx
        self.px_for_y = self.viewport.height() / dy

    def _beautify_grid_borders(self, raw_min, raw_max):
        nice_min = math.floor(raw_min)
        nice_max = math.ceil(raw_max)

        return nice_min, nice_max

    def _calculate_optimal_steps_xy(self, dx, dy, theme):
        def beautify_step_number(raw_step):
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

        # Preferred axis-label size
        font = theme.label_font
        metrics = QFontMetrics(font)
        sample_text = "-888.88"
        text_width_px = metrics.horizontalAdvance(sample_text)
        text_height_px = metrics.height()

        # Calculate labels quantity that fit current screen
        x_labels_cnt = max(1, self.viewport.width() // text_width_px)
        y_labels_cnt = max(1, self.viewport.height() // text_height_px)

        x_raw_step = dx / x_labels_cnt
        y_raw_step = dy / y_labels_cnt

        x_nice_step = beautify_step_number(x_raw_step)
        y_nice_step = beautify_step_number(y_raw_step)

        return x_nice_step, y_nice_step

    def math_to_pixels(self, point: QPointF) -> QPointF:
        x_px = self.viewport.left() + (point.x() - self.x_min) * self.px_for_x
        y_px = self.viewport.bottom() - (point.y() - self.y_min) * self.px_for_y
        return QPointF(x_px, y_px)

    def pixels_to_math(self, point: QPointF) -> QPointF:
        x_math = self.x_min + (point.x() - self.viewport.left()) / self.px_for_x
        y_math = self.y_min + (self.viewport.bottom() - point.y()) / self.px_for_y
        return QPointF(x_math, y_math)
