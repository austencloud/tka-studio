"""
Integration tests for the refactored launcher components.
"""

import os
import sys

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

# Add launcher directory to path for imports
launcher_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, launcher_dir)
sys.path.insert(0, os.path.join(launcher_dir, "tests"))

import test_base
from test_base import LauncherTestCase


class TestLauncherIntegration(LauncherTestCase):
    """Integration tests for the refactored launcher."""

    def setup_method(self):
        """Setup test environment."""
        super().setup_method()
        # Import here to avoid import issues during collection
        from components.button import ModernButton as ExtractedButton
        from components.search_box import ModernSearchBox as ExtractedSearchBox
        from launcher_window import ModernButton, ModernSearchBox, TKAModernWindow

        self.TKAModernWindow = TKAModernWindow
        self.ModernSearchBox = ModernSearchBox
        self.ExtractedSearchBox = ExtractedSearchBox
        self.ModernButton = ModernButton
        self.ExtractedButton = ExtractedButton

    def test_extracted_search_box_same_as_original(self):
        """Test that the extracted search box is the same as the original import."""  # Both imports should point to the same class
        assert self.ModernSearchBox == self.ExtractedSearchBox

    def test_launcher_window_creation(self):
        """Test that the main launcher window can be created."""
        window = self.TKAModernWindow(self.tka_integration)
        assert isinstance(window, QWidget)
        assert window is not None

    def test_search_box_in_launcher_context(self):
        """Test that the search box works within the launcher context."""
        search_box = self.ModernSearchBox("Test placeholder")

        assert search_box.placeholderText() == "Test placeholder"
        assert len(search_box.styleSheet()) > 0
        # Test text input
        search_box.setText("test input")
        assert search_box.text() == "test input"

    def test_launcher_window_has_search_functionality(self):
        """Test that the launcher window properly integrates search functionality."""
        window = self.TKAModernWindow(self.tka_integration)

        # The window should be able to create and use search components
        search_widget = self.ModernSearchBox("Search applications...", parent=window)
        assert search_widget.parent() == window
        assert search_widget.placeholderText() == "Search applications..."

    def test_extracted_button_same_as_original(self):
        """Test that the extracted button is the same as the original import."""
        # Both imports should point to the same class
        assert self.ModernButton == self.ExtractedButton

    def test_button_in_launcher_context(self):
        """Test that the button works within the launcher context."""
        button = self.ModernButton("Test Button", button_type="primary")

        assert button.text() == "Test Button"
        assert button.button_type == "primary"
        assert len(button.styleSheet()) > 0

        # Test button type change
        secondary_button = self.ModernButton("Secondary", button_type="secondary")
        assert secondary_button.button_type == "secondary"
