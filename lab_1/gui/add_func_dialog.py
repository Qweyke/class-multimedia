from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QColorDialog,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

STYLE_MAP = {
    "Solid": Qt.PenStyle.SolidLine,
    "Dash": Qt.PenStyle.DashLine,
    "Dot": Qt.PenStyle.DotLine,
    "Dash-Dot": Qt.PenStyle.DashDotLine,
}


class AddFunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Function")
        self.selected_color = QColor("red")  # Default

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.func_input = QLineEdit("10*sin(x)")

        self.color_btn = QPushButton("Pick Color")
        self.color_btn.clicked.connect(self.pick_color)

        self.line_style = QComboBox()
        self.line_style.addItems(list(STYLE_MAP.keys()))

        form.addRow("Expression:", self.func_input)
        form.addRow("Line Style:", self.line_style)
        form.addRow("Color:", self.color_btn)

        layout.addLayout(form)

        self.ok_btn = QPushButton("Add to Plot")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_btn.setStyleSheet(f"background-color: {color.name()}")

    def get_data(self):
        return {
            "expr": self.func_input.text(),
            "color": self.selected_color,
            "line": STYLE_MAP.get(self.line_style.currentText(), Qt.PenStyle.SolidLine),
        }
