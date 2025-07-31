"""
Launcher UI Components - Reliable Design System
==============================================

Modern launcher components built with the reliable design system.
These replace the old ModernXXX components with simpler, more reliable versions.
"""

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from ui.pyqt6_compatible_design_system import get_reliable_style_builder
from ui.reliable_effects import get_animation_manager, get_shadow_manager


class LauncherLabel(QLabel):
    """Reliable label component with consistent styling."""

    def __init__(self, text="", size="base", weight="normal", parent=None):
        super().__init__(text, parent)
        self.style_builder = get_reliable_style_builder()
        self._setup_styling(size, weight)

    def _setup_styling(self, size: str, weight: str):
        """Apply reliable label styling."""
        self.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.typography(size, weight)}
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }}
        """
        )


class LauncherNotification(QFrame):
    """Reliable notification component with glassmorphism styling."""

    # Signals
    dismissed = pyqtSignal()

    def __init__(self, message="", notification_type="info", parent=None):
        super().__init__(parent)
        self.message = message
        self.notification_type = notification_type

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()
        self.animation_manager = get_animation_manager()

        self._setup_layout()
        self._setup_styling()
        self._setup_effects()
        self._setup_auto_dismiss()

    def _setup_layout(self):
        """Setup notification layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Icon based on type
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}

        self.icon_label = LauncherLabel(icons.get(self.notification_type, "ℹ️"), "lg")
        layout.addWidget(self.icon_label)

        # Message
        self.message_label = LauncherLabel(self.message, "base", "normal")
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label, 1)

        # Close button (X)
        self.close_label = LauncherLabel("✕", "sm", "bold")
        self.close_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_label.mousePressEvent = self._on_close_clicked
        layout.addWidget(self.close_label)

    def _setup_styling(self):
        """Apply notification styling based on type."""
        # Color scheme based on notification type
        colors = {
            "info": self.style_builder.tokens.ACCENTS["blue"],
            "success": self.style_builder.tokens.ACCENTS["emerald"],
            "warning": self.style_builder.tokens.ACCENTS["amber"],
            "error": self.style_builder.tokens.ACCENTS["rose"],
        }

        color_scheme = colors.get(self.notification_type, colors["info"])

        self.setStyleSheet(
            f"""
            LauncherNotification {{
                {self.style_builder.glass_surface("secondary")}
                border-left: 4px solid {color_scheme["primary"]};
                border-radius: {self.style_builder.tokens.RADIUS["md"]}px;
            }}
        """
        )

    def _setup_effects(self):
        """Setup visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    def _setup_auto_dismiss(self):
        """Setup auto-dismiss timer."""
        self.dismiss_timer = QTimer()
        self.dismiss_timer.setSingleShot(True)
        self.dismiss_timer.timeout.connect(self.dismiss_with_animation)
        self.dismiss_timer.start(5000)  # Auto-dismiss after 5 seconds

    def _on_close_clicked(self, event):
        """Handle close button click."""
        self.dismiss_with_animation()

    def dismiss_with_animation(self):
        """Dismiss notification with smooth animation."""
        # Fade out animation
        fade_anim = self.animation_manager.smooth_fade(self, fade_in=False)
        fade_anim.finished.connect(self._on_animation_finished)
        fade_anim.start()

    def _on_animation_finished(self):
        """Handle animation completion."""
        self.dismissed.emit()
        self.setParent(None)
        self.deleteLater()

    def show_with_animation(self):
        """Show notification with smooth animation."""
        self.show()

        # Slide in from top
        fade_anim = self.animation_manager.smooth_fade(self, fade_in=True)
        fade_anim.start()


class LauncherStatusBar(QFrame):
    """Reliable status bar component."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        self._setup_layout()
        self._setup_styling()
        self._setup_effects()

    def _setup_layout(self):
        """Setup status bar layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(16)

        # Status label
        self.status_label = LauncherLabel("Ready", "sm", "normal")
        layout.addWidget(self.status_label)

        layout.addStretch()

        # App count label
        self.app_count_label = LauncherLabel("0 applications", "sm", "normal")
        layout.addWidget(self.app_count_label)

    def _setup_styling(self):
        """Apply status bar styling."""
        self.setStyleSheet(
            f"""
            LauncherStatusBar {{
                {self.style_builder.glass_surface("tertiary")}
                border-radius: {self.style_builder.tokens.RADIUS["sm"]}px;
            }}
        """
        )

    def _setup_effects(self):
        """Setup visual effects."""
        # Subtle shadow for status bar
        self.shadow_manager.apply_card_shadow(self)

    def update_status(self, status: str):
        """Update status text."""
        self.status_label.setText(status)

    def update_app_count(self, count: int):
        """Update application count."""
        app_text = "application" if count == 1 else "applications"
        self.app_count_label.setText(f"{count} {app_text}")


class LauncherHeader(QFrame):
    """Reliable header component with title and controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.style_builder = get_reliable_style_builder()

        self._setup_layout()
        self._setup_styling()

    def _setup_layout(self):
        """Setup header layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Title
        self.title_label = LauncherLabel("TKA Launcher", "title", "bold")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Version info
        self.version_label = LauncherLabel("v2.0", "sm", "normal")
        layout.addWidget(self.version_label)

    def _setup_styling(self):
        """Apply header styling."""
        self.setStyleSheet(
            """
            LauncherHeader {
                background: transparent;
                border: none;
            }
        """
        )
