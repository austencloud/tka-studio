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

from application_grid import ApplicationGridWidget
from launcher_config import LauncherConfig
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from ui.reliable_design_system import get_reliable_style_builder

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

        # Initialize UI component attributes
        self.app_grid = None

        # Window properties
        self.setWindowTitle("TKA Modern Launcher")
        self._setup_window_geometry()
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

    # Removed _create_modern_home_interface - now using simplified single-window layout

    # Removed _create_modern_header_section - simplified interface has no header

    # Removed _create_modern_search_section - simplified interface has no search

    # Removed _create_modern_action_section - simplified interface has no action buttons

    # Removed _create_modern_settings_interface - simplified interface has no settings tab

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # Application grid signals (only direct launching needed)
        self.app_grid.application_launched.connect(self._on_application_launched)

    # Removed old event handlers - simplified interface uses direct launching only

    def _on_application_launched(self, app_id: str, app_title: str):
        """Handle application launch."""
        logger.info("🚀 Application launched: %s", app_title)

        # Emit signal
        self.application_launched.emit(app_id, app_title)

        # Update status
        self.status_label.setText(f"Launched: {app_title}")

    def cleanup(self):
        """Cleanup resources when closing."""
        logger.info("🧹 Cleaning up TKA Modern Window...")

        try:
            if hasattr(self, "app_grid"):
                self.app_grid.cleanup()

        except (AttributeError, RuntimeError) as e:
            logger.warning("⚠️ Window cleanup warning: %s", e)
