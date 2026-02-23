from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QColorDialog,
    QDialog,
    QListWidgetItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap, QIcon
from gui.add_func_dialog import AddFunctionDialog
from gui.removable_list_view import RemovableListWidget
from plot_core.function_resolver import FunctionResolver
from plot_core.renderer import Renderer
from res.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._main_ui = Ui_MainWindow()
        self._main_ui.setupUi(self)

        self.setWindowTitle("Simple Plotter")

        # Create chart widget, insert it to GUI widget's space
        self._renderer = Renderer(parent=self._main_ui.plot_wdgt)
        layout = QVBoxLayout(self._main_ui.plot_wdgt)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._renderer)

        self.funcs_list = RemovableListWidget(parent=self._main_ui.plot_wdgt)
        layout = QVBoxLayout(self._main_ui.funcs_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.funcs_list)

        # Connect btns
        self._main_ui.clear_btn.clicked.connect(self._renderer.clear)
        self._main_ui.add_btn.clicked.connect(self._handle_add_function)

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

    # def _plot_func(self):
    #     self._renderer.plot_function(
    #         func_name=self._main_ui.func_lineEdit.text(),
    #         left_x=self._main_ui.from_doubleSpinBox.value(),
    #         right_x=self._main_ui.to_doubleSpinBox.value(),
    #         points=self._main_ui.func_points_spinBox.value(),
    #         color=self.current_color,
    #         use_cones=self._main_ui.cones_checkBox.isChecked(),
    #     )

    def get_active_plots(self):
        active_funcs = []
        for i in range(self.funcs_list.count()):
            item = self.funcs_list.item(i)
            active_funcs.append(item.data(Qt.ItemDataRole.UserRole))

        print(active_funcs)
        return active_funcs

    def _handle_add_function(self):
        func_dialog = AddFunctionDialog()

        if func_dialog.exec() == QDialog.DialogCode.Accepted:
            func_gata = func_dialog.get_data()
            func_item = QListWidgetItem(func_gata["expr"])

            _, _, x_vals, y_vals = FunctionResolver.get_prepared_values(
                left_x=self._main_ui.from_doubleSpinBox.value(),
                right_x=self._main_ui.to_doubleSpinBox.value(),
                function_symbolic=func_gata["expr"],
                points_qnty=self._main_ui.func_points_spinBox.value(),
            )

            func_item.setData(
                Qt.ItemDataRole.UserRole,
                {
                    "x_vals": x_vals,
                    "y_vals": y_vals,
                    "color": func_gata["color"],
                    "line": func_gata["line"],
                },
            )

            # 4. Set the Marker Icon [cite: 21]
            pix = QPixmap(12, 12)
            pix.fill(func_gata["color"])
            func_item.setIcon(QIcon(pix))

            self.funcs_list.addItem(func_item)

            self.get_active_plots()

            self._renderer.plot_function(
                func_name=func_gata["expr"],
                left_x=self._main_ui.from_doubleSpinBox.value(),
                right_x=self._main_ui.to_doubleSpinBox.value(),
                points=self._main_ui.func_points_spinBox.value(),
                color=func_gata["color"],
                use_cones=self._main_ui.cones_checkBox.isChecked(),
            )
