"""
Right Panel Tab Navigation Widget

A tab-based navigation widget for the top of the right panel in the construct tab.
Provides 3 tabs for switching between Picker, Graph Editor, and Generate Controls.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy, QWidget


class RightPanelTabWidget(QWidget):
    """
    Tab navigation widget for the right panel.

    Provides 3 equally-sized tabs:
    - 🔨 Picker (Start Position Picker/Option Picker)
    - 🔧 Graph Editor
    - 🤖 Generate Controls
    """

    # Signals emitted when tabs are clicked
    picker_tab_clicked = pyqtSignal()
    graph_editor_tab_clicked = pyqtSignal()
    generate_controls_tab_clicked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_tab = 0  # 0=Picker, 1=Graph Editor, 2=Generate Controls
        self._tab_buttons = []
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the tab navigation UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Tab definitions
        tab_configs = [
            ("🔨 Build", self.picker_tab_clicked),
            ("🤖 Generate", self.generate_controls_tab_clicked),
            ("🔧 Edit", self.graph_editor_tab_clicked),
        ]

        for i, (text, signal) in enumerate(tab_configs):
            tab_button = self._create_tab_button(text, i, signal)
            self._tab_buttons.append(tab_button)
            layout.addWidget(tab_button)

        # Set the first tab as active by default
        self._set_active_tab(0)

    def _create_tab_button(
        self, text: str, index: int, signal: pyqtSignal
    ) -> QPushButton:
        """Create a single tab button."""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumHeight(40)
        button.setMaximumHeight(40)

        # Connect the button click to both the signal and tab switching
        button.clicked.connect(lambda: self._on_tab_clicked(index))
        button.clicked.connect(signal)

        return button

    def _on_tab_clicked(self, index: int):
        """Handle tab button click."""
        self._set_active_tab(index)

    def _set_active_tab(self, index: int):
        """Set the active tab and update button states."""
        if 0 <= index < len(self._tab_buttons):
            self._current_tab = index

            # Update button states
            for i, button in enumerate(self._tab_buttons):
                button.setChecked(i == index)

    def set_active_tab(self, index: int):
        """Public method to set the active tab from external code."""
        self._set_active_tab(index)

    def get_active_tab(self) -> int:
        """Get the currently active tab index."""
        return self._current_tab

    def _apply_styling(self):
        """Apply modern tab styling."""
        self.setStyleSheet(
            """
            RightPanelTabWidget {
                background-color: #f0f0f0;
                border-bottom: 2px solid #d0d0d0;
            }
            
            QPushButton {
                background-color: #e8e8e8;
                border: none;
                border-right: 1px solid #d0d0d0;
                color: #666666;
                font-size: 12px;
                font-weight: 500;
                padding: 8px 12px;
                text-align: center;
            }
            
            QPushButton:last-child {
                border-right: none;
            }
            
            QPushButton:hover {
                background-color: #f5f5f5;
                color: #333333;
            }
            
            QPushButton:checked {
                background-color: #ffffff;
                color: #000000;
                font-weight: 600;
                border-bottom: 2px solid #007acc;
            }
            
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """
        )
