from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from sympy import symbols, sympify, lambdify

from log.custom_logger import logger
from renderer import Renderer
from gui.gui import Ui_MainWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self._main_ui = Ui_MainWindow()
        self._main_ui.setupUi(self)

        # Create chart widget, insert it to GUI widget's space
        self._renderer = Renderer(parent=self._main_ui.plot_wdgt)
        layout = QVBoxLayout(self._main_ui.plot_wdgt)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._renderer)

        # Connect btns
        self._main_ui.plot_btn.clicked.connect(self._plot_func)
        # self._main_ui.clear_btn.clicked.connect(self._renderer.clear_canvas)
        # self._main_ui.grid_btn.clicked.connect(self._renderer._create_axis_grid)
        # self._main_ui.center_btn.clicked.connect(self._renderer.draw_central_dot)

    def showEvent(self, event):
        super().showEvent(event)
        screen = self.windowHandle().screen()

    def _plot_func(self):
        x = symbols("x")
        expr = sympify(self._main_ui.func_lineEdit.text())
        func = lambdify(x, expr, modules=["math"])

        if self._main_ui.cones_checkBox.isChecked():
            #     self._renderer.draw_function_cones3d(
            #         func,
            #         self._main_ui.from_spinBox.value(),
            #         self._main_ui.to_spinBox.value(),
            #         step=self._main_ui.step_spinBox.value(),
            #     )
            # else:
            self._renderer.draw_function(
                func,
                self._main_ui.from_spinBox.value(),
                self._main_ui.to_spinBox.value(),
                self._main_ui.step_spinBox.value(),
            )
