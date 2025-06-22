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
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QScrollArea,
    QGraphicsBlurEffect,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QLinearGradient

from application_grid import ApplicationGridWidget
from launcher_config import LauncherConfig
from components.search_box import ModernSearchBox
from components.button import ModernButton

logger = logging.getLogger(__name__)

# Import enhanced design system
try:
    from ui.design_system import (
        get_theme_manager,
        get_style_builder,
        apply_global_theme,
    )
    from ui.themes.base_theme import get_smart_theme_manager
    from ui.effects.glassmorphism import get_effect_manager
    from ui.components.animation_mixins import (
        HoverAnimationMixin,
        FeedbackAnimationMixin,
    )

    ENHANCED_UI_AVAILABLE = True
    logger.info("🎨 Enhanced UI design system loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced UI not available: {e}")
    ENHANCED_UI_AVAILABLE = False


# Enhanced Modern UI Components with Premium 2025 Design

class ModernLabel(QLabel):
    """Modern label with Inter typography."""

    def __init__(self, text="", label_type="body", parent=None):
        super().__init__(text, parent)
        self.label_type = label_type
        self._setup_typography()

    def _setup_typography(self):
        """Apply Inter typography based on label type."""
        font = QFont("Inter", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)

        if self.label_type == "title":
            font.setPointSize(24)
            font.setWeight(QFont.Weight.Bold)
            color = "#ffffff"
        elif self.label_type == "subtitle":
            font.setPointSize(16)
            font.setWeight(QFont.Weight.Medium)
            color = "rgba(255, 255, 255, 0.8)"
        elif self.label_type == "caption":
            font.setPointSize(12)
            font.setWeight(QFont.Weight.Normal)
            color = "rgba(255, 255, 255, 0.6)"
        else:  # body
            font.setPointSize(14)
            font.setWeight(QFont.Weight.Normal)
            color = "rgba(255, 255, 255, 0.9)"

        self.setFont(font)
        self.setStyleSheet(f"color: {color}; font-family: 'Inter', sans-serif;")


