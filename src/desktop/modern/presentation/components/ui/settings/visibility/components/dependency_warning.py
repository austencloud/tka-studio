"""
Dependency Warning Component for Visibility Settings.

Focused component for displaying motion dependency warnings with glassmorphism styling.
Extracted from the monolithic visibility tab following TKA clean architecture principles.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class DependencyWarning(QLabel):
    """
    Warning display component for motion dependencies.
    
    Shows/hides warnings when motion visibility affects element visibility options.
    Follows TKA single-responsibility principle and glassmorphism design.
    """

    def __init__(self, parent=None):
        """
        Initialize dependency warning component.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.setText(
            "⚠️ Some visibility options are hidden.\nActivate both motions to show them."
        )
        self.setObjectName("dependency_warning")
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Initially hidden
        self.hide()
        
        self._apply_styling()

    def set_visible(self, visible: bool):
        """
        Set warning visibility based on dependency state.
        
        Args:
            visible: Whether to show the warning
        """
        if visible:
            self.show()
        else:
            self.hide()

    def update_warning_state(self, all_motions_visible: bool):
        """
        Update warning visibility based on motion states.
        
        Args:
            all_motions_visible: Whether all motions are currently visible
        """
        self.set_visible(not all_motions_visible)

    def _apply_styling(self):
        """Apply glassmorphism styling to the warning."""
        self.setStyleSheet(
            """
            QLabel#dependency_warning {
                color: rgba(255, 193, 7, 1.0);
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                background: rgba(255, 193, 7, 0.1);
                border: 2px solid rgba(255, 193, 7, 0.3);
                border-radius: 8px;
                margin: 10px 0;
            }
        """
        )
