from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPointF, QPoint, QSize
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QFont, QTransform
from PySide6.QtWidgets import QWidget


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._cached_pixmap = None
        self._x_min = -10
        self._y_min = 0
        self._x_max = 10
        self._y_max = 5
        self._dots_qnty = 100

    def resizeEvent(self, event):
        self._build_axis_grid()
        self.update()

    def paintEvent(self, event):
        if self._cached_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(QPointF(0, 0), self._cached_pixmap)

    def _calculate_transform(self):
        # Define rendering area
        x_margin = int(self.width() * 0.05)
        y_margin = int(self.height() * 0.05)
        rect_start_point = QPoint(x_margin, y_margin)
        rect_size = QSize((self.width() - 2 * x_margin), (self.height() - 2 * y_margin))
        render_area_rect = QRect(rect_start_point, rect_size)

        # Calculate ratio between qt and logic coords
        scale_x = round(render_area_rect.width() / (self._x_max - self._x_min))
        scale_y = round(render_area_rect.height() / (self._y_max - self._y_min))

        # Move start point to logical axis start
        dx = round(render_area_rect.x() - (self._x_min * scale_x))
        dy = round(
            render_area_rect.y() + render_area_rect.height() - (self._y_min * scale_y)
        )

        print(f"Scale: {scale_x, scale_y}")
        print(f"Differ {dx, dy}")

        # Create affine matrix
        transform = QTransform()
        transform.translate(dx, dy)
        transform.scale(scale_x, -scale_y)

        return transform

    def _math_point_to_pixels(self, plot_area: QRect, point: QPointF):
        px_per_x_unit = plot_area.width() / (self._x_max - self._x_min)
        px_per_y_unit = plot_area.height() / (self._y_max - self._y_min)
        print(f"X-unit {px_per_x_unit}px , Y-unit {px_per_y_unit}px ")

        px = plot_area.left() + (point.x() - self._x_min) * px_per_x_unit
        py = plot_area.bottom() - (point.y() - self._y_min) * px_per_y_unit

        return QPointF(px, py)

    def _build_axis_grid(self):
        # Initialize drawing cache, fill it in with mono-color
        self._cached_pixmap = QPixmap(self.width(), self.height())
        self._cached_pixmap.fill(QColor(255, 255, 225))

        painter = QPainter(self._cached_pixmap)
        print(f"Viewport rect {painter.viewport()}")

        plot_area = painter.viewport()

        painter.setPen(QPen(Qt.gray, 1, Qt.DotLine))
        # Vertical
        step_x = (self._x_max - self._x_min) / self._dots_qnty
        x = self._x_min + step_x
        while x < self._x_max:
            painter.drawLine(
                self._math_point_to_pixels(plot_area, QPointF(x, self._y_min)),
                self._math_point_to_pixels(plot_area, QPointF(x, self._y_max)),
            )
            x += step_x

        # Horizontal
        step_y = (self._y_max - self._y_min) / self._dots_qnty
        y = self._y_min + step_y
        while y < self._y_max:
            painter.drawLine(
                self._math_point_to_pixels(plot_area, QPointF(self._x_min, y)),
                self._math_point_to_pixels(plot_area, QPointF(self._x_max, y)),
            )
            y += step_y

        painter.end()

    def _test(self):
        painter = self._create_adjusted_painter()
        # Test
        painter.setPen(QPen(Qt.red, 0, Qt.SolidLine))
        painter.drawRect(QRect(QPoint(0, 0), QSize(10, 5)))
        painter.drawLine(QPoint(0, 0), QPoint(5, 10))