class ModernNotification(QFrame):
    """Modern notification widget with glassmorphism styling."""

    def __init__(self, title="", message="", notification_type="info", parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self._setup_ui(title, message)
        self._setup_styling()
        self._setup_animations()

    def _setup_ui(self, title, message):
        """Setup the notification UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Icon (emoji for now)
        icon_map = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}

        self.icon_label = QLabel(icon_map.get(self.notification_type, "ℹ️"))
        self.icon_label.setFixedSize(24, 24)
        layout.addWidget(self.icon_label)

        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        if title:
            self.title_label = ModernLabel(title, "body")
            text_layout.addWidget(self.title_label)

        self.message_label = ModernLabel(message, "caption")
        text_layout.addWidget(self.message_label)

        layout.addLayout(text_layout)
        layout.addStretch()

    def _setup_styling(self):
        """Apply modern notification styling."""
        color_map = {
            "info": "rgba(59, 130, 246, 0.2)",
            "success": "rgba(34, 197, 94, 0.2)",
            "warning": "rgba(245, 158, 11, 0.2)",
            "error": "rgba(239, 68, 68, 0.2)",
        }

        bg_color = color_map.get(self.notification_type, "rgba(59, 130, 246, 0.2)")

        self.setStyleSheet(
            f"""
            ModernNotification {{
                background: {bg_color};
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }}
        """
        )

    def _setup_animations(self):
        """Setup fade in/out animations."""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def show_notification(self):
        """Show notification with fade in."""
        self.setWindowOpacity(0.0)
        self.show()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

        # Auto-hide after 3 seconds
        QTimer.singleShot(3000, self.hide_notification)

    def hide_notification(self):
        """Hide notification with fade out."""
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()


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

        # Window properties
        self.setWindowTitle("TKA Modern Launcher")
        self._setup_window_geometry()
        self._setup_modern_styling()

        # Initialize UI components
        self._init_modern_ui()
        self._connect_signals()

        logger.info("✅ TKA Modern Window initialized")

    def _setup_modern_styling(self):
        """Setup premium 2025 glassmorphism styling with design system."""
        if ENHANCED_UI_AVAILABLE:
            try:
                # Apply global theme first
                apply_global_theme()

                # Get design system components
                style_builder = get_style_builder()
                theme = get_theme_manager().get_current_theme()

                # Enhanced styling with design system
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
                        {style_builder.glassmorphism_surface('secondary')}
                        border-radius: {theme['radius']['lg']};
                    }}

                    QTabBar::tab {{
                        {style_builder.glassmorphism_surface('tertiary')}
                        {style_builder.typography('base', 'medium')}
                        color: rgba(255, 255, 255, 0.8);
                        padding: {theme['spacing']['md']} {theme['spacing']['lg']};
                        margin-right: {theme['spacing']['xs']};
                        border-top-left-radius: {theme['radius']['md']};
                        border-top-right-radius: {theme['radius']['md']};
                    }}

                    QTabBar::tab:selected {{
                        {style_builder.glassmorphism_surface('selected')}
                        color: #ffffff;
                        border: 1px solid {theme['accent']['primary']};
                    }}

                    QTabBar::tab:hover {{
                        {style_builder.glassmorphism_surface('hover')}
                    }}
                """
                )

                # Setup smart theme manager
                smart_theme_manager = get_smart_theme_manager()
                smart_theme_manager.theme_changed.connect(self._on_theme_changed)

                logger.info("🎨 Enhanced styling applied with design system")

            except Exception as e:
                logger.warning(f"Could not apply enhanced styling: {e}")
                self._apply_fallback_styling()
        else:
            self._apply_fallback_styling()

    def _apply_fallback_styling(self):
        """Apply fallback styling when enhanced UI is not available."""
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 15, 15, 0.95),
                    stop:1 rgba(30, 30, 30, 0.95));
                color: #ffffff;
                font-family: 'Inter', 'Segoe UI', sans-serif;
            }

            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
            }

            QTabBar::tab {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.8);
                padding: 12px 20px;
                margin-right: 4px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-family: 'Inter', sans-serif;
                font-weight: 500;
                font-size: 14px;
            }

            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )

    def _on_theme_changed(self, new_theme):
        """Handle theme changes and update styling."""
        logger.info("🎨 Theme changed, updating window styling")
        self._setup_modern_styling()

    def _setup_window_geometry(self):
        """Setup window geometry to 50% of screen size and center it."""
        from PyQt6.QtWidgets import QApplication

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
            f"🪟 Window geometry set: {target_width}x{target_height} at ({x}, {y}) - 50% of screen: {screen.width()}x{screen.height()}"
        )

    def _init_modern_ui(self):
        """Initialize the modern UI with glassmorphism design."""
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # 8px grid system (3 * 8)
        layout.setSpacing(24)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create interfaces
        self.home_interface = self._create_modern_home_interface()
        self.settings_interface = self._create_modern_settings_interface()

        # Add tabs
        self.tab_widget.addTab(self.home_interface, "🏠 Home")
        self.tab_widget.addTab(self.settings_interface, "⚙️ Settings")

        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        layout.addWidget(self.tab_widget)

        logger.info("🏠 Modern UI initialized with glassmorphism design")

    def _create_modern_home_interface(self) -> QWidget:
        """Create the modern home interface with glassmorphism design."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(32, 24, 32, 24)  # 8px grid system
        layout.setSpacing(24)  # 8px grid system

        # Header section with modern styling
        header_layout = self._create_modern_header_section()
        layout.addLayout(header_layout)

        # Search section with glassmorphism
        search_layout = self._create_modern_search_section()
        layout.addLayout(search_layout)

        # Application grid (gets most of the space)
        self.app_grid = ApplicationGridWidget(self.tka_integration)
        layout.addWidget(self.app_grid, 1)  # Give it stretch factor of 1

        # Action buttons with modern styling
        action_layout = self._create_modern_action_section()
        layout.addLayout(action_layout)

        return widget

    def _create_modern_header_section(self) -> QHBoxLayout:
        """Create the modern header section with glassmorphism styling."""
        layout = QHBoxLayout()

        # Title and subtitle with modern typography
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)  # 8px grid system

        self.title_label = ModernLabel("TKA Applications", "title")
        self.subtitle_label = ModernLabel(
            "Launch and manage your TKA applications", "caption"
        )

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        layout.addLayout(title_layout)
        layout.addStretch()

        # Mode toggle button with modern styling
        self.mode_toggle_btn = ModernButton("Switch to Docked Mode", "secondary")
        layout.addWidget(self.mode_toggle_btn)

        return layout

    def _create_modern_search_section(self) -> QHBoxLayout:
        """Create the modern search section with glassmorphism styling."""
        layout = QHBoxLayout()
        layout.setSpacing(16)  # 8px grid system

        # Search label with modern typography
        search_label = ModernLabel("Search:", "body")
        layout.addWidget(search_label)

        # Modern search box with glassmorphism
        self.search_box = ModernSearchBox("Type to search applications...")
        self.search_box.setFixedWidth(400)
        layout.addWidget(self.search_box)

        layout.addStretch()

        # Refresh button with modern styling
        self.refresh_btn = ModernButton("Refresh", "secondary")
        layout.addWidget(self.refresh_btn)

        return layout

    def _create_modern_action_section(self) -> QHBoxLayout:
        """Create the modern action buttons section."""
        layout = QHBoxLayout()
        layout.setSpacing(16)  # 8px grid system

        # Launch button with modern styling
        self.launch_btn = ModernButton("Launch Selected", "primary")
        self.launch_btn.setEnabled(False)  # Enabled when app is selected
        layout.addWidget(self.launch_btn)

        layout.addStretch()

        # Status label with modern typography
        self.status_label = ModernLabel("Ready", "caption")
        layout.addWidget(self.status_label)

        return layout

    def _create_modern_settings_interface(self) -> QWidget:
        """Create the modern settings interface."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(32, 24, 32, 24)  # 8px grid system
        layout.setSpacing(24)

        # Settings title with modern typography
        title = ModernLabel("Launcher Settings", "title")
        layout.addWidget(title)

        # Settings content (placeholder for now)
        content_label = ModernLabel("Settings panel will be implemented here.", "body")
        layout.addWidget(content_label)

        layout.addStretch()

        return widget

    def _on_tab_changed(self, index):
        """Handle tab change."""
        if index == 0:
            logger.info("🏠 Switched to Home tab")
        elif index == 1:
            logger.info("⚙️ Switched to Settings tab")
        else:
            logger.info(f"🔄 Switched to tab {index}")

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # Search functionality
        self.search_box.textChanged.connect(self._on_search_changed)

        # Button actions
        self.refresh_btn.clicked.connect(self._on_refresh_clicked)
        self.launch_btn.clicked.connect(self._on_launch_clicked)
        self.mode_toggle_btn.clicked.connect(self._on_mode_toggle_clicked)

        # Application grid signals
        self.app_grid.application_selected.connect(self._on_application_selected)
        self.app_grid.application_launched.connect(self._on_application_launched)

    def _on_search_changed(self, text: str):
        """Handle search text changes."""
        logger.info(f"🔍 Search text changed: '{text}'")
        self.app_grid.filter_applications(text)

        # Update status
        if text:
            self.status_label.setText(f"Searching for '{text}'...")
        else:
            self.status_label.setText("Ready")

    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        logger.info("🔄 Refresh button clicked - refreshing applications...")

        try:
            self.app_grid.refresh_applications()
            self.status_label.setText("Applications refreshed")
            logger.info("✅ Refresh completed successfully")

            # Show modern success notification
            notification = ModernNotification(
                title="Refreshed",
                message="Application list has been updated",
                notification_type="success",
                parent=self,
            )
            notification.show_notification()
        except Exception as e:
            logger.error(f"❌ Refresh failed: {e}")
            # Show modern error notification
            notification = ModernNotification(
                title="Refresh Failed",
                message=f"Failed to refresh applications: {str(e)}",
                notification_type="error",
                parent=self,
            )
            notification.show_notification()

    def _on_launch_clicked(self):
        """Handle launch button click."""
        logger.info("🚀 Launch button clicked")

        selected_app = self.app_grid.get_selected_application()
        if selected_app:
            logger.info(f"🎯 Launching selected application: {selected_app.title}")
            self.app_grid.launch_application(selected_app.id)
        else:
            logger.warning("⚠️ No application selected for launch")
            # Show modern warning notification
            notification = ModernNotification(
                title="No Selection",
                message="Please select an application to launch",
                notification_type="warning",
                parent=self,
            )
            notification.show_notification()

    def _on_mode_toggle_clicked(self):
        """Handle mode toggle button click."""
        logger.info("🔄 Mode toggle button clicked")

        current_mode = self.config.get_window_mode()
        logger.info(f"📊 Current window mode: {current_mode}")

        # TODO: Implement dual-mode functionality
        logger.info("⚠️ Dual-mode functionality not yet implemented")

        # Show modern notification
        notification = ModernNotification(
            title="Coming Soon",
            message="Docked mode will be available in a future update",
            notification_type="warning",
            parent=self,
        )
        notification.show_notification()

    def _on_application_selected(self, app_data):
        """Handle application selection."""
        if app_data:
            self.launch_btn.setEnabled(True)
            self.launch_btn.setText(f"Launch {app_data.title}")
            self.status_label.setText(f"Selected: {app_data.title}")
        else:
            self.launch_btn.setEnabled(False)
            self.launch_btn.setText("Launch Selected")
            self.status_label.setText("Ready")

    def _on_application_launched(self, app_id: str, app_title: str):
        """Handle application launch."""
        logger.info(f"🚀 Application launched: {app_title}")

        # Emit signal
        self.application_launched.emit(app_id, app_title)

        # Update status
        self.status_label.setText(f"Launched: {app_title}")

        # Show modern success notification
        notification = ModernNotification(
            title="Application Launched",
            message=f"{app_title} has been started successfully",
            notification_type="success",
            parent=self,
        )
        notification.show_notification()

    def cleanup(self):
        """Cleanup resources when closing."""
        logger.info("🧹 Cleaning up TKA Fluent Window...")

        try:
            if hasattr(self, "app_grid"):
                self.app_grid.cleanup()

        except Exception as e:
            logger.warning(f"⚠️ Window cleanup warning: {e}")
