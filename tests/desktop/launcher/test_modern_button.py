"""
Tests for ModernButton component.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QPushButton

# Add launcher directory to path for imports
launcher_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, launcher_dir)
sys.path.insert(0, os.path.join(launcher_dir, "tests"))

import test_base
from test_base import LauncherTestCase, get_test_app


class TestModernButton(LauncherTestCase):
    """Test cases for ModernButton component."""

    def setup_method(self):
        """Setup test environment."""
        super().setup_method()

        # Import here to avoid import issues during collection
        from components.button import ModernButton

        self.ModernButton = ModernButton

    def test_button_creation_default(self):
        """Test that button can be created with default parameters."""
        button = self.ModernButton()

        assert isinstance(button, QPushButton)
        assert button.text() == ""
        assert button.button_type == "primary"

    def test_button_creation_with_text(self):
        """Test button creation with custom text."""
        button_text = "Click Me"
        button = self.ModernButton(button_text)

        assert button.text() == button_text
        assert button.button_type == "primary"

    def test_button_creation_secondary(self):
        """Test button creation with secondary style."""
        button = self.ModernButton("Secondary", button_type="secondary")

        assert button.text() == "Secondary"
        assert button.button_type == "secondary"

    def test_button_styling_applied(self):
        """Test that styling is applied to the button."""
        button = self.ModernButton("Test Button")
        # Check that styleSheet is not empty (styling was applied)
        assert len(button.styleSheet()) > 0

    def test_primary_button_styling(self):
        """Test primary button has correct styling."""
        button = self.ModernButton("Primary", button_type="primary")

        style = button.styleSheet()
        # Should have primary button styling
        assert "rgba(59, 130, 246" in style  # Primary blue color
        assert "QPushButton" in style

    def test_secondary_button_styling(self):
        """Test secondary button has correct styling."""
        button = self.ModernButton("Secondary", button_type="secondary")

        style = button.styleSheet()
        # Should have secondary button styling (more transparent)
        assert "rgba(255, 255, 255" in style  # Secondary transparent style
        assert "QPushButton" in style

    def test_button_click_signal(self):
        """Test button click signal is emitted."""
        button = self.ModernButton("Click Test")

        # Track click signal
        clicked_count = []
        button.clicked.connect(lambda: clicked_count.append(1))

        # Simulate button click
        button.click()

        # Process events to ensure signal is emitted
        self.app.processEvents()

        # Verify signal was emitted
        assert len(clicked_count) == 1

    def test_button_mouse_events(self):
        """Test button responds to mouse events."""
        button = self.ModernButton("Mouse Test")

        # Button should handle mouse events without errors
        button.show()

        # Simulate mouse press and release
        QTest.mousePress(button, Qt.MouseButton.LeftButton)
        self.app.processEvents()

        QTest.mouseRelease(button, Qt.MouseButton.LeftButton)
        self.app.processEvents()

        # If we get here without exceptions, mouse events work
        assert True

    def test_button_hover_behavior(self):
        """Test button hover behavior."""
        button = self.ModernButton("Hover Test")
        button.show()

        # Simulate enter and leave events
        QTest.mouseMove(button, button.rect().center())
        self.app.processEvents()

        # Button should handle hover events without errors
        assert True

    def test_button_text_update(self):
        """Test that button text can be updated."""
        button = self.ModernButton("Initial")

        new_text = "Updated Text"
        button.setText(new_text)

        assert button.text() == new_text

    def test_button_enabled_state(self):
        """Test button enabled/disabled state."""
        button = self.ModernButton("Enabled Test")

        # Button should be enabled by default
        assert button.isEnabled()

        # Disable button
        button.setEnabled(False)
        assert not button.isEnabled()

        # Re-enable button
        button.setEnabled(True)
        assert button.isEnabled()

    def test_button_animations_setup(self):
        """Test that animations are set up properly."""
        button = self.ModernButton("Animation Test")

        # Button should have some form of animation setup
        # (either enhanced or fallback)
        assert hasattr(button, "animation") or hasattr(button, "press_animation")

    def test_button_fallback_styling(self):
        """Test fallback styling when enhanced UI is not available."""
        # The button should always have fallback styling
        button = self.ModernButton("Fallback Test")

        # Should still have styling applied
        assert len(button.styleSheet()) > 0

        style = button.styleSheet()
        # Should have basic button properties
        assert "QPushButton" in style
