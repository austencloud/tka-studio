#!/usr/bin/env python3
"""
Tests for ModernSearchBox component.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QLineEdit

# Add launcher directory to path for imports
launcher_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, launcher_dir)
sys.path.insert(0, os.path.join(launcher_dir, "tests"))

import test_base
from test_base import LauncherTestCase, get_test_app


class TestModernSearchBox(LauncherTestCase):
    """Test cases for ModernSearchBox component."""

    def setup_method(self):
        """Setup test environment."""
        super().setup_method()

        # Import here to avoid import issues during collection
        from components.search_box import ModernSearchBox

        self.ModernSearchBox = ModernSearchBox

    def test_search_box_creation(self):
        """Test that search box can be created with default parameters."""
        search_box = self.ModernSearchBox()

        assert isinstance(search_box, QLineEdit)
        assert search_box.placeholderText() == "Search..."

    def test_search_box_custom_placeholder(self):
        """Test search box with custom placeholder text."""
        custom_placeholder = "Type to search applications..."
        search_box = self.ModernSearchBox(placeholder=custom_placeholder)

        assert search_box.placeholderText() == custom_placeholder

    def test_search_box_styling_applied(self):
        """Test that styling is applied to the search box."""
        search_box = self.ModernSearchBox()

        # Check that styleSheet is not empty (styling was applied)
        assert len(search_box.styleSheet()) > 0

        # Check for key style properties
        style = search_box.styleSheet()
        assert "border-radius" in style
        assert "padding" in style

    def test_search_box_text_change_signal(self):
        """Test that text change signal is emitted correctly."""
        search_box = self.ModernSearchBox()

        # Track signal emissions
        signal_received = []
        search_box.textChanged.connect(lambda text: signal_received.append(text))

        # Set text programmatically
        test_text = "test search"
        search_box.setText(test_text)

        # Process events to ensure signal is emitted
        self.app.processEvents()
        # Verify signal was emitted with correct text
        assert len(signal_received) > 0
        assert signal_received[-1] == test_text

    @patch("launcher_window.ENHANCED_UI_AVAILABLE", False)
    def test_search_box_fallback_styling(self):
        """Test fallback styling when enhanced UI is not available."""
        search_box = self.ModernSearchBox()

        # Should still have styling applied
        assert len(search_box.styleSheet()) > 0

        style = search_box.styleSheet()
        assert "rgba(255, 255, 255, 0.12)" in style  # Fallback background

    def test_search_box_enhanced_styling(self):
        """Test enhanced styling gracefully handles when design system is not available."""
        # This test ensures the component doesn't break when enhanced features aren't available
        search_box = self.ModernSearchBox()

        # Should still have fallback styling applied
        assert len(search_box.styleSheet()) > 0

        style = search_box.styleSheet()
        # Should have fallback styling
        assert "rgba(255, 255, 255, 0.12)" in style  # Fallback background

    def test_search_box_focus_behavior(self):
        """Test search box focus behavior."""
        search_box = self.ModernSearchBox()
        search_box.show()

        # Initially should not have focus
        assert not search_box.hasFocus()

        # Set focus
        search_box.setFocus()
        self.app.processEvents()

        # Should now have focus
        assert search_box.hasFocus()

    def test_search_box_clear_text(self):
        """Test clearing search box text."""
        search_box = self.ModernSearchBox()

        # Set some text
        search_box.setText("test text")
        assert search_box.text() == "test text"

        # Clear text
        search_box.clear()
        assert search_box.text() == ""

    def test_search_box_keyboard_interaction(self):
        """Test keyboard interaction with search box."""
        search_box = self.ModernSearchBox()
        search_box.show()
        search_box.setFocus()

        # Simulate typing
        search_box.setText("hello")
        self.app.processEvents()

        assert search_box.text() == "hello"

        # Simulate clearing text
        search_box.setText("hell")
        self.app.processEvents()

        assert search_box.text() == "hell"
