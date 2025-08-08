from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
)


class SortButton(QPushButton):
    """A modern styled sort button with selection state."""

    # Signal emitted when button is clicked
    sort_selected = pyqtSignal(str)  # sort_method

    def __init__(self, label: str, sort_method: str, parent: QWidget | None = None):
        super().__init__(label, parent)

        self.sort_method = sort_method
        self.is_selected = False

        self._setup_styling()
        self._connect_signals()

    def _setup_styling(self) -> None:
        """Setup modern glassmorphism button styling."""
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.setMinimumSize(80, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._update_style()

    def _update_style(self) -> None:
        """Update button style based on selection state."""
        if self.is_selected:
            # Selected state
            self.setStyleSheet(
                """
                QPushButton {
                    background: rgba(100, 150, 255, 0.4);
                    border: 1px solid rgba(100, 150, 255, 0.6);
                    border-radius: 8px;
                    color: white;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(100, 150, 255, 0.5);
                    border: 1px solid rgba(100, 150, 255, 0.7);
                }
                QPushButton:pressed {
                    background: rgba(100, 150, 255, 0.6);
                }
            """
            )
        else:
            # Normal state
            self.setStyleSheet(
                """
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    color: rgba(255, 255, 255, 0.9);
                    padding: 6px 12px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    color: white;
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.15);
                }
            """
            )

    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(lambda: self.sort_selected.emit(self.sort_method))

    def set_selected(self, selected: bool) -> None:
        """Update selection state."""
        self.is_selected = selected
        self._update_style()
