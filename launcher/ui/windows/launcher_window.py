#!/usr/bin/env python3
"""
TKA Modern Launcher Window - Premium UI Component
================================================

The main launcher window built with pure PyQt6 and custom glassmorphism design:
- Premium 2025 glassmorphism effects
- Application grid with smooth animations
- Dual-mode operation (window/docked)
- Inter typography with 8px grid system
- WCAG 4.5:1 contrast ratios

Architecture:
- Pure PyQt6 with custom styling
- Modular component design
- Clean separation of UI and business logic
- QPropertyAnimation-based micro-interactions
"""

import logging

from ui.layouts.application_grid import ApplicationGridWidget
from config.config.launcher_config import LauncherConfig
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
)
from ui.pyqt6_compatible_design_system import get_reliable_style_builder

try:
    from managers.window_mode_manager import WindowModeManager
    from managers.window_geometry_manager import WindowGeometryManager
except ImportError:
    from managers.window_mode_manager import WindowModeManager
    from managers.window_geometry_manager import WindowGeometryManager

logger = logging.getLogger(__name__)

logger.info("🎨 Reliable UI design system loaded successfully")


class TKAModernWindow(QWidget):
    """
    Main launcher window with modern glassmorphism design.

    Features:
    - Premium 2025 glassmorphism effects
    - Application grid with smooth animations
    - Dual-mode operation (window/docked)
    - Inter typography with 8px grid system
    - WCAG 4.5:1 contrast ratios
    """

    # Signals
    application_launched = pyqtSignal(str, str)  # app_id, app_title
    settings_changed = pyqtSignal(dict)  # settings dict

    def __init__(self, tka_integration):
        """Initialize the modern launcher window."""
        super().__init__()

        self.tka_integration = tka_integration
        self.config = LauncherConfig()

        # Initialize UI component attributes FIRST
        self.app_grid = None
        self.status_label = QLabel("Ready")  # Create immediately to ensure it exists

        # Initialize helper managers
        self.geometry_manager = WindowGeometryManager(self.config)
        self.mode_manager = WindowModeManager(self)
        self.mode_manager.set_components(self, tka_integration)

        # Window properties
        self.setWindowTitle("TKA Modern Launcher")
        self.geometry_manager.setup_window_geometry(self)
        self._setup_modern_styling()

        # Initialize UI components
        self._init_modern_ui()
        self._connect_signals()

        logger.info("✅ TKA Modern Window initialized")

    def _setup_modern_styling(self):
        """Setup reliable glassmorphism styling using proven PyQt6 patterns."""
        # Get reliable design system components
        style_builder = get_reliable_style_builder()

        # Apply consistent styling across the application
        self.setStyleSheet(
            f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 15, 15, 0.95),
                    stop:1 rgba(30, 30, 30, 0.95));
                color: #ffffff;
                {style_builder.typography()}
            }}

            QTabWidget::pane {{
                {style_builder.glass_surface('secondary')}
                border-radius: {style_builder.tokens.RADIUS['lg']}px;
            }}

            QTabBar::tab {{
                {style_builder.glass_surface('tertiary')}
                {style_builder.typography('base', 'medium')}
                color: rgba(255, 255, 255, 0.8);
                padding: {style_builder.tokens.SPACING['md']}px \
{style_builder.tokens.SPACING['lg']}px;
                margin-right: {style_builder.tokens.SPACING['xs']}px;
                border-top-left-radius: {style_builder.tokens.RADIUS['md']}px;
                border-top-right-radius: {style_builder.tokens.RADIUS['md']}px;
            }}

            QTabBar::tab:hover {{
                {style_builder.glass_surface_hover('primary')}
            }}

            QTabBar::tab:selected {{
                {style_builder.glass_surface('selected')}
                color: #ffffff;
                border: {style_builder.tokens.BORDERS['selected']};
            }}
        """
        )

        logger.info("🎨 Reliable styling applied successfully")

    def _setup_window_geometry(self):
        """Setup window geometry to 50% of screen size and center it."""
        # Get screen dimensions
        screen = QApplication.primaryScreen().geometry()

        # Calculate 50% of screen dimensions
        target_width = int(screen.width() * 0.5)
        target_height = int(screen.height() * 0.5)

        # Update config with calculated dimensions
        self.config.config.window.width = target_width
        self.config.config.window.height = target_height

        # Center the window on screen
        x = (screen.width() - target_width) // 2
        y = (screen.height() - target_height) // 2

        # Set geometry
        self.setGeometry(x, y, target_width, target_height)

        logger.info(
            "🪟 Window geometry set: %dx%d at (%d, %d) - 50%% of screen: %dx%d",
            target_width,
            target_height,
            x,
            y,
            screen.width(),
            screen.height(),
        )

    def _init_modern_ui(self):
        """Initialize the simplified single-window UI."""
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # 8px grid system (3 * 8)
        layout.setSpacing(24)

        # Create simplified interface directly (no tabs)
        self._create_simplified_interface(layout)

        logger.info("🏠 Simplified UI initialized with glassmorphism design")

    def _create_simplified_interface(self, layout):
        """Create the simplified single-window interface."""
        # Application grid (gets most of the space)
        self.app_grid = ApplicationGridWidget(self.tka_integration)
        layout.addWidget(self.app_grid, 1)  # Give it stretch factor of 1

        # Bottom section with status and dock toggle
        bottom_layout = QHBoxLayout()

        # Apply styling to the existing status label
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                padding: 4px 8px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
            }
        """
        )
        bottom_layout.addWidget(self.status_label)

        # Add stretch to push dock button to the right
        bottom_layout.addStretch()

        # Create dock toggle button
        self.dock_toggle_button = QPushButton("Switch to Dock Mode")
        self.dock_toggle_button.setStyleSheet(
            """
            QPushButton {
                color: rgba(255, 255, 255, 0.9);
                background: rgba(100, 100, 100, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(120, 120, 120, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(80, 80, 80, 0.5);
            }
        """
        )
        self.dock_toggle_button.clicked.connect(self.toggle_dock_mode)
        bottom_layout.addWidget(self.dock_toggle_button)

        layout.addLayout(bottom_layout)

    # Removed _create_modern_home_interface - now using simplified single-window layout

    # Removed _create_modern_header_section - simplified interface has no header

    # Removed _create_modern_search_section - simplified interface has no search

    # Removed _create_modern_action_section - simplified interface has no action buttons

    # Removed _create_modern_settings_interface - simplified interface has no settings tab

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # Application grid signals (only direct launching needed)
        self.app_grid.application_launched.connect(self._on_application_launched)

        # Mode manager signals
        self.mode_manager.mode_changed.connect(self._on_mode_changed)

    # Removed old event handlers - simplified interface uses direct launching only

    def _on_application_launched(self, app_id: str, app_title: str):
        """Handle application launch."""
        logger.info("🚀 Application launched: %s", app_title)

        # Emit signal
        self.application_launched.emit(app_id, app_title)

        # Update status
        self.status_label.setText(f"Launched: {app_title}")

    def toggle_dock_mode(self):
        """Toggle between window and dock modes."""
        self.mode_manager.toggle_mode()

    def _on_mode_changed(self, new_mode: str):
        """Handle mode change from mode manager."""
        # Save geometry when switching away from window mode
        if new_mode == "docked":
            self.geometry_manager.save_window_geometry(self)
        elif new_mode == "window":
            self.geometry_manager.restore_window_geometry(self)

        # Update toggle button text if it exists
        if hasattr(self, "dock_toggle_button") and self.dock_toggle_button:
            if new_mode == "docked":
                self.dock_toggle_button.setText("Switch to Window Mode")
            else:
                self.dock_toggle_button.setText("Switch to Dock Mode")

        logger.info(f"🔄 Mode changed to: {new_mode}")

    def cleanup(self):
        """Cleanup resources when closing."""
        logger.info("🧹 Cleaning up TKA Modern Window...")

        try:
            # Save current geometry before cleanup
            self.geometry_manager.save_window_geometry(self)

            # Cleanup mode manager (which handles dock window)
            self.mode_manager.cleanup()

            if hasattr(self, "app_grid"):
                self.app_grid.cleanup()

        except (AttributeError, RuntimeError) as e:
            logger.warning("⚠️ Window cleanup warning: %s", e)
