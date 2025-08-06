"""
Style mixins for easy component integration with the design system.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from .core.types import ComponentType, StyleVariant
from .design_system import get_design_system


class StyleMixin:
    """
    Mixin to add centralized styling capabilities to any QWidget component.

    This mixin provides a simple interface for components to adopt the
    centralized design system without needing to manage styling details.
    """

    def apply_design_system_style(
        self,
        component_type: ComponentType,
        variant: StyleVariant = StyleVariant.DEFAULT,
        **kwargs,
    ) -> None:
        """
        Apply centralized design system styling to this component.

        Args:
            component_type: The type of component for styling
            variant: The style variant to apply
            **kwargs: Additional component-specific styling options
        """
        if not isinstance(self, QWidget):
            raise TypeError("StyleMixin can only be used with QWidget subclasses")

        design_system = get_design_system()
        style = design_system.create_component_style(component_type, variant, **kwargs)
        self.setStyleSheet(style)

    def apply_button_style(
        self,
        variant: StyleVariant = StyleVariant.DEFAULT,
        size: str = "medium",
        **kwargs,
    ) -> None:
        """Convenience method for applying button styling."""
        self.apply_design_system_style(
            ComponentType.BUTTON, variant, size=size, **kwargs
        )

    def apply_menu_bar_style(self, **kwargs) -> None:
        """Convenience method for applying menu bar styling."""
        self.apply_design_system_style(ComponentType.MENU_BAR, **kwargs)

    def apply_dialog_style(self, **kwargs) -> None:
        """Convenience method for applying dialog styling."""
        self.apply_design_system_style(ComponentType.DIALOG, **kwargs)

    def apply_label_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> None:
        """Convenience method for applying label styling."""
        self.apply_design_system_style(ComponentType.LABEL, variant, **kwargs)

    def apply_panel_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> None:
        """Convenience method for applying panel styling."""
        self.apply_design_system_style(ComponentType.PANEL, variant, **kwargs)


class StyledWidget(QWidget, StyleMixin):
    """
    Base widget class that includes styling capabilities.

    Use this as a base class for new components that need design system integration.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Default styling can be applied here if needed


# Helper functions for direct styling without mixins
def apply_style_to_widget(
    widget: QWidget,
    component_type: ComponentType,
    variant: StyleVariant = StyleVariant.DEFAULT,
    **kwargs,
) -> None:
    """
    Apply design system styling to any widget without using mixins.

    This function is useful for styling existing widgets that can't inherit
    from StyleMixin.
    """
    design_system = get_design_system()
    style = design_system.create_component_style(component_type, variant, **kwargs)
    widget.setStyleSheet(style)


def apply_dialog_style_to_widget(widget: QWidget, **kwargs) -> None:
    """Apply dialog styling to any widget."""
    apply_style_to_widget(widget, ComponentType.DIALOG, **kwargs)
