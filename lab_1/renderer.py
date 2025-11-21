from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QPolygonF, QPen, QColor

from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QBrush, QPolygon
from PySide6.QtWidgets import QWidget


from log.custom_logger import logger

BASE_CELL_SIZE_PX = 40
Y_RANGE_INDENT = 1.1


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Plugs for chart and for plotting area
        self._pixmap = QPixmap()
        self._plotting_rect = QRect()

        # Qt's real pixel coords
        self._qt_center_x = None
        self._qt_center_y = None

        self._cell_size_x = BASE_CELL_SIZE_PX
        self._cell_size_y = BASE_CELL_SIZE_PX

    def _reinit_plotting_areas(self):
        def reinit_pixmap():
            self._pixmap = QPixmap(self.width(), self.height())
            self._pixmap.fill(QColor(224, 224, 224))
            "Reinitialize Pixmap: Success"

        def reinit_rect():
            start_x = int(self.width() * 0.05)
            start_y = int(self.height() * 0.01)

            indent_y = int(self.height() * 0.07)

            self._plotting_rect = QRect(
                start_x,
                start_y,
                self.width()
                - start_x
                - start_y,  # Add the same indent as Y has at the top
                self.height() - indent_y,
            )
            logger.debug(
                f"Reinitialize Plotting-Rectangle: Success \ Start x coord: {start_x}; y coord: {start_y}"
            )

        def calculate_new_centers():
            self._qt_center_x = self._plotting_rect.left() + int(
                self._plotting_rect.width() / 2
            )

            self._qt_center_y = self._plotting_rect.top() + int(
                self._plotting_rect.height() / 2
            )
            logger.debug("Recalculate Centers: Success")

        # New pixmap-object with actual sizes
        reinit_pixmap()

        # Create area for chart plotting (axis rectangle for plotting)
        reinit_rect()

        # Calculate current center coordinates
        calculate_new_centers()

        logger.info("Reinitialize Drawing-Areas: Success")

    def resizeEvent(self, event):
        self._reinit_plotting_areas()
        # self._create_axis_grid()

    # Draw event for pre-drawn pixmap
    def paintEvent(self, event, /):
        def handle_invalid_size():
            if self._pixmap.isNull():
                raise ValueError("Pixmap is null")

            pixmap_size = self._pixmap.size()
            if pixmap_size.width() <= 0 or pixmap_size.height() <= 0:
                raise ValueError(f"Pixmap size is invalid: {pixmap_size}")

            plotting_rect_size = self._plotting_rect.size()
            if plotting_rect_size.width() <= 0 or plotting_rect_size.height() <= 0:
                raise ValueError(f"Plotting rect size is invalid: {plotting_rect_size}")

        try:
            handle_invalid_size()
        except Exception as ex:
            logger.error(f"Draw Areas: Fail / {ex}")
            return

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._pixmap)
        painter.end()

        logger.debug("Draw Areas: Success")

    def _to_qt_coordinates(self, logic_x, logic_y):
        x = self._plotting_rect.left() + (logic_x - self._func_left_x) * self._cell_size_x
        y = self._plotting_rect.top() + (self._func_y_max - logic_y) * self._cell_size_y
        return int(x), int(y)

    def _to_logic_coordinates(self, qt_x, qt_y):
        logic_x = self._func_left_x + (qt_x - self._plotting_rect.left()) / self._cell_size_x
        logic_y = self._func_y_max - (qt_y - self._plotting_rect.top()) / self._cell_size_y
        return logic_x, logic_y

    def clear_canvas(self):
        logger.debug("Clear canvas")
        self._pixmap.fill(QColor(224, 224, 224))
        self._cell_size_x = BASE_CELL_SIZE_PX
        self._cell_size_y = BASE_CELL_SIZE_PX
        self.update()

    def _calculate_cell_size_for_func(self, left_x, right_x, step, y_vals: list[float]):
        # --- Save function range (NECESSARY for convertors) ---
        self._func_left_x = left_x
        self._func_right_x = right_x

        y_sorted = sorted(y_vals)
        self._func_y_max = y_sorted[-1]
        self._func_y_min = y_sorted[0]

        # --- Calculate X cell size ---
        points_num = right_x - left_x
        self._cell_size_x = self._plotting_rect.width() / points_num / step

        # --- Calculate Y cell size ---
        y_range = self._func_y_max - self._func_y_min
        self._cell_size_y = self._plotting_rect.height() / (y_range * Y_RANGE_INDENT)

        logger.debug(
            f"Cell size: x={self._cell_size_x}, y={self._cell_size_y}; "
            f"Y-range: {self._func_y_min}..{self._func_y_max}"
    )


    def _create_axis_grid(self):
        logger.debug(
            f"Creating axis grid, [{self._plotting_rect.width()}; {self._plotting_rect.height()}], cell: [{self._cell_size_x}; {self._cell_size_y}]"
        )

        # Clear prev drawings
        self._pixmap.fill(QColor(224, 224, 224))

        painter = QPainter(self._pixmap)
        thickness = 2
        border_pen = QPen(Qt.black, thickness, Qt.SolidLine)
        painter.setPen(border_pen)
        painter.drawRect(self._plotting_rect)

        # Prepare to draw grid lines
        grid_pen = QPen(Qt.black, 1, Qt.DotLine)
        painter.setPen(grid_pen)
        font_metrics = painter.fontMetrics()

        # Draw (vertical or 'x') grid lines
        halves_rows_num = int(self._plotting_rect.width() / self._cell_size_x / 2)

        # Calculate start pos for text y, shift it down by height of text and small indent
        text_baseline_y = int(
            self._plotting_rect.bottom()
            + font_metrics.height()
            + (self._plotting_rect.height() * 0.005)
        )

        for i in range(-halves_rows_num, halves_rows_num + 1):
            x = self._qt_center_x + i * self._cell_size_x
            # Draw lines
            painter.drawLine(
                int(x), self._plotting_rect.top(), int(x), self._plotting_rect.bottom()
            )

            # Draw cell's legend
            logic_x, _ = self._to_logic_coordinates(x, 0)
            text = f"{logic_x:.1f}"
            text_width = font_metrics.horizontalAdvance(text)

            # Calculate start pos for text, shift it left by half of its width
            text_baseline_x = int(x - text_width / 2)

            painter.drawText(text_baseline_x, text_baseline_y, text)

        # Draw (horizontal or 'y') grid lines
        halves_cols_num = int(self._plotting_rect.height() / self._cell_size_y / 2)
        for i in range(-halves_cols_num, halves_cols_num + 1):
            y = self._qt_center_y + i * self._cell_size_y
            # Draw lines
            painter.drawLine(
                self._plotting_rect.left(), int(y), self._plotting_rect.right(), int(y)
            )

            # Draw cell's legend
            _, logic_y = self._to_logic_coordinates(0, y)
            text = f"{logic_y:.1f}"
            text_width = font_metrics.horizontalAdvance(text)

            # Calculate start pos for text, shift it left by half of its width
            text_baseline_x = int(
                self._plotting_rect.left()
                - text_width
                - (self._plotting_rect.width() * 0.005)
            )
            text_baseline_y = int((y + font_metrics.ascent() / 2))

            painter.drawText(text_baseline_x, text_baseline_y, text)

        painter.end()
        self.update()

    def draw_central_dot(self):
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._plotting_rect)
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)
        x, y = self._to_qt_coordinates(0, 0)
        painter.drawPoint(x, y)
        painter.end()
        self.update()

    def draw_function(
        self,
        func,
        left_x: float,
        right_x: float,
        step: float = 1,
        line_thickness: int = 2,
    ):
        logger.debug("Function plotting")
        x = left_x
        y_vals_list = []

        while x <= right_x:
            try:
                y_vals_list.append(func(x))
            except Exception as ex:
                logger.error(f"Error at x={x}: {ex}")

            x += step

        self._calculate_cell_size_for_func(left_x, right_x, step, y_vals_list)
        self._create_axis_grid()

        # Create painter and restrict its action to plotting_rect area
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._plotting_rect)
        pen = QPen(Qt.blue, line_thickness, Qt.SolidLine)
        painter.setPen(pen)

        x = left_x
        prev = None
        while x <= right_x:
            try:
                y = func(x)
                pixel_x, pixel_y = self._to_qt_coordinates(x, y)

                if prev is not None:
                    painter.drawLine(prev[0], prev[1], pixel_x, pixel_y)

                prev = (pixel_x, pixel_y)

            except Exception as ex:
                logger.debug(f"Error at x={x}: {ex}")

            x += step

        painter.end()
        self.update()

    def draw_function_cones3d(
    self,
    func,
    x_start: float,
    x_end: float,
    step: float = 0.2,
    cone_width: float = 1.0,
    color: QColor = QColor(220, 20, 120),
):
        logger.debug("Drawing 3D cones")

        # ---------------------------
        # 1) Collect ALL y-values
        # ---------------------------
        x = x_start
        y_vals_list = []

        while x <= x_end:
            try:
                y_vals_list.append(func(x))
            except Exception as ex:
                logger.error(f"Error at x={x}: {ex}")
            x += step

        if not y_vals_list:
            logger.error("No y-values computed. Cannot draw cones.")
            return

        # ---------------------------
        # 2) Auto-scale like normal graph
        # ---------------------------
        self._calculate_cell_size_for_func(x_start, x_end, step, y_vals_list)
        self._create_axis_grid()

        # ---------------------------
        # 3) Start actual drawing
        # ---------------------------
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._plotting_rect)

        base_color = QColor(color)
        dark_color = QColor(color.darker(160))
        light_color = QColor(color.lighter(140))

        x = x_start
        last_y = None

        while x <= x_end:
            try:
                y = func(x)

                top_x, top_y = self._to_qt_coordinates(x, y)
                base_left_x, base_left_y = self._to_qt_coordinates(
                    x - cone_width / 2, 0
                )
                base_right_x, base_right_y = self._to_qt_coordinates(
                    x + cone_width / 2, 0
                )
                center_x, center_y = self._to_qt_coordinates(x, 0)

                # ellipse radii
                rx = abs(base_left_x - base_right_x) // 2
                ry = max(3, int(0.25 * rx))

                ell_rect = QRect(center_x - rx, center_y - ry, 2 * rx, 2 * ry)

                # shadow side
                left_poly = QPolygon(
                    [
                        QPoint(top_x, top_y),
                        QPoint(base_left_x, base_left_y),
                        QPoint(center_x, center_y),
                    ]
                )
                painter.setBrush(QBrush(dark_color))
                painter.setPen(Qt.NoPen)
                painter.drawPolygon(left_poly)

                # bright side
                right_poly = QPolygon(
                    [
                        QPoint(top_x, top_y),
                        QPoint(base_right_x, base_right_y),
                        QPoint(center_x, center_y),
                    ]
                )
                painter.setBrush(QBrush(light_color))
                painter.drawPolygon(right_poly)

                # ellipse
                painter.setBrush(QBrush(dark_color))
                painter.drawPie(ell_rect, 0 * 16, 180 * 16)
                painter.setBrush(QBrush(light_color))
                painter.drawPie(ell_rect, 180 * 16, 180 * 16)

                painter.setPen(QPen(Qt.black, 0.7))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(ell_rect)

            except Exception as ex:
                logger.debug(f"Error at x={x}: {ex}")

            x += step

        painter.end()
        self.update()

