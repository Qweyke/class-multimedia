from PySide6.QtWidgets import QListWidget, QWidget
from PySide6.QtCore import Qt


class RemovableListWidget(QListWidget):
    def __init__(self, /, parent: QWidget) -> None:
        super().__init__(
            parent,
        )

    def keyPressEvent(self, event):

        # Check if the pressed key is the Delete key
        if event.key() == Qt.Key.Key_Delete:
            self.remove_selected_items()
        else:
            # Important: let other keys (arrows, etc.) work normally
            super().keyPressEvent(event)

    def remove_selected_items(self):
        # Loop through selected items and remove them
        for item in self.selectedItems():
            # takeItem requires a row index
            row = self.row(item)
            self.takeItem(row)
            # In Python, 'del item' isn't strictly necessary for memory here,
            # but it's good practice if you have heavy custom objects.
            del item
