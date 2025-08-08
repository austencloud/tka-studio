#!/usr/bin/env python3
"""
Test script to verify PyQt6 import suggestions are working correctly.
This script helps VS Code's language server index PyQt6 modules properly.
"""

# Test imports that should trigger auto-completion suggestions
from PyQt6.QtCore import (
    pyqtSignal,
)
from PyQt6.QtGui import (
    QFont,
)
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)


def test_qt_components():
    """Test function to ensure PyQt6 components are properly recognized."""
    # Test QFont - this should now have proper autocomplete
    font = QFont("Inter", 12, QFont.Weight.Bold)

    # Test other common Qt components
    app = QApplication([])
    widget = QWidget()
    layout = QVBoxLayout()

    # Test signal
    signal = pyqtSignal(str)

    print("PyQt6 imports working correctly!")
    return app, widget, layout, font, signal


if __name__ == "__main__":
    test_qt_components()
