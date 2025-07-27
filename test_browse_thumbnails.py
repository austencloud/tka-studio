#!/usr/bin/env python3
"""
Test script to debug browse tab thumbnail loading issues.
"""

import sys
from pathlib import Path

# Add the correct paths for TKA imports
tka_root = Path.cwd()
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern"))
sys.path.insert(0, str(tka_root / "src" / "desktop"))
sys.path.insert(0, str(tka_root / "src"))

import logging

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

# Set up logging
logging.basicConfig(level=logging.INFO)


def test_browse_thumbnails():
    """Test browse tab thumbnail loading."""

    # Create app
    app = QApplication([])

    # Import and create browse tab
    from desktop.modern.core.dependency_injection.di_container import DIContainer
    from desktop.modern.presentation.tabs.browse.browse_tab import BrowseTab
    from desktop.modern.presentation.tabs.browse.models import FilterType

    sequences_dir = Path("data/sequences")
    settings_file = Path("settings.json")
    container = DIContainer()

    browse_tab = BrowseTab(sequences_dir, settings_file, container)
    browse_tab.show()

    print("Browse tab created and shown")
    print(
        f"Internal stack current index: {browse_tab.internal_left_stack.currentIndex()}"
    )

    def test_filter():
        print("\n=== TESTING FILTER SELECTION ===")
        print("Triggering ALL_SEQUENCES filter...")

        # Get the filter selection panel
        filter_panel = browse_tab.filter_selection_panel
        print(f"Filter panel visible: {filter_panel.isVisible()}")

        # Trigger the filter
        filter_panel._handle_filter_selection(FilterType.ALL_SEQUENCES, None)
        print(
            f"After filter - Internal stack current index: {browse_tab.internal_left_stack.currentIndex()}"
        )

        # Check if we switched to sequence browser
        browser_panel = browse_tab.sequence_browser_panel
        print(f"Browser panel visible: {browser_panel.isVisible()}")

        # Check the grid layout
        if browser_panel.grid_layout:
            print(f"Grid layout exists: True")
            print(f"Grid layout row count: {browser_panel.grid_layout.rowCount()}")
            print(f"Grid layout item count: {browser_panel.grid_layout.count()}")

            # Check if there are any widgets in the grid
            for i in range(browser_panel.grid_layout.count()):
                item = browser_panel.grid_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    print(
                        f"Grid item {i}: {type(widget).__name__} - visible: {widget.isVisible()}"
                    )
        else:
            print("Grid layout is None!")
            # Debug why grid layout is None
            print(f"Browser panel ui_setup: {browser_panel.ui_setup}")
            if browser_panel.ui_setup:
                print(f"UI setup grid_layout: {browser_panel.ui_setup.grid_layout}")
                print(f"UI setup grid_widget: {browser_panel.ui_setup.grid_widget}")
                print(f"UI setup scroll_area: {browser_panel.ui_setup.scroll_area}")

        # Check the scroll area
        if browser_panel.scroll_area:
            print(f"Scroll area exists: True")
            print(f"Scroll area visible: {browser_panel.scroll_area.isVisible()}")
            scroll_widget = browser_panel.scroll_area.widget()
            if scroll_widget:
                print(
                    f"Scroll widget: {type(scroll_widget).__name__} - visible: {scroll_widget.isVisible()}"
                )
            else:
                print("Scroll widget is None!")
        else:
            print("Scroll area is None!")

        # Check the browsing widget
        if hasattr(browser_panel, "browsing_widget") and browser_panel.browsing_widget:
            print(
                f"Browsing widget visible: {browser_panel.browsing_widget.isVisible()}"
            )

        # Check loading state
        if hasattr(browser_panel, "loading_widget") and browser_panel.loading_widget:
            print(f"Loading widget visible: {browser_panel.loading_widget.isVisible()}")

        # Check if progressive loading service is working
        if browser_panel.progressive_loading_service:
            print(f"Progressive loading service exists: True")
            print(
                f"Is loading: {browser_panel.progressive_loading_service._is_loading}"
            )
        else:
            print("Progressive loading service is None!")

    def check_after_delay():
        print("\n=== CHECKING AFTER 3 SECOND DELAY ===")
        browser_panel = browse_tab.sequence_browser_panel

        if browser_panel.grid_layout:
            print(f"Grid layout row count: {browser_panel.grid_layout.rowCount()}")
            print(f"Grid layout item count: {browser_panel.grid_layout.count()}")

            # List all widgets in the grid
            for i in range(browser_panel.grid_layout.count()):
                item = browser_panel.grid_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    print(
                        f"Grid item {i}: {type(widget).__name__} - visible: {widget.isVisible()} - size: {widget.size()}"
                    )

        # Check all loaded sequences
        print(f"All loaded sequences count: {len(browser_panel.all_loaded_sequences)}")

        app.quit()

    # Schedule the tests
    QTimer.singleShot(1000, test_filter)
    QTimer.singleShot(4000, check_after_delay)

    return app.exec()


if __name__ == "__main__":
    test_browse_thumbnails()
