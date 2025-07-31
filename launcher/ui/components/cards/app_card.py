"""
Reliable Application Card Component
==================================

Professional application card with glassmorphism styling and animations.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from ...pyqt6_compatible_design_system import get_reliable_style_builder
from ...reliable_effects import get_animation_manager, get_shadow_manager


class ReliableApplicationCard(QFrame):
    """Reliable application card with consistent behavior."""

    clicked = pyqtSignal(object)  # app_data
    launch_requested = pyqtSignal(str)  # app_id

    def __init__(
        self, app_data, card_width: int = 280, card_height: int = 140, parent=None
    ):
        super().__init__(parent)

        self.app_data = app_data
        self.is_selected = False

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()
        self.animation_manager = get_animation_manager()

        # Set fixed size
        self.setFixedSize(card_width, card_height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_layout()
        self._setup_styling()
        self._setup_effects()

    def _setup_layout(self):
        """Setup card layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Header with icon and title
        header_layout = QHBoxLayout()

        # Icon (emoji for simplicity)
        self.icon_label = QLabel(getattr(self.app_data, "icon", "📱"))
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.glass_surface("secondary")}
                border-radius: {self.style_builder.tokens.RADIUS["sm"]}px;
                {self.style_builder.typography("lg", "normal")}
            }}
        """
        )
        header_layout.addWidget(self.icon_label)

        # Title and category
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        self.title_label = QLabel(self.app_data.title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.typography("base", "semibold")}
                color: #ffffff;
            }}
        """
        )
        title_layout.addWidget(self.title_label)

        self.category_label = QLabel(self.app_data.category.value.title())
        self.category_label.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.typography("sm", "normal")}
                color: rgba(255, 255, 255, 0.7);
            }}
        """
        )
        title_layout.addWidget(self.category_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Description
        self.desc_label = QLabel(self.app_data.description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.typography("sm", "normal")}
                color: rgba(255, 255, 255, 0.8);
            }}
        """
        )
        layout.addWidget(self.desc_label)

        layout.addStretch()

        # Removed launch button - cards now use direct-click launching

    def _setup_styling(self):
        """Setup card styling."""
        self.setStyleSheet(
            f"""
            ReliableApplicationCard {{
                {self.style_builder.glass_surface("primary")}
                border-radius: {self.style_builder.tokens.RADIUS["xl"]}px;
            }}
        """
        )

    def _setup_effects(self):
        """Setup visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    # Removed _on_launch_clicked - using direct-click launching instead

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected

        if selected:
            self.setStyleSheet(
                f"""
                ReliableApplicationCard {{
                    {self.style_builder.glass_surface("selected")}
                    border: {self.style_builder.tokens.BORDERS["selected"]};
                    border-radius: {self.style_builder.tokens.RADIUS["xl"]}px;
                }}
            """
            )
        else:
            self._setup_styling()

    def enterEvent(self, event):
        """Handle hover enter."""
        super().enterEvent(event)

        if not self.is_selected:
            self.setStyleSheet(
                f"""
                ReliableApplicationCard {{
                    {self.style_builder.glass_surface_hover("primary")}
                    border-radius: {self.style_builder.tokens.RADIUS["xl"]}px;
                }}
            """
            )

        self.shadow_manager.apply_hover_shadow(self)

        # Reliable hover animation
        hover_anim = self.animation_manager.smooth_hover_scale(self, 1.02)
        hover_anim.start()

    def leaveEvent(self, event):
        """Handle hover leave."""
        super().leaveEvent(event)

        if not self.is_selected:
            self._setup_styling()

        self.shadow_manager.reset_shadow(self)

        # Return to normal size
        normal_anim = self.animation_manager.smooth_hover_scale(self, 1.0)
        normal_anim.start()

    def mousePressEvent(self, event):
        """Handle mouse press - direct launch on click."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Direct launch instead of selection
            self.launch_requested.emit(self.app_data.id)

            # Press animation
            press_anim = self.animation_manager.button_press_feedback(self)
            press_anim.start()
