#!/usr/bin/env python3
"""
TKA Dock Components - Individual Dock UI Components
==================================================

Focused components for the TKA dock interface including:
- DockApplicationIcon: Individual application icons with status indicators
- Status management and visual feedback
- Mouse interaction handling

Architecture:
- Extracted from dock_window.py for better separation of concerns
- Maintains clean interface with main dock window
- Follows TKA's reliable design system patterns
"""

import logging
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor

from domain.models import ApplicationData, ApplicationStatus

logger = logging.getLogger(__name__)


class DockApplicationIcon(QFrame):
    """Compact application icon for dock display."""

    launch_requested = pyqtSignal(str)  # app_id
    context_menu_requested = pyqtSignal(str, object)  # app_id, position

    def __init__(self, app_data: ApplicationData, style_builder):
        super().__init__()

        self.app_data = app_data
        self.style_builder = style_builder
        self.current_status = app_data.status

        # Slightly larger icon size for better touch targets
        self.setFixedSize(44, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_layout()
        self._setup_styling()

        # Set tooltip
        self.setToolTip(f"{app_data.title}\n{app_data.description}")

    def _setup_layout(self):
        """Setup icon layout."""
        layout = QVBoxLayout(self)
        # Adjust margins for larger icon
        layout.setContentsMargins(3, 3, 3, 3)

        # Icon label (using emoji for now)
        self.icon_label = QLabel(self.app_data.icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Increase font for slightly larger icon
        self.icon_label.setStyleSheet("font-size: 22px;")

        layout.addWidget(self.icon_label)

    def _setup_styling(self):
        """Setup icon styling."""
        self._update_style_for_status(self.current_status)

    def _update_style_for_status(self, status: ApplicationStatus):
        """Update styling based on application status."""
        if status == ApplicationStatus.RUNNING:
            # Running state - green accent
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(34, 197, 94, 0.3),
                        stop:1 rgba(34, 197, 94, 0.1));
                    border: 1px solid rgba(34, 197, 94, 0.5);
                    border-radius: 8px;
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(34, 197, 94, 0.4),
                        stop:1 rgba(34, 197, 94, 0.2));
                    border: 1px solid rgba(34, 197, 94, 0.7);
                }}
            """
            )
        elif status == ApplicationStatus.STARTING:
            # Starting state - blue accent with subtle animation
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(59, 130, 246, 0.3),
                        stop:1 rgba(59, 130, 246, 0.1));
                    border: 1px solid rgba(59, 130, 246, 0.5);
                    border-radius: 8px;
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(59, 130, 246, 0.4),
                        stop:1 rgba(59, 130, 246, 0.2));
                    border: 1px solid rgba(59, 130, 246, 0.7);
                }}
            """
            )
        elif status == ApplicationStatus.ERROR:
            # Error state - red accent
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(239, 68, 68, 0.3),
                        stop:1 rgba(239, 68, 68, 0.1));
                    border: 1px solid rgba(239, 68, 68, 0.5);
                    border-radius: 8px;
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(239, 68, 68, 0.4),
                        stop:1 rgba(239, 68, 68, 0.2));
                    border: 1px solid rgba(239, 68, 68, 0.7);
                }}
            """
            )
        else:
            # Stopped state - subtle glassmorphism appearance
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.1),
                        stop:1 rgba(255, 255, 255, 0.05));
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 8px;
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.2),
                        stop:1 rgba(255, 255, 255, 0.1));
                    border: 1px solid rgba(255, 255, 255, 0.25);
                }}
            """
            )

    def update_status(self, status: ApplicationStatus):
        """Update the visual status of this icon."""
        self.current_status = status
        self._update_style_for_status(status)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.launch_requested.emit(self.app_data.id)
        elif event.button() == Qt.MouseButton.RightButton:
            self.context_menu_requested.emit(self.app_data.id, QCursor.pos())

        super().mousePressEvent(event)
