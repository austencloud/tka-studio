"""
Reliable Modern Components - Single Implementation
================================================

Replaces the complex enhanced/fallback system with reliable components
that work consistently using proven PyQt6 patterns.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from ..reliable_design_system import get_reliable_style_builder
from ..reliable_effects import get_shadow_manager, get_animation_manager


class ReliableSearchBox(QLineEdit):
    """Reliable search box with consistent glassmorphism styling."""

    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        self._setup_styling()
        self._setup_effects()

    def _setup_styling(self):
        """Apply reliable glassmorphism styling."""
        self.setStyleSheet(
            f"""
            QLineEdit {{
                {self.style_builder.glass_surface('primary')}
                border-radius: {self.style_builder.tokens.RADIUS['lg']}px;
                padding: 12px 20px;
                {self.style_builder.typography('base', 'normal')}
                color: #ffffff;
            }}
            QLineEdit:focus {{
                {self.style_builder.glass_surface_hover('primary')}
                border: {self.style_builder.tokens.BORDERS['focus']};
            }}
            QLineEdit::placeholder {{
                color: rgba(255, 255, 255, 0.5);
                font-style: italic;
            }}
        """
        )

    def _setup_effects(self):
        """Setup reliable visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    def focusInEvent(self, event):
        """Handle focus with reliable effects."""
        super().focusInEvent(event)
        self.shadow_manager.apply_hover_shadow(self)

    def focusOutEvent(self, event):
        """Handle focus out."""
        super().focusOutEvent(event)
        self.shadow_manager.reset_shadow(self)


class ReliableButton(QPushButton):
    """Reliable button with consistent styling and animations."""

    def __init__(self, text: str = "", variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()
        self.animation_manager = get_animation_manager()

        self._setup_styling()
        self._setup_effects()

    def _setup_styling(self):
        """Apply reliable button styling."""
        if self.variant == "primary":
            base_style = self.style_builder.accent_button()
        else:
            base_style = self.style_builder.secondary_button()

        self.setStyleSheet(
            f"""
            QPushButton {{
                {base_style}
                border-radius: {self.style_builder.tokens.RADIUS['md']}px;
                padding: 10px 20px;
                {self.style_builder.typography('base', 'medium')}
                min-height: 36px;
            }}
            QPushButton:hover {{
                {self.style_builder.glass_surface_hover('primary') if self.variant != 'primary' else base_style}
                border: {self.style_builder.tokens.BORDERS['hover']};
            }}
            QPushButton:pressed {{
                {self.style_builder.glass_surface('pressed')}
            }}
        """
        )

    def _setup_effects(self):
        """Setup reliable visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    def enterEvent(self, event):
        """Handle hover enter."""
        super().enterEvent(event)
        self.shadow_manager.apply_hover_shadow(self)

    def leaveEvent(self, event):
        """Handle hover leave."""
        super().leaveEvent(event)
        self.shadow_manager.reset_shadow(self)

    def mousePressEvent(self, event):
        """Handle mouse press with animation."""
        super().mousePressEvent(event)

        # Reliable button press animation
        press_anim = self.animation_manager.button_press_feedback(self)
        press_anim.start()

        self.shadow_manager.apply_pressed_shadow(self)


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
                {self.style_builder.glass_surface('secondary')}
                border-radius: {self.style_builder.tokens.RADIUS['sm']}px;
                {self.style_builder.typography('lg', 'normal')}
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
                {self.style_builder.typography('base', 'semibold')}
                color: #ffffff;
            }}
        """
        )
        title_layout.addWidget(self.title_label)

        self.category_label = QLabel(self.app_data.category.value.title())
        self.category_label.setStyleSheet(
            f"""
            QLabel {{
                {self.style_builder.typography('sm', 'normal')}
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
                {self.style_builder.typography('sm', 'normal')}
                color: rgba(255, 255, 255, 0.8);
            }}
        """
        )
        layout.addWidget(self.desc_label)

        layout.addStretch()

        # Launch button
        self.launch_btn = ReliableButton("Launch", "primary")
        self.launch_btn.clicked.connect(self._on_launch_clicked)
        layout.addWidget(self.launch_btn)

    def _setup_styling(self):
        """Setup card styling."""
        self.setStyleSheet(
            f"""
            ReliableApplicationCard {{
                {self.style_builder.glass_surface('primary')}
                border-radius: {self.style_builder.tokens.RADIUS['xl']}px;
            }}
        """
        )

    def _setup_effects(self):
        """Setup visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    def _on_launch_clicked(self):
        """Handle launch button click."""
        self.launch_requested.emit(self.app_data.id)

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected

        if selected:
            self.setStyleSheet(
                f"""
                ReliableApplicationCard {{
                    {self.style_builder.glass_surface('selected')}
                    border: {self.style_builder.tokens.BORDERS['selected']};
                    border-radius: {self.style_builder.tokens.RADIUS['xl']}px;
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
                    {self.style_builder.glass_surface_hover('primary')}
                    border-radius: {self.style_builder.tokens.RADIUS['xl']}px;
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
        """Handle mouse press."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.app_data)

            # Press animation
            press_anim = self.animation_manager.button_press_feedback(self)
            press_anim.start()
