"""
Layout component style providers (menu bar, tabs, dialogs, panels).
"""

from __future__ import annotations

from . import StyleProvider
from ..core.types import StyleVariant


class MenuBarStyleProvider(StyleProvider):
    """Style provider for menu bar components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate menu bar styling."""
        colors = self.design_system.colors
        tokens = self.design_system.tokens

        return f"""
        MenuBarWidget {{
            background: transparent;
            border: none;
            min-height: 60px;
        }}

        MenuBarWidget > QWidget {{
            background: {colors.GLASS_BASE};
            border-bottom: 2px solid {colors.ACCENT_BORDER};
            border-radius: 0px;
        }}
        """


class TabContainerStyleProvider(StyleProvider):
    """Style provider for tab container components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate tab container styling."""
        colors = self.design_system.colors
        tokens = self.design_system.tokens

        background = colors.GLASS_BASE
        if variant == StyleVariant.PROMINENT:
            background = colors.GLASS_LIGHT
        elif variant == StyleVariant.SUBTLE:
            background = colors.GLASS_BASE.replace("0.1", "0.05")

        return f"""
        QWidget {{
            background: {background};
            border: 1px solid {colors.BORDER_NORMAL};
            border-radius: {tokens.radius["lg"]};
            margin: {tokens.spacing["2"]};
        }}
        """


class DialogStyleProvider(StyleProvider):
    """Style provider for dialog components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate dialog styling that replaces scattered dialog styles."""
        colors = self.design_system.colors
        tokens = self.design_system.tokens

        return f"""
        QDialog {{
            background: transparent;
        }}

        #glassmorphism_container {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {colors.GLASS_LIGHTER},
                stop:0.5 {colors.GLASS_LIGHT},
                stop:1 {colors.GLASS_BASE});
            border: 1px solid {colors.BORDER_STRONG};
            border-radius: {tokens.radius["xl"]};
        }}

        #header_frame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors.GLASS_LIGHT},
                stop:1 {colors.GLASS_BASE});
            border: 1px solid {colors.BORDER_NORMAL};
            border-radius: {tokens.radius["lg"]};
            margin-bottom: {tokens.spacing["3"]};
            padding: {tokens.spacing["2"]};
        }}
        """


class PanelStyleProvider(StyleProvider):
    """Style provider for panel components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate panel styling."""
        colors = self.design_system.colors
        tokens = self.design_system.tokens

        return f"""
        QWidget {{
            background: {colors.GLASS_BASE};
            border: 1px solid {colors.BORDER_NORMAL};
            border-radius: {tokens.radius["base"]};
            padding: {tokens.spacing["4"]};
        }}
        """
