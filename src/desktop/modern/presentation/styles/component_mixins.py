"""
Style Mixins for TKA Modern Desktop Components
=============================================

This module provides mixin classes that components can inherit from or use
to easily adopt the centralized design system styling. These mixins eliminate
the need for components to implement their own styling logic.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from .design_system import ComponentType, StyleVariant, get_design_system


class StyleMixin:
    """
    Base mixin that adds centralized styling capabilities to any QWidget.

    This mixin provides a simple interface for applying consistent styling
    without requiring knowledge of the underlying design system implementation.
    """

    def apply_design_system_style(
        self,
        component_type: ComponentType,
        variant: StyleVariant = StyleVariant.DEFAULT,
        **kwargs,
    ) -> None:
        """
        Apply centralized design system styling to this widget.

        Args:
            component_type: The type of component to style as
            variant: The style variant to apply
            **kwargs: Additional component-specific styling options
        """
        if not isinstance(self, QWidget):
            raise TypeError("StyleMixin can only be used with QWidget subclasses")

        design_system = get_design_system()
        style = design_system.create_component_style(component_type, variant, **kwargs)
        self.setStyleSheet(style)

    def apply_glassmorphism_container(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> None:
        """Convenience method to apply glassmorphism container styling."""
        self.apply_design_system_style(ComponentType.CONTAINER, variant, **kwargs)

    def apply_glassmorphism_panel(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> None:
        """Convenience method to apply glassmorphism panel styling."""
        self.apply_design_system_style(ComponentType.PANEL, variant, **kwargs)


class ButtonStyleMixin(StyleMixin):
    """Specialized mixin for button components."""

    def apply_button_style(
        self,
        variant: StyleVariant = StyleVariant.DEFAULT,
        size: str = "medium",
        **kwargs,
    ) -> None:
        """Apply centralized button styling."""
        self.apply_design_system_style(
            ComponentType.BUTTON, variant, size=size, **kwargs
        )


class LabelStyleMixin(StyleMixin):
    """Specialized mixin for label components."""

    def apply_label_style(
        self,
        variant: StyleVariant = StyleVariant.DEFAULT,
        size: str = "base",
        weight: str = "normal",
        **kwargs,
    ) -> None:
        """Apply centralized label styling."""
        self.apply_design_system_style(
            ComponentType.LABEL, variant, size=size, weight=weight, **kwargs
        )


class TabContainerStyleMixin(StyleMixin):
    """Specialized mixin for tab container components."""

    def apply_tab_container_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> None:
        """Apply centralized tab container styling."""
        self.apply_design_system_style(ComponentType.TAB_CONTAINER, variant, **kwargs)


class DialogStyleMixin(StyleMixin):
    """Specialized mixin for dialog components."""

    def apply_dialog_style(self, **kwargs) -> None:
        """Apply centralized dialog styling."""
        self.apply_design_system_style(ComponentType.DIALOG, **kwargs)


class MenuBarStyleMixin(StyleMixin):
    """Specialized mixin for menu bar components."""

    def apply_menu_bar_style(self, **kwargs) -> None:
        """Apply centralized menu bar styling."""
        self.apply_design_system_style(ComponentType.MENU_BAR, **kwargs)


# Utility functions for non-mixin usage
def apply_consistent_text_styling(
    widget: QWidget,
    variant: StyleVariant = StyleVariant.DEFAULT,
    size: str = "base",
    weight: str = "normal",
) -> None:
    """
    Apply consistent text styling to any widget.

    This function replaces scattered rgba() color usage with centralized text styling.

    Args:
        widget: The widget to style
        variant: Text style variant (DEFAULT, ACCENT, SUBTLE, MUTED, etc.)
        size: Font size (xs, sm, base, lg, xl, etc.)
        weight: Font weight (light, normal, medium, semibold, bold)
    """
    design_system = get_design_system()
    style = design_system.create_label_style(variant, size=size, weight=weight)
    widget.setStyleSheet(style)


def apply_consistent_overlay_styling(
    widget: QWidget, variant: StyleVariant = StyleVariant.DEFAULT
) -> None:
    """
    Apply consistent overlay styling to any widget.

    This function replaces hardcoded rgba(0, 0, 0, 0.9) usage with centralized overlay styling.

    Args:
        widget: The widget to style as an overlay
        variant: Overlay variant (DEFAULT for dark, SUBTLE for lighter)
    """
    design_system = get_design_system()
    style = design_system.create_overlay_style(variant)
    widget.setStyleSheet(style)


# Migration utilities for existing components
class StyleMigrationHelper:
    """
    Helper class to assist in migrating existing components to the centralized system.

    This class provides utilities to identify and replace common styling anti-patterns.
    """

    @staticmethod
    def replace_hardcoded_rgba_text(
        widget: QWidget, variant: StyleVariant = None
    ) -> None:
        """
        Replace hardcoded rgba text colors with centralized styling.

        Args:
            widget: Widget to update
            variant: Style variant to apply (auto-detected if None)
        """
        if variant is None:
            # Auto-detect variant based on common rgba patterns
            current_style = widget.styleSheet()
            if "rgba(255, 255, 255, 0.9)" in current_style:
                variant = StyleVariant.ACCENT
            elif "rgba(255, 255, 255, 0.8)" in current_style:
                variant = StyleVariant.DEFAULT
            elif (
                "rgba(255, 255, 255, 0.6)" in current_style
                or "rgba(255, 255, 255, 0.5)" in current_style
            ):
                variant = StyleVariant.MUTED
            else:
                variant = StyleVariant.DEFAULT

        apply_consistent_text_styling(widget, variant)

    @staticmethod
    def replace_hardcoded_rgba_overlay(widget: QWidget) -> None:
        """Replace hardcoded rgba overlay colors with centralized styling."""
        current_style = widget.styleSheet()
        if "rgba(0, 0, 0, 0.5)" in current_style:
            variant = StyleVariant.SUBTLE
        else:
            variant = StyleVariant.DEFAULT

        apply_consistent_overlay_styling(widget, variant)


# Example usage patterns for developers
class StyleUsageExamples:
    """
    Documentation class showing proper usage patterns for the centralized styling system.

    This class serves as living documentation for developers.
    """

    @staticmethod
    def example_button_styling():
        """Example of how to style buttons using the centralized system."""
        # BEFORE (scattered approach):
        # button.setStyleSheet("background: rgba(100, 149, 237, 0.8); border: 2px solid rgba(100, 149, 237, 1.0);")

        # AFTER (centralized approach):
        from PyQt6.QtWidgets import QPushButton

        button = QPushButton("Example")

        # Method 1: Using mixin
        if hasattr(button, "apply_button_style"):
            button.apply_button_style(StyleVariant.ACCENT, size="medium")

        # Method 2: Using utility function
        design_system = get_design_system()
        style = design_system.create_button_style(StyleVariant.ACCENT, size="medium")
        button.setStyleSheet(style)

    @staticmethod
    def example_text_styling():
        """Example of how to style text using the centralized system."""
        # BEFORE (scattered approach):
        # label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")

        # AFTER (centralized approach):
        from PyQt6.QtWidgets import QLabel

        label = QLabel("Example text")

        # Use the utility function
        apply_consistent_text_styling(
            label, StyleVariant.DEFAULT, size="base", weight="normal"
        )

    @staticmethod
    def example_container_styling():
        """Example of how to style containers using the centralized system."""
        # BEFORE (scattered approach):
        # container.setStyleSheet("background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);")

        # AFTER (centralized approach):
        from PyQt6.QtWidgets import QWidget

        container = QWidget()

        # Using mixin
        if hasattr(container, "apply_glassmorphism_container"):
            container.apply_glassmorphism_container(StyleVariant.DEFAULT)
