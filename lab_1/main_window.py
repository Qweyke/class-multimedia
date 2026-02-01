from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QColorDialog
from PySide6.QtGui import QColor
from renderer import Renderer
from gui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._main_ui = Ui_MainWindow()
        self._main_ui.setupUi(self)

        # Create chart widget, insert it to GUI widget's space
        self._renderer = Renderer(parent=self._main_ui.plot_wdgt)
        layout = QVBoxLayout(self._main_ui.plot_wdgt)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._renderer)

        self.current_color = QColor(204, 0, 0)
        self._main_ui.color_btn.setStyleSheet(
            f"background-color: {self.current_color.name()};"
        )

        # Connect btns
        self._main_ui.plot_btn.clicked.connect(self._plot_func)
        self._main_ui.clear_btn.clicked.connect(self._renderer.clear)
        self._main_ui.color_btn.clicked.connect(self._pick_color)

    def _pick_color(self):
        color = QColorDialog.getColor(self.current_color, self, "Choose function color")

        if color.isValid():
            self.current_color = color
            self._main_ui.color_btn.setStyleSheet(f"background-color: {color.name()};")
            self._plot_func()

    def _plot_func(self):
        self._renderer.plot_func(
            func_name=self._main_ui.func_lineEdit.text(),
            left_x=self._main_ui.from_doubleSpinBox.value(),
            right_x=self._main_ui.to_doubleSpinBox.value(),
            points=self._main_ui.func_points_spinBox.value(),
            color=self.current_color,
            use_cones=self._main_ui.cones_checkBox.isChecked(),
        )
