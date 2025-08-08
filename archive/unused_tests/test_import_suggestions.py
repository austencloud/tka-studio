"""
Test file for PyQt6 import suggestions.

Instructions:
1. Delete one of the imports below (e.g., remove 'from PyQt6.QtGui import QFont')
2. Then somewhere in the code, type 'QFont'
3. Position your cursor on the red underlined 'QFont'
4. Press Ctrl+. (or Ctrl+Shift+.)
5. You should see import suggestions like "Import 'QFont' from 'PyQt6.QtGui'"

Try this with any PyQt6 component!
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TestWidget(QWidget):
    test_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Test QFont usage - try removing the import above!
        label = QLabel("Test Label")
        font = QFont("Inter", 12, QFont.Weight.Bold)
        label.setFont(font)

        layout.addWidget(label)

        # Try typing these without imports to test Ctrl+.:
        # QPushButton - should suggest PyQt6.QtWidgets
        # QTimer - should suggest PyQt6.QtCore
        # QPixmap - should suggest PyQt6.QtGui
        # QApplication - should suggest PyQt6.QtWidgets


if __name__ == "__main__":
    # Remove this import and try Ctrl+. on QApplication:
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    widget = TestWidget()
    widget.show()
    app.exec()
