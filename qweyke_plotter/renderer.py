from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget

from custom_logger import logger

BASE_CELL_SIZE_PX_PX = 40
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

        self._cell_size_x = BASE_CELL_SIZE_PX_PX
        self._cell_size_y = BASE_CELL_SIZE_PX_PX

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

    def _to_qt_coordinates(self, logic_x, logic_y) -> tuple[int, int]:
        pixel_x = self._qt_center_x + (logic_x * self._cell_size_x)
        pixel_y = self._qt_center_y - (logic_y * self._cell_size_y)
        return int(pixel_x), int(pixel_y)

    def _to_logic_coordinates(self, pixel_x, pixel_y) -> tuple[float, float]:
        logic_x = (pixel_x - self._qt_center_x) / self._cell_size_x
        # Invert to qt coords
        logic_y = -(pixel_y - self._qt_center_y) / self._cell_size_y
        return logic_x, logic_y

    def clear_canvas(self):
        logger.debug("Clear canvas")
        self._pixmap.fill(QColor(224, 224, 224))
        self._cell_size_x = BASE_CELL_SIZE_PX
        self._cell_size_y = BASE_CELL_SIZE_PX
        self.update()

    def _calculate_cell_size_for_func(self, left_x, right_x, step, y_vals: list[float]):
        # Calculate cell x-size
        points_num = right_x - left_x
        self._cell_size_x = self._plotting_rect.width() / points_num / step

        # Calculate cell y-size
        y_sorted = sorted(y_vals)
        y_top_value = y_sorted[int(len(y_sorted)) - 1]
        y_bottom_value = y_sorted[0]

        y_range = y_top_value - y_bottom_value
        self._cell_size_y = self._plotting_rect.height() / (y_range * Y_RANGE_INDENT)

        logger.debug(f"Cell size: x - {self._cell_size_x}; y - {self._cell_size_y}")

    def draw_function_test(
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

    # def draw_function(self, func, x_start, x_end, step=0.1):
    #     self._last_func = partial(self.draw_function, func, x_start, x_end, step)
    #
    #     painter = QPainter(self._pixmap)
    #     painter.setClipRect(self._plotting_rect)
    #     pen = QPen(Qt.blue, 2)
    #     painter.setPen(pen)
    #
    #     x = x_start
    #     prev = None
    #     while x <= x_end:
    #         try:
    #             y = func(x)
    #             px, py = self._to_pyside_coords(x, y)
    #             if math.isfinite(y):
    #                 if prev is not None:
    #                     if abs(prev[1] - py) < self.height():
    #                         painter.drawLine(prev[0], prev[1], px, py)
    #                 prev = (px, py)
    #             else:
    #                 prev = None
    #
    #         except (ZeroDivisionError, ValueError, OverflowError):
    #             prev = None
    #
    #         except Exception as ex:
    #             logger.debug(f"Error at x={x}: {ex}")
    #
    #         x += step
    #
    #     painter.end()
    #     self.update()

    # def draw_function_cones(self, func, x_start, x_end, color=QColor(80, 160, 255), step=0.1):
    #     self._last_func = partial(self.draw_function_cones, func, x_start, x_end, color, step)
    #
    #     painter = QPainter(self._pixmap)
    #     painter.setClipRect(self._plotting_rect)
    #
    #     cone_width = 1.0
    #     x = x_start
    #     prev_y = None
    #     max_y_jump = (self._logical_range_y * 0.3)
    #     while x <= x_end:
    #         try:
    #             y = func(x)
    #
    #             if not math.isfinite(y):
    #                 prev_y = None
    #                 x += step
    #                 continue
    #
    #             if prev_y is not None and abs(y - prev_y) > max_y_jump:
    #                 prev_y = y
    #                 x += step
    #                 continue
    #
    #             qt_top_x, qt_top_y = self._to_pyside_coords(x, y)
    #             qt_left_x, qt_left_y = self._to_pyside_coords(x - cone_width / 2, 0)
    #             qt_right_x, qt_right_y = self._to_pyside_coords(x + cone_width / 2, 0)
    #
    #             top_point = QPoint(qt_top_x, qt_top_y)
    #             left_point = QPoint(qt_left_x, qt_left_y)
    #             right_point = QPoint(qt_right_x, qt_right_y)
    #
    #             cone = QPolygon([top_point, left_point, right_point])
    #             painter.setBrush(QBrush(color))
    #             painter.setPen(QPen(QColor(0, 0, 0), 0.5))
    #             painter.drawPolygon(cone)
    #
    #             # Преобразуем центр и радиусы
    #             cx, cy = self._to_pyside_coords(x, 0)
    #             rx = abs(left_point.x() - right_point.x()) // 2
    #             ry = int(0.1 * abs(y) * self._scale * (self._plotting_rect.height() / (2 * self._logical_range_y)))
    #
    #             # QRect, in ellipse
    #             rect = QRect(cx - rx, cy - ry, 2 * rx, 2 * ry)
    #
    #             # Left side
    #             painter.setPen(Qt.NoPen)
    #             painter.setBrush(QBrush(color.darker(150)))
    #             painter.drawPie(rect, 180 * 16, 90 * 16)  # from 180° to 270° left
    #
    #             # Right side
    #             painter.setBrush(QBrush(color))
    #             painter.drawPie(rect, 270 * 16, 90 * 16)
    #
    #             # Draw shadow
    #             shadow = QPolygon([top_point, left_point, QPoint(top_point.x(), left_point.y())])
    #             painter.setBrush(QBrush(color.darker(150)))
    #             painter.drawPolygon(shadow)
    #
    #         except (ZeroDivisionError, ValueError, OverflowError):
    #             prev_y = None
    #         except Exception as e:
    #             logger.debug(f"Error at x={x}: {e}")
    #
    #         x += step
    #
    #     painter.end()
    #     self.update()
