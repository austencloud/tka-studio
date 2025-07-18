"""
Right Panel Tab Navigation Widget

A tab-based navigation widget for the top of the right panel in the construct tab.
Provides 3 tabs for switching between Picker, Graph Editor, and Generate Controls.
Uses the centralized glassmorphism style system for consistent modern aesthetics.
"""

from typing import Optional

from presentation.styles.glassmorphism_styles import GlassmorphismStyleGenerator
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
        tab_configs = {
            0: {
                "text": "🔨 Build",
                "signal": self.picker_tab_clicked,
                "tooltip": "Build and construct your sequence",
            },
            1: {
                "text": "🤖 Generate",
                "signal": self.generate_controls_tab_clicked,
                "tooltip": "Generate AI-powered content",
            },
            2: {
                "text": "🔧 Edit",
                "signal": self.graph_editor_tab_clicked,
                "tooltip": "Edit and refine your sequence",
            },
        }

        for index in sorted(tab_configs.keys()):
            config = tab_configs[index]
            tab_button = self._create_tab_button(
                config["text"], index, config["signal"], config["tooltip"]
            )
            self._tab_buttons.append(tab_button)
            layout.addWidget(tab_button)

        # Set the first tab as active by default
        self._set_active_tab(0)

    def _create_tab_button(
        self, text: str, index: int, signal: pyqtSignal, tooltip: str
    ) -> QPushButton:
        """Create a single tab button with glassmorphism styling."""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumHeight(48)
        button.setMaximumHeight(48)

        # Set tooltip
        button.setToolTip(tooltip)

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
        """Apply modern glassmorphism tab styling using the centralized style system."""
        # Container styling
        container_style = """
        RightPanelTabWidget {
            background: rgba(255, 255, 255, 0.05);
            border: none;
            border-radius: 12px;
            margin: 4px;
        }
        """

        # Tab button styling using the glassmorphism style generator
        tab_style = GlassmorphismStyleGenerator.create_tab_style(
            active_variant="accent"
        )

        # Combine all styles
        self.setStyleSheet(container_style + tab_style)
