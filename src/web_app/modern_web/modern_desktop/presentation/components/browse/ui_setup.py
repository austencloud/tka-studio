"""
UI Setup for Sequence Browser Panel

Handles the UI setup and component creation for the sequence browser.
Separates UI construction from business logic.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .browse_control_panel import BrowseControlPanel
from .modern_navigation_sidebar import ModernNavigationSidebar


class SequenceBrowserUISetup:
    """Handles UI setup for the sequence browser panel."""

    def __init__(self, parent_widget: QWidget):
        """Initialize with parent widget."""
        self.parent = parent_widget

        # UI components that will be created
        self.control_panel: BrowseControlPanel = None
        self.navigation_sidebar: ModernNavigationSidebar = None
        self.scroll_area: QScrollArea = None
        self.grid_layout: QGridLayout = None
        self.grid_widget: QWidget = None
        self.loading_widget: QFrame = None
        self.browsing_widget: QWidget = None
        self.loading_progress_bar: QProgressBar = None
        self.loading_label: QLabel = None
        self.cancel_button: QPushButton = None

    def setup_ui(self) -> None:
        """Setup the complete UI structure."""
        layout = QVBoxLayout(self.parent)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Control panel
        self.control_panel = BrowseControlPanel(self.parent.state_service)
        layout.addWidget(self.control_panel)

        # Main content area
        content_panel = QFrame()
        content_panel.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """
        )
        content_layout = QVBoxLayout(content_panel)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Loading widget (initially hidden)
        self._setup_loading_widget()
        content_layout.addWidget(self.loading_widget)
        self.loading_widget.hide()

        # Main browsing area: sidebar + grid
        browsing_layout = QHBoxLayout()
        browsing_layout.setSpacing(15)

        # Navigation sidebar
        self.navigation_sidebar = ModernNavigationSidebar()
        self.navigation_sidebar.set_minimum_width(150)
        self.navigation_sidebar.setMaximumWidth(250)
        browsing_layout.addWidget(self.navigation_sidebar, 0)

        # Thumbnail grid scroll area
        self._setup_scroll_area()
        browsing_layout.addWidget(self.scroll_area, 1)

        # Browsing widget container
        self.browsing_widget = QWidget()
        self.browsing_widget.setLayout(browsing_layout)
        content_layout.addWidget(self.browsing_widget)

        layout.addWidget(content_panel)

    def _setup_loading_widget(self) -> None:
        """Setup loading UI components."""
        self.loading_widget = QFrame()
        self.loading_widget.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 20px;
            }
        """
        )

        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setSpacing(15)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Loading title
        title_label = QLabel("Loading Sequences...")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: white; background: transparent; border: none;"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(title_label)

        # Progress bar
        self.loading_progress_bar = QProgressBar()
        self.loading_progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background: rgba(0, 0, 0, 0.3);
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A90E2, stop:1 #7BB3F0);
                border-radius: 6px;
            }
        """
        )
        self.loading_progress_bar.setMinimumHeight(30)
        loading_layout.addWidget(self.loading_progress_bar)

        # Status label
        self.loading_label = QLabel("Preparing to load sequences...")
        self.loading_label.setFont(QFont("Segoe UI", 12))
        self.loading_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent; border: none;"
        )
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_label)

        # Cancel button
        self.cancel_button = QPushButton("Cancel Loading")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 100, 100, 0.8);
                border: 1px solid rgba(255, 100, 100, 1.0);
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 100, 100, 1.0);
            }
            QPushButton:pressed {
                background: rgba(200, 80, 80, 1.0);
            }
        """
        )
        loading_layout.addWidget(self.cancel_button)

    def _setup_scroll_area(self) -> None:
        """Setup the scroll area and grid layout."""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
            }
        """
        )

        # Grid widget with fixed layout
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)

        # Set column stretch factors for 3 equal columns
        for col in range(3):
            self.grid_layout.setColumnStretch(col, 1)

        self.scroll_area.setWidget(self.grid_widget)
