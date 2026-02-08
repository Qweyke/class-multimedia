from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QColorDialog
from PySide6.QtGui import QColor
from plot_core.renderer import Renderer
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

        # Interval values handling
        self.last_val_from = self._main_ui.from_doubleSpinBox.value()
        self.last_val_to = self._main_ui.to_doubleSpinBox.value()
        self._main_ui.from_doubleSpinBox.editingFinished.connect(
            self._handle_from_change
        )
        self._main_ui.to_doubleSpinBox.editingFinished.connect(self._handle_to_change)

    def _handle_from_change(self):
        val = self._main_ui.from_doubleSpinBox.value()
        if val >= self._main_ui.to_doubleSpinBox.value():
            self._main_ui.from_doubleSpinBox.setValue(self.last_val_from)
        else:
            self.last_val_from = val

    def _handle_to_change(self):
        val = self._main_ui.to_doubleSpinBox.value()
        if val <= self._main_ui.from_doubleSpinBox.value():
            self._main_ui.to_doubleSpinBox.setValue(self.last_val_to)
        else:
            self.last_val_to = val

    def _pick_color(self):
        color = QColorDialog.getColor(self.current_color, self, "Choose function color")

        if color.isValid():
            self.current_color = color
            self._main_ui.color_btn.setStyleSheet(f"background-color: {color.name()};")
            self._plot_func()

    def _plot_func(self):
        self._renderer.plot_function(
            func_name=self._main_ui.func_lineEdit.text(),
            left_x=self._main_ui.from_doubleSpinBox.value(),
            right_x=self._main_ui.to_doubleSpinBox.value(),
            points=self._main_ui.func_points_spinBox.value(),
            color=self.current_color,
            use_cones=self._main_ui.cones_checkBox.isChecked(),
        )
