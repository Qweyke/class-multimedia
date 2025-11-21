import sys

from PySide6.QtWidgets import QApplication

from core import MainApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
