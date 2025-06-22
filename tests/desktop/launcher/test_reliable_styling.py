#!/usr/bin/env python3
"""Test that reliable styling works consistently."""

import sys
from pathlib import Path

# Add launcher directory to Python path
launcher_dir = Path(__file__).parent
sys.path.insert(0, str(launcher_dir))

from PyQt6.QtWidgets import QApplication
from ui.components import ReliableButton, ReliableSearchBox
from ui.reliable_design_system import get_reliable_style_builder
from ui.reliable_effects import get_shadow_manager


def test_reliable_components():
    """Test all reliable components work without errors."""

    style_builder = get_reliable_style_builder()
    shadow_manager = get_shadow_manager()

    # Test style generation
    glass_surface = style_builder.glass_surface("primary")
    assert (
        "background-color:" in glass_surface
    ), "Glass surface should have background-color"
    assert "border:" in glass_surface, "Glass surface should have border"

    hover_surface = style_builder.glass_surface_hover("primary")
    assert (
        "background-color:" in hover_surface
    ), "Hover surface should have background-color"
    assert "border:" in hover_surface, "Hover surface should have border"

    accent_button = style_builder.accent_button()
    assert (
        "background-color:" in accent_button
    ), "Accent button should have background-color"
    assert "color:" in accent_button, "Accent button should have text color"

    secondary_button = style_builder.secondary_button()
    assert (
        "background-color:" in secondary_button
    ), "Secondary button should have background-color"

    typography = style_builder.typography("base", "medium")
    assert "font-family:" in typography, "Typography should have font-family"
    assert "font-size:" in typography, "Typography should have font-size"
    assert "font-weight:" in typography, "Typography should have font-weight"

    print("✅ Style builder generates correct CSS")

    # Test component creation
    app = QApplication([])

    try:
        button = ReliableButton("Test Button")
        search = ReliableSearchBox("Test Search")

        # Components should have styles applied
        assert button.styleSheet() != "", "Button should have non-empty stylesheet"
        assert search.styleSheet() != "", "Search box should have non-empty stylesheet"

        # Test that components have proper attributes
        assert hasattr(button, "style_builder"), "Button should have style_builder"
        assert hasattr(button, "shadow_manager"), "Button should have shadow_manager"
        assert hasattr(
            button, "animation_manager"
        ), "Button should have animation_manager"

        assert hasattr(search, "style_builder"), "Search should have style_builder"
        assert hasattr(search, "shadow_manager"), "Search should have shadow_manager"

        print("✅ Components create successfully with proper attributes")

        # Test shadow manager
        shadow = shadow_manager.apply_card_shadow(button)
        assert shadow is not None, "Shadow should be applied"
        assert (
            id(button) in shadow_manager.active_shadows
        ), "Button should be in active shadows"

        print("✅ Shadow effects work correctly")

        # Test style tokens
        tokens = style_builder.tokens
        assert len(tokens.GLASS) > 0, "Should have glass tokens"
        assert len(tokens.BORDERS) > 0, "Should have border tokens"
        assert len(tokens.SHADOWS) > 0, "Should have shadow tokens"
        assert len(tokens.ACCENTS) > 0, "Should have accent tokens"
        assert len(tokens.TYPOGRAPHY) > 0, "Should have typography tokens"

        print("✅ Design tokens are properly configured")

        print("\n🎉 All reliable components work correctly!")
        print("✨ Ready to migrate launcher to reliable system")

    except Exception as e:
        print(f"❌ Error testing components: {e}")
        raise
    finally:
        app.quit()


if __name__ == "__main__":
    test_reliable_components()
