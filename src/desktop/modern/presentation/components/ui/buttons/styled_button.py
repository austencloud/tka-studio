"""
Modern Styled Button Component

A modern PyQt6 button with context-aware styling, smooth animations, and clean design.
Adapted for the TKA modern desktop app with dependency injection principles.
Uses the centralized design system for consistent styling.
"""

from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import (
    QEasingCurve,
    QEvent,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QCursor, QFont, QIcon
from PyQt6.QtWidgets import QPushButton

from desktop.modern.presentation.styles.core.types import StyleVariant

# Import new design system
from desktop.modern.presentation.styles.mixins import StyleMixin


class ButtonContext(Enum):
    """Defines different button contexts for appropriate styling."""

    STANDARD = "standard"  # Default filter buttons, dialog buttons
    COMPACT = "compact"  # Social media icons, small UI elements
    NAVIGATION = "navigation"  # Menu navigation bar buttons
    WORKBENCH = "workbench"  # Sequence workbench circular buttons
    SETTINGS = "settings"  # Settings and configuration buttons


class ButtonState(Enum):
    """Button state enumeration for styling."""

    NORMAL = "normal"
    HOVERED = "hovered"
    PRESSED = "pressed"
    SELECTED = "selected"
    DISABLED = "disabled"


class StyledButton(QPushButton, StyleMixin):
    """A context-aware modern PyQt6 button with adaptive styling based on usage context."""

    clicked_signal = pyqtSignal(str)

    def __init__(
        self,
        label: str,
        icon_path: str | None = None,
        context: ButtonContext = ButtonContext.STANDARD,
        parent=None,
    ):
        super().__init__(label, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._state = ButtonState.NORMAL
        self._context = context
        self._animation_scale = 1.0
        self._is_selected = False

        # Context-aware properties
        self._setup_context_properties()
        self._setup_animations()

        if icon_path:
            self.setIcon(QIcon(icon_path))

        # Modern typography
        self._setup_modern_font()

        # Initial styling
        self.update_appearance()

    def _setup_context_properties(self):
        """Setup properties based on button context."""
        context_configs = {
            ButtonContext.NAVIGATION: {
                "base_height": 50,
                "base_width": 140,
                "font_size": 11,
                "font_weight": QFont.Weight.Medium,
                "border_radius": 8,
                "padding": "8px 16px",
            },
            ButtonContext.STANDARD: {
                "base_height": 32,
                "base_width": 100,
                "font_size": 10,
                "font_weight": QFont.Weight.Normal,
                "border_radius": 6,
                "padding": "6px 12px",
            },
            ButtonContext.COMPACT: {
                "base_height": 28,
                "base_width": 28,
                "font_size": 9,
                "font_weight": QFont.Weight.Normal,
                "border_radius": 4,
                "padding": "4px",
            },
            ButtonContext.SETTINGS: {
                "base_height": 36,
                "base_width": 120,
                "font_size": 10,
                "font_weight": QFont.Weight.Medium,
                "border_radius": 6,
                "padding": "6px 14px",
            },
            ButtonContext.WORKBENCH: {
                "base_height": 48,
                "base_width": 48,
                "font_size": 12,
                "font_weight": QFont.Weight.Bold,
                "border_radius": 24,
                "padding": "8px",
            },
        }

        self.config = context_configs.get(
            self._context, context_configs[ButtonContext.STANDARD]
        )

    def _setup_animations(self):
        """Setup smooth animations for modern feel."""
        self._animation = QPropertyAnimation(self, b"animationScale")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _setup_modern_font(self):
        """Setup modern typography."""
        font = QFont("Segoe UI", self.config["font_size"], self.config["font_weight"])
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        self.setFont(font)

    def set_selected(self, selected: bool):
        """Set the selected state of the button."""
        self._is_selected = selected
        self._state = ButtonState.SELECTED if selected else ButtonState.NORMAL
        self.update_appearance()

    def update_appearance(self):
        """Update button appearance based on current state and context."""
        # Try to use new design system for supported contexts
        if (
            self._context == ButtonContext.NAVIGATION
            or self._context == ButtonContext.STANDARD
        ):
            self._apply_design_system_styling()
        else:
            # Fall back to legacy styling for unsupported contexts
            self._apply_legacy_styling()

    def _apply_design_system_styling(self):
        """Apply styling using the new centralized design system."""
        try:
            # Map ButtonContext to StyleVariant
            variant = StyleVariant.DEFAULT

            if self._is_selected:
                variant = StyleVariant.ACCENT
            elif self._state == ButtonState.HOVERED:
                variant = StyleVariant.PROMINENT
            elif self._context == ButtonContext.NAVIGATION:
                variant = (
                    StyleVariant.SUBTLE
                    if not self._is_selected
                    else StyleVariant.ACCENT
                )

            # Apply the centralized button styling
            self.apply_button_style(
                variant=variant,
                size="medium",
                custom_properties={
                    "border-radius": f"{self.config['border_radius']}px",
                    "padding": self.config["padding"],
                },
            )
        except Exception as e:
            # Fallback to legacy styling if design system fails
            print(f"Design system styling failed, falling back: {e}")
            self._apply_legacy_styling()

    def _apply_legacy_styling(self):
        """Apply legacy styling as fallback."""
        if self._context == ButtonContext.NAVIGATION:
            self._apply_navigation_styling()
        elif self._context == ButtonContext.STANDARD:
            self._apply_standard_styling()
        elif self._context == ButtonContext.COMPACT:
            self._apply_compact_styling()
        elif self._context == ButtonContext.SETTINGS:
            self._apply_settings_styling()
        elif self._context == ButtonContext.WORKBENCH:
            self._apply_workbench_styling()

    def _apply_navigation_styling(self):
        """Apply modern navigation button styling."""
        base_style = f"""
            QPushButton {{
                background: {self._get_navigation_background()};
                border: {self._get_navigation_border()};
                border-radius: {self.config["border_radius"]}px;
                padding: {self.config["padding"]};
                color: {self._get_navigation_text_color()};
                font-weight: {self.config["font_weight"].value};
                text-align: center;
                outline: none;
                /* Prevent text clipping issues */
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                line-height: 1.2;
            }}
            QPushButton:hover {{
                background: {self._get_navigation_hover_background()};
                border: {self._get_navigation_hover_border()};
                /* Ensure font-weight doesn't change on hover to prevent text shifting */
                font-weight: {self.config["font_weight"].value};
            }}
            QPushButton:pressed {{
                background: {self._get_navigation_pressed_background()};
            }}
        """
        self.setStyleSheet(base_style)

    def _get_navigation_background(self):
        """Get navigation button background based on state."""
        if self._is_selected:
            return "rgba(100, 149, 237, 0.8)"  # Cornflower blue with transparency
        if self._state == ButtonState.HOVERED:
            return "rgba(255, 255, 255, 0.15)"
        if self._state == ButtonState.PRESSED:
            return "rgba(255, 255, 255, 0.25)"
        return "rgba(255, 255, 255, 0.1)"

    def _get_navigation_border(self):
        """Get navigation button border based on state."""
        if self._is_selected:
            return "2px solid rgba(100, 149, 237, 1.0)"
        return "1px solid rgba(255, 255, 255, 0.2)"

    def _get_navigation_text_color(self):
        """Get navigation button text color based on state."""
        if self._is_selected:
            return "rgba(255, 255, 255, 1.0)"
        return "rgba(255, 255, 255, 0.9)"

    def _get_navigation_hover_background(self):
        """Get navigation button hover background."""
        if self._is_selected:
            return "rgba(100, 149, 237, 0.9)"
        return "rgba(255, 255, 255, 0.2)"

    def _get_navigation_hover_border(self):
        """Get navigation button hover border."""
        if self._is_selected:
            return "2px solid rgba(100, 149, 237, 1.0)"
        return "1px solid rgba(255, 255, 255, 0.3)"

    def _get_navigation_pressed_background(self):
        """Get navigation button pressed background."""
        if self._is_selected:
            return "rgba(100, 149, 237, 1.0)"
        return "rgba(255, 255, 255, 0.3)"

    def _apply_standard_styling(self):
        """Apply standard button styling."""
        style = f"""
            QPushButton {{
                background: rgba(70, 130, 180, 0.8);
                border: 1px solid rgba(70, 130, 180, 1.0);
                border-radius: {self.config["border_radius"]}px;
                padding: {self.config["padding"]};
                color: white;
                font-weight: {self.config["font_weight"].value};
            }}
            QPushButton:hover {{
                background: rgba(70, 130, 180, 0.9);
            }}
            QPushButton:pressed {{
                background: rgba(70, 130, 180, 1.0);
            }}
        """
        self.setStyleSheet(style)

    def _apply_compact_styling(self):
        """Apply compact button styling."""
        style = f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.config["border_radius"]}px;
                padding: {self.config["padding"]};
                color: rgba(255, 255, 255, 0.8);
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.3);
            }}
        """
        self.setStyleSheet(style)

    def _apply_settings_styling(self):
        """Apply settings button styling."""
        style = f"""
            QPushButton {{
                background: rgba(128, 128, 128, 0.6);
                border: 1px solid rgba(128, 128, 128, 0.8);
                border-radius: {self.config["border_radius"]}px;
                padding: {self.config["padding"]};
                color: white;
                font-weight: {self.config["font_weight"].value};
            }}
            QPushButton:hover {{
                background: rgba(128, 128, 128, 0.8);
            }}
            QPushButton:pressed {{
                background: rgba(128, 128, 128, 1.0);
            }}
        """
        self.setStyleSheet(style)

    def _apply_workbench_styling(self):
        """Apply workbench button styling."""
        style = f"""
            QPushButton {{
                background: rgba(255, 165, 0, 0.8);
                border: 2px solid rgba(255, 165, 0, 1.0);
                border-radius: {self.config["border_radius"]}px;
                padding: {self.config["padding"]};
                color: white;
                font-weight: {self.config["font_weight"].value};
            }}
            QPushButton:hover {{
                background: rgba(255, 165, 0, 0.9);
            }}
            QPushButton:pressed {{
                background: rgba(255, 165, 0, 1.0);
            }}
        """
        self.setStyleSheet(style)

    def enterEvent(self, event: QEvent):
        """Handle mouse enter event."""
        if self._state != ButtonState.SELECTED:
            self._state = ButtonState.HOVERED
        # Only apply scaling animation for non-navigation buttons to prevent text clipping
        if self._context != ButtonContext.NAVIGATION:
            self._animate_scale(1.05)
        self.update_appearance()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        """Handle mouse leave event."""
        if self._state != ButtonState.SELECTED:
            self._state = ButtonState.NORMAL
        # Only apply scaling animation for non-navigation buttons to prevent text clipping
        if self._context != ButtonContext.NAVIGATION:
            self._animate_scale(1.0)
        self.update_appearance()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        self._state = ButtonState.PRESSED
        # Only apply scaling animation for non-navigation buttons to prevent text clipping
        if self._context != ButtonContext.NAVIGATION:
            self._animate_scale(0.95)
        self.update_appearance()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release event."""
        if self._state != ButtonState.SELECTED:
            self._state = (
                ButtonState.HOVERED if self.underMouse() else ButtonState.NORMAL
            )
        # Only apply scaling animation for non-navigation buttons to prevent text clipping
        if self._context != ButtonContext.NAVIGATION:
            self._animate_scale(1.05 if self.underMouse() else 1.0)
        self.update_appearance()
        super().mouseReleaseEvent(event)

    def _animate_scale(self, target_scale: float):
        """Animate button scale smoothly."""
        self._animation.stop()
        self._animation.setStartValue(self._animation_scale)
        self._animation.setEndValue(target_scale)
        self._animation.start()

    @pyqtProperty(float)
    def animationScale(self):
        """Get the current animation scale."""
        return self._animation_scale

    @animationScale.setter
    def animationScale(self, value: float):
        """Set the animation scale."""
        self._animation_scale = value
        self.update()
